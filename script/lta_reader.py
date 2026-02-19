#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import html
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# -------------------------
# XML helpers (namespace-safe)
# -------------------------
def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag and "}" in tag else (tag or "")

def children(elem: Optional[ET.Element]) -> List[ET.Element]:
    return list(elem) if elem is not None else []

def text_of(elem: Optional[ET.Element]) -> str:
    if elem is None or elem.text is None:
        return ""
    return elem.text.strip()

def is_leaf(elem: ET.Element) -> bool:
    # leaf = no element-children
    return len(list(elem)) == 0

def path_of(elem: ET.Element, parent_map: Dict[ET.Element, Optional[ET.Element]]) -> str:
    parts = []
    cur = elem
    while cur is not None:
        parts.append(localname(cur.tag))
        cur = parent_map.get(cur)
    return "/".join(reversed(parts))


# -------------------------
# Formatting
# -------------------------
def fmt_date(yyyymmdd: str) -> str:
    s = (yyyymmdd or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[6:8]}/{s[4:6]}/{s[0:4]}"
    return s

def fmt_time(hhmm_or_hhmmss: str) -> str:
    s = (hhmm_or_hhmmss or "").strip()
    if len(s) == 4 and s.isdigit():
        return f"{s[:2]}:{s[2:]}"
    if len(s) == 6 and s.isdigit():
        return f"{s[:2]}:{s[2:4]}:{s[4:]}"
    return s

def int_or_none(s: str) -> Optional[int]:
    s = (s or "").strip()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return None


# -------------------------
# P7M extraction (optional)
# -------------------------
def looks_pem(path: str) -> bool:
    with open(path, "rb") as f:
        head = f.read(64)
    return b"-----BEGIN" in head

def extract_p7m_to_temp_xml(p7m_path: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
    tmp_path = tmp.name
    tmp.close()

    inform = "PEM" if looks_pem(p7m_path) else "DER"

    # 1) openssl cms
    try:
        subprocess.run(
            ["openssl", "cms", "-verify", "-noverify", "-inform", inform, "-in", p7m_path, "-out", tmp_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return tmp_path
    except Exception:
        pass

    # 2) macOS security cms -D
    try:
        with open(tmp_path, "wb") as out:
            subprocess.run(
                ["/usr/bin/security", "cms", "-D", "-i", p7m_path],
                check=True,
                stdout=out,
                stderr=subprocess.DEVNULL,
            )
        return tmp_path
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise RuntimeError("Impossibile estrarre payload dal .p7m (openssl e security falliti).")


# -------------------------
# Output naming + open
# -------------------------
def strip_ext_for_output(name: str) -> str:
    low = name.lower()
    if low.endswith(".p7m"):
        name = name[:-4]
        low = name.lower()
    if low.endswith(".xml") or low.endswith(".xsi"):
        name = name[:-4]
    return name

def open_in_browser(path: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", path], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", path], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore


# -------------------------
# Collection detection (adaptive)
# -------------------------
@dataclass
class Collection:
    parent_path: str
    item_tag: str
    items: List[ET.Element]

def build_parent_map(root: ET.Element) -> Dict[ET.Element, Optional[ET.Element]]:
    parent_map: Dict[ET.Element, Optional[ET.Element]] = {root: None}
    stack = [root]
    while stack:
        cur = stack.pop()
        for c in list(cur):
            parent_map[c] = cur
            stack.append(c)
    return parent_map

def find_collections(root: ET.Element, parent_map: Dict[ET.Element, Optional[ET.Element]]) -> List[Collection]:
    cols: List[Collection] = []
    # for each parent, group children by tag name
    stack = [root]
    while stack:
        p = stack.pop()
        groups: Dict[str, List[ET.Element]] = defaultdict(list)
        for c in list(p):
            groups[localname(c.tag)].append(c)
            stack.append(c)
        for tag, items in groups.items():
            if len(items) >= 2:
                cols.append(Collection(parent_path=path_of(p, parent_map), item_tag=tag, items=items))
    return cols

def choose_primary_collection(cols: List[Collection]) -> Optional[Collection]:
    if not cols:
        return None
    # prefer common domain tags
    preferred = ["Evento", "Transazione", "TitoloAccesso", "Titolo", "Record", "Riga", "Elemento"]
    for pref in preferred:
        best = [c for c in cols if c.item_tag == pref]
        if best:
            # choose the one with most items
            return sorted(best, key=lambda c: len(c.items), reverse=True)[0]
    # else choose the biggest collection
    return sorted(cols, key=lambda c: len(c.items), reverse=True)[0]


# -------------------------
# Row extraction (adaptive)
# -------------------------
def flatten_item(item: ET.Element, max_depth: int = 2) -> Dict[str, str]:
    """
    Columns:
    - attributes: @attr
    - leaf child texts up to max_depth
    Skips nested repeated collections; includes only first occurrence for a tag.
    """
    out: Dict[str, str] = {}

    # attrs
    for k, v in (item.attrib or {}).items():
        out[f"@{k}"] = (v or "").strip()

    def walk(e: ET.Element, depth: int, prefix: str):
        if depth > max_depth:
            return
        kids = list(e)
        if not kids:
            if e is not item:
                key = prefix
                val = text_of(e)
                if key and val != "":
                    out.setdefault(key, val)
            return

        # group children by name
        grp: Dict[str, List[ET.Element]] = defaultdict(list)
        for c in kids:
            grp[localname(c.tag)].append(c)

        for name, arr in grp.items():
            # if repeated, don't expand fully here
            if len(arr) >= 2:
                out.setdefault(f"{prefix}{name}#count", str(len(arr)))
                continue
            c = arr[0]
            if is_leaf(c):
                val = text_of(c)
                if val != "":
                    out.setdefault(f"{prefix}{name}", val)
            else:
                walk(c, depth + 1, f"{prefix}{name}/")

    walk(item, 0, "")
    return out

def pick_display_columns(all_keys: List[str]) -> List[str]:
    """
    Order columns: date/time/codes/title first, then others.
    """
    def score(k: str) -> Tuple[int, int, str]:
        lk = k.lower()
        pri = 50
        if "data" in lk or "date" in lk:
            pri = 0
        elif "ora" in lk or "time" in lk:
            pri = 1
        elif "codice" in lk or "code" in lk or "id" == lk or lk.endswith("/id"):
            pri = 2
        elif "titolo" in lk or "nome" in lk or "denomin" in lk:
            pri = 3
        elif k.startswith("@"):
            pri = 4
        elif "#count" in lk:
            pri = 5
        return (pri, len(k), k)
    return sorted(all_keys, key=score)


def make_sort_key(val: str) -> str:
    """
    Used for data-sort; tries date yyyymmdd, time hhmm/ hhmmss, integers.
    """
    v = (val or "").strip()
    if re.fullmatch(r"\d{8}", v):
        return v  # YYYYMMDD
    if re.fullmatch(r"\d{4}(\d{2})?", v):
        return v  # HHMM or HHMMSS
    n = int_or_none(v)
    if n is not None:
        return str(n)
    return v.lower()


# -------------------------
# HTML builder
# -------------------------
def build_html(root: ET.Element, file_title: str) -> str:
    parent_map = build_parent_map(root)
    root_tag = localname(root.tag)
    cols = find_collections(root, parent_map)

    primary = choose_primary_collection(cols)

    # Header summary
    total_elements = sum(1 for _ in root.iter())
    all_tags = defaultdict(int)
    for e in root.iter():
        all_tags[localname(e.tag)] += 1
    top_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:8]

    # If we have Evento collection, make it primary (already preferred)
    if primary is None:
        # fallback: show whole XML as nested list
        return build_fallback_tree_html(root, file_title)

    # Build rows
    items = primary.items
    flat_rows = [flatten_item(it, max_depth=2) for it in items]
    keys_set = set()
    for r in flat_rows:
        keys_set.update(r.keys())
    keys = pick_display_columns(list(keys_set))
    # limit columns to keep readable (details will show everything)
    MAX_COLS = 14
    display_keys = keys[:MAX_COLS]

    # Build table rows + details blocks
    tbody = []
    details = []
    for i, (it, row) in enumerate(zip(items, flat_rows), start=1):
        # filter blob = concat values
        blob_parts = [str(i), primary.item_tag]
        for k in display_keys:
            blob_parts.append(row.get(k, ""))
        # also include attrs and some other keys
        for k, v in row.items():
            if v:
                blob_parts.append(v)
        filter_blob = " ".join(blob_parts).lower()

        tds = [f"<td data-sort='{i}'>{i}</td>"]
        for k in display_keys:
            v = row.get(k, "")
            shown = v
            # format date/time if looks like it
            if re.fullmatch(r"\d{8}", v):
                shown = fmt_date(v)
            elif re.fullmatch(r"\d{4}", v) or re.fullmatch(r"\d{6}", v):
                shown = fmt_time(v)
            tds.append(f"<td data-sort='{html.escape(make_sort_key(v))}'>{html.escape(shown)}</td>")

        tbody.append(
            f"<tr class='mainrow' data-filter='{html.escape(filter_blob)}' data-idx='{i}'>"
            + "".join(tds) +
            "</tr>"
        )

        # details: show key->value for all flattened keys + some raw subtree
        all_kv = []
        for k in keys:
            v = row.get(k, "")
            if v != "":
                all_kv.append((k, v))
        # pretty subtree for this item (limited depth)
        subtree_html = render_subtree(it, max_depth=3)

        details.append(f"""
        <details class="item" data-filter="{html.escape(filter_blob)}" data-idx="{i}">
          <summary>{html.escape(primary.item_tag)} #{i}</summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h4>Campi</h4>
                <table>
                  <thead><tr><th>Campo</th><th>Valore</th></tr></thead>
                  <tbody>
                    {''.join(f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v)}</td></tr>" for k,v in all_kv)}
                  </tbody>
                </table>
              </div>
              <div class="card2">
                <h4>Struttura (parziale)</h4>
                {subtree_html}
              </div>
            </div>
          </div>
        </details>
        """)

    # Build HTML doc
    def th(label: str, dtype: str) -> str:
        return f"<th class='sortable' data-type='{html.escape(dtype)}'>{html.escape(label)}</th>"

    # dtype heuristic for columns
    def dtype_for(k: str) -> str:
        lk = k.lower()
        if "data" in lk or "date" in lk:
            return "date"
        if "ora" in lk or "time" in lk:
            return "time"
        if "#count" in lk or "num" in lk or "quant" in lk:
            return "num"
        if k.startswith("@"):
            return "text"
        return "text"

    header_cols = "<tr>" + th("#", "num") + "".join(th(k, dtype_for(k)) for k in display_keys) + "</tr>"

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    h2{margin:0 0 8px 0;}
    h4{margin:0 0 8px 0;}
    .muted{color:#666;font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px;}
    .grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:12px;margin-top:10px;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;}
    .card2{border:1px solid #eee;border-radius:12px;padding:12px;background:#fff;}
    .search{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    table{border-collapse:collapse;width:100%;margin-top:10px;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;word-break:break-all;}
    ul{margin:8px 0 0 18px;}
    .pill{display:inline-block;margin-left:8px;padding:2px 8px;border-radius:999px;background:#f0f0f0;font-weight:700;font-size:12px;color:#333;}
    .tree{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;white-space:pre-wrap;background:#f7f7f7;border:1px solid #eee;border-radius:10px;padding:10px;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyFilter(){
      const q = norm(document.getElementById('q').value).trim();
      const rows = document.querySelectorAll('#tb tr.mainrow');
      const dets = document.querySelectorAll('details.item');

      if(!q){
        rows.forEach(r=>r.style.display="");
        dets.forEach(d=>d.style.display="");
        return;
      }

      rows.forEach(r=>{
        const hay = norm(r.getAttribute('data-filter'));
        r.style.display = hay.includes(q) ? "" : "none";
      });

      dets.forEach(d=>{
        const hay = norm(d.getAttribute('data-filter'));
        d.style.display = hay.includes(q) ? "" : "none";
      });
    }

    function clearSortStyles(table){
      table.querySelectorAll('th.sortable').forEach(th=>{
        th.classList.remove('sorted-asc','sorted-desc');
      });
    }

    function sortTableByCol(tableId, colIndex, type, asc){
      const table = document.getElementById(tableId);
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));

      const getKey = (tr) => {
        const td = tr.children[colIndex];
        if(!td) return "";
        return td.getAttribute('data-sort') || td.textContent || "";
      };

      const cmp = (a,b) => {
        const ka = getKey(a);
        const kb = getKey(b);
        if(type === 'num' || type === 'date' || type === 'time'){
          const na = parseFloat(ka) || 0;
          const nb = parseFloat(kb) || 0;
          return na - nb;
        }
        return ka.localeCompare(kb, undefined, {numeric:true, sensitivity:'base'});
      };

      rows.sort((a,b)=> asc ? cmp(a,b) : -cmp(a,b));
      rows.forEach(r=>tbody.appendChild(r));

      clearSortStyles(table);
      const ths = table.querySelectorAll('th.sortable');
      const th = ths[colIndex];
      if(th){
        th.classList.add(asc ? 'sorted-asc' : 'sorted-desc');
      }
    }

    function initSorting(){
      const table = document.getElementById('mainTable');
      const ths = table.querySelectorAll('th.sortable');
      ths.forEach((th, idx) => {
        th.addEventListener('click', () => {
          const type = th.getAttribute('data-type') || 'text';
          const isAsc = !th.classList.contains('sorted-asc');
          sortTableByCol('mainTable', idx, type, isAsc);
        });
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('input', applyFilter);
      initSorting();
    });
    """

    summary = f"""
    <h1>LTA Reader</h1>
    <div class="muted">{html.escape(file_title)} — root: <code>{html.escape(root_tag)}</code></div>

    <div class="grid">
      <div class="card">
        <h2>Struttura</h2>
        <ul>
          <li><b>Elementi totali</b>: {total_elements}</li>
          <li><b>Collezione principale</b>: <code>{html.escape(primary.parent_path)}/{html.escape(primary.item_tag)}</code> ({len(items)} righe)</li>
        </ul>
      </div>
      <div class="card">
        <h2>Tag più presenti</h2>
        <ul>
          {''.join(f"<li><code>{html.escape(k)}</code>: {v}</li>" for k,v in top_tags)}
        </ul>
      </div>
    </div>
    """

    main = f"""
    <div class="card" style="margin-top:12px;">
      <h2>Tabella: {html.escape(primary.item_tag)} ({len(items)})</h2>
      <input id="q" class="search" placeholder="Filtra per qualunque campo..." />
      <div class="tablewrap">
        <table id="mainTable">
          <thead>{header_cols}</thead>
          <tbody id="tb">
            {''.join(tbody)}
          </tbody>
        </table>
      </div>

      <h3>Dettaglio</h3>
      {''.join(details)}
    </div>
    """

    return f"<!doctype html><html><head><meta charset='utf-8'><title>LTA Reader</title><style>{css}</style></head><body>{summary}{main}<script>{js}</script></body></html>"


def render_subtree(elem: ET.Element, max_depth: int = 3) -> str:
    """
    Rende una vista testuale del sottoalbero (limitata).
    """
    lines: List[str] = []

    def rec(e: ET.Element, depth: int):
        if depth > max_depth:
            return
        name = localname(e.tag)
        attrs = " ".join([f"{k}='{v}'" for k,v in (e.attrib or {}).items()])
        head = name + ((" " + attrs) if attrs else "")
        txt = (e.text or "").strip()
        if txt and len(txt) > 80:
            txt = txt[:77] + "…"
        if txt:
            head += f": {txt}"
        lines.append(("  " * depth) + head)

        kids = list(e)
        if kids:
            # limit children shown if enormous
            for c in kids[:50]:
                rec(c, depth + 1)
            if len(kids) > 50:
                lines.append(("  " * (depth + 1)) + f"… ({len(kids)-50} altri)")
    rec(elem, 0)
    return f"<div class='tree'>{html.escape('\\n'.join(lines))}</div>"


def build_fallback_tree_html(root: ET.Element, file_title: str) -> str:
    root_tag = localname(root.tag)
    tree = render_subtree(root, max_depth=6)
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>LTA Reader</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;}}
.muted{{color:#666;font-size:13px;}}
</style>
</head><body>
<h1>LTA Reader</h1>
<div class="muted">{html.escape(file_title)} — root: <code>{html.escape(root_tag)}</code></div>
<h2>Vista struttura</h2>
{tree}
</body></html>
"""


# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="LTA Reader: genera un report HTML (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File LTA .xml/.xsi oppure firmati .p7m")
    ap.add_argument("--open", action="store_true", help="Apri il report nel browser a fine generazione")
    args = ap.parse_args()

    for in_path in args.files:
        p = pathlib.Path(in_path)
        if not p.exists():
            print(f"SKIP: non trovato: {in_path}", file=sys.stderr)
            continue

        actual_xml_path = str(p)
        temp_to_cleanup = None

        if p.name.lower().endswith(".p7m"):
            temp_to_cleanup = extract_p7m_to_temp_xml(str(p))
            actual_xml_path = temp_to_cleanup

        try:
            root = ET.parse(actual_xml_path).getroot()
        except Exception as e:
            print(f"FAIL parsing XML: {in_path} -> {e}", file=sys.stderr)
            if temp_to_cleanup:
                try: os.unlink(temp_to_cleanup)
                except: pass
            continue

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".lta.html"))

        html_doc = build_html(root, p.name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_doc)

        print(f"OK: {in_path} -> {out_path}")

        if args.open:
            open_in_browser(out_path)

        if temp_to_cleanup:
            try:
                os.unlink(temp_to_cleanup)
            except Exception:
                pass


if __name__ == "__main__":
    main()


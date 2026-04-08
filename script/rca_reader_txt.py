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
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple


# =========================
# Helpers
# =========================
def hattr(s: str) -> str:
    return html.escape(s or "", quote=True)

def esc(s: str) -> str:
    return html.escape(s or "", quote=False)

def fmt_date8(yyyymmdd: str) -> str:
    s = (yyyymmdd or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[6:8]}/{s[4:6]}/{s[0:4]}"
    return s

def fmt_time4(hhmm: str) -> str:
    s = (hhmm or "").strip()
    if len(s) == 4 and s.isdigit():
        return f"{s[:2]}:{s[2:]}"
    return s

def fmt_time6(hhmmss: str) -> str:
    s = (hhmmss or "").strip()
    if len(s) == 6 and s.isdigit():
        return f"{s[:2]}:{s[2:4]}:{s[4:]}"
    return s

def int_or0(s: str) -> int:
    s = (s or "").strip()
    return int(s) if s.isdigit() else 0

def slice1(s: str, pos: int, ln: int) -> str:
    # 1-based positions
    return s[pos - 1 : pos - 1 + ln]


# =========================
# Optional: P7M extraction (if RCA is signed)
# =========================
def looks_pem(path: str) -> bool:
    with open(path, "rb") as f:
        head = f.read(64)
    return b"-----BEGIN" in head

def extract_p7m_to_temp_file(p7m_path: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp_path = tmp.name
    tmp.close()

    inform = "PEM" if looks_pem(p7m_path) else "DER"

    # openssl cms
    try:
        subprocess.run(
            ["openssl", "cms", "-verify", "-noverify", "-inform", inform, "-in", p7m_path, "-out", tmp_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return tmp_path
    except Exception:
        pass

    # macOS security cms -D
    try:
        with open(tmp_path, "wb") as out:
            subprocess.run(
                ["/usr/bin/security", "cms", "-D", "-i", p7m_path],
                check=True, stdout=out, stderr=subprocess.DEVNULL
            )
        return tmp_path
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise RuntimeError("Impossibile estrarre payload dal .p7m (openssl e security falliti).")


# =========================
# Read + split records
# =========================
def read_text(path: str) -> str:
    try:
        return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return pathlib.Path(path).read_text(encoding="cp1252", errors="replace")

def split_records(content: str) -> List[str]:
    # provvedimento: record delimitati da '&' (anche all'inizio e alla fine) :contentReference[oaicite:9]{index=9}
    if "&" in content:
        flat = content.replace("\r", "").replace("\n", "")
        parts = [p.strip() for p in flat.split("&") if p.strip()]
        return parts
    # fallback: line-based
    return [ln.strip("\r\n") for ln in content.splitlines() if ln.strip()]


# =========================
# RCA record parsers
# =========================

# Record 01: Anagrafica evento (posizioni dal provvedimento) :contentReference[oaicite:10]{index=10}
FIELDS_01: List[Tuple[str, int, int]] = [
    ("TipoRecord", 1, 2),
    ("CFTitolareCA", 3, 16),
    ("DenomTitolareCA", 19, 30),
    ("SistemaCA", 49, 8),
    ("CFOrganizzatore", 57, 16),
    ("DenomOrganizzatore", 73, 30),
    ("TipologiaOrganizzatore", 103, 1),
    ("SpettacoloIntrattenimento", 104, 1),
    ("IncidenzaIntrattenimento", 105, 3),
    ("DenomLocale", 108, 30),
    ("CodiceLocale", 138, 13),
    ("DataInizioEvento", 151, 8),
    ("OraInizioEvento", 159, 4),
    ("TipoEvento", 163, 2),
    ("TitoloEvento", 165, 40),
    ("Autore", 205, 30),
    ("Esecutore", 235, 40),
    ("NazionalitaFilm", 275, 4),
    ("NumeroOpereRappresentate", 279, 3),
]

# Record 14: Riepilogo titoli (parte fissa) :contentReference[oaicite:11]{index=11}
FIXED_14_15: List[Tuple[str, int, int]] = [
    ("TipoRecord", 1, 2),
    ("SistemaCA", 3, 8),
    ("CFTitolareCA", 11, 16),
    ("CFOrganizzatore", 27, 16),
    ("CFTitolareEmissione", 43, 16),
    ("SistemaEmissione", 59, 8),
    ("CodiceLocale", 67, 13),
    ("DataInizioEvento", 80, 8),
    ("OraInizioEvento", 88, 4),
    ("OrdinePosto", 92, 2),
    ("Capienza", 94, 7),
    ("OccorrenzeTipiTitolo", 101, 2),
]
GROUP_LEN = 107  # 2 + (15 * 7)

STATUS_ORDER = [
    "TotaleLTA",  # VT+VD+ZT+ZD+MT+MD+AT+AD+DT+DD+FT+FD+BT+BD :contentReference[oaicite:12]{index=12}
    "VT", "VD", "ZT", "ZD", "MT", "MD", "AT", "AD", "DT", "DD", "FT", "FD", "BT", "BD"
]

STATUS_LABELS = {
    "VT": "Valido (tradizionale)",
    "VD": "Valido (digitale)",
    "ZT": "Accesso automatizzato (tradizionale)",
    "ZD": "Accesso automatizzato (digitale)",
    "MT": "Accesso manuale (tradizionale)",
    "MD": "Accesso manuale (digitale)",
    "AT": "Annullato (tradizionale)",
    "AD": "Annullato (digitale)",
    "DT": "Daspato (tradizionale)",
    "DD": "Daspato (digitale)",
    "FT": "Denuncia furto (tradizionale)",
    "FD": "Denuncia furto (digitale)",
    "BT": "Black list (tradizionale)",
    "BD": "Black list (digitale)",
}

STATUS_LEGEND_ORDER = STATUS_ORDER[1:]

def parse_record_01(rec: str) -> Dict[str, str]:
    d: Dict[str, str] = {"Raw": rec}
    for name, pos, ln in FIELDS_01:
        d[name] = slice1(rec, pos, ln).rstrip()  # alfanumerici riempiti blank
    return d

def parse_record_14_15(rec: str) -> Dict[str, object]:
    d: Dict[str, object] = {"Raw": rec}
    for name, pos, ln in FIXED_14_15:
        d[name] = slice1(rec, pos, ln).strip()
    occ = int_or0(str(d.get("OccorrenzeTipiTitolo", "0")))
    groups: List[Dict[str, object]] = []

    base0 = 102  # 1..102 fissi, gruppi da pos 103
    for i in range(occ):
        start = base0 + i * GROUP_LEN
        chunk = rec[start : start + GROUP_LEN]
        if len(chunk) < GROUP_LEN:
            break
        tipo_tit = chunk[0:2].strip()
        nums = [chunk[2 + j * 7 : 2 + (j + 1) * 7] for j in range(15)]
        g: Dict[str, object] = {"TipoTitolo": tipo_tit}
        for j, key in enumerate(STATUS_ORDER):
            g[key] = int_or0(nums[j])
        groups.append(g)

    d["Gruppi"] = groups

    # Totali di riga (somma gruppi)
    totals = {k: 0 for k in STATUS_ORDER}
    for g in groups:
        for k in STATUS_ORDER:
            totals[k] += int(g.get(k, 0))
    d["Totali"] = totals

    return d

# Record S: sostituzione (se presente) :contentReference[oaicite:13]{index=13}
FIELDS_S: List[Tuple[str, int, int]] = [
    ("TipoRecord", 1, 2),
    ("CFTitolareCA", 3, 16),
    ("SistemaCA", 19, 8),
    ("TipoRiepilogoSostituito", 27, 1),
    ("CFOrganizzatore", 28, 16),
    ("CodiceLocale", 44, 13),
    ("DataInizioEvento", 57, 8),
    ("OraInizioEvento", 65, 4),
]
def parse_record_S(rec: str) -> Dict[str, str]:
    d: Dict[str, str] = {"Raw": rec}
    for name, pos, ln in FIELDS_S:
        d[name] = slice1(rec, pos, ln).strip()
    return d

# Record H: record di testa (layout coerente con il tuo esempio RCA TXT)
# (nel testo estratto dal PDF la tabella completa è troncata, ma questo parse combacia sul tuo file)
FIELDS_H: List[Tuple[str, int, int]] = [
    ("TipoRecord", 1, 2),
    ("CFTitolareCA", 3, 16),
    ("DenomTitolareCA", 19, 30),
    ("SistemaCA", 49, 8),
    ("TipoRiepilogo", 57, 1),
    ("DataRiepilogo", 58, 8),
    ("DataGenerazione", 66, 8),
    ("OraGenerazione", 74, 6),
    ("ProgressivoGenerazione", 80, 8),
    ("Versione", 88, 5),
]
def parse_record_H(rec: str) -> Dict[str, str]:
    d: Dict[str, str] = {"Raw": rec}
    for name, pos, ln in FIELDS_H:
        d[name] = slice1(rec, pos, ln).rstrip()
    return d


# =========================
# HTML builder (filter + sorting + details)
# =========================
def th(label: str, dtype: str) -> str:
    return f"<th class=\"sortable\" data-type=\"{hattr(dtype)}\">{esc(label)}</th>"

def td(val: str, sort_key: Optional[str] = None) -> str:
    safe = esc(val)
    sk = sort_key if sort_key is not None else safe.strip().lower()
    return f"<td data-sort=\"{hattr(sk)}\">{safe}</td>"

def build_html(filename: str,
               head: Optional[Dict[str, str]],
               sost: Optional[Dict[str, str]],
               events: Dict[str, Dict[str, str]],
               rec14: List[Dict[str, object]],
               rec15: List[Dict[str, object]]) -> str:

    # Totali globali per 14/15
    def sum_totals(recs: List[Dict[str, object]]) -> Dict[str, int]:
        out = {k: 0 for k in STATUS_ORDER}
        for r in recs:
            t = r.get("Totali", {})
            if isinstance(t, dict):
                for k in STATUS_ORDER:
                    out[k] += int(t.get(k, 0))
        return out

    tot14 = sum_totals(rec14)
    tot15 = sum_totals(rec15)

    # counts
    n_events = len(events)
    n14 = len(rec14)
    n15 = len(rec15)

    # helper to build record key to join with event
    def evkey(cf_org: str, codloc: str, d: str, o: str) -> str:
        return f"{cf_org.strip()}|{codloc.strip()}|{d.strip()}|{o.strip()}"

    # Top summary
    head_block = "<div class='muted'>Nessun record H trovato</div>"
    if head:
        head_block = f"""
        <table class="kv"><tbody>
          <tr><td><b>CFTitolareCA</b></td><td>{esc(head.get("CFTitolareCA","").strip())}</td></tr>
          <tr><td><b>Denominazione</b></td><td>{esc(head.get("DenomTitolareCA","").strip())}</td></tr>
          <tr><td><b>SistemaCA</b></td><td>{esc(head.get("SistemaCA","").strip())}</td></tr>
          <tr><td><b>Tipo riepilogo</b></td><td>{esc(head.get("TipoRiepilogo","").strip())}</td></tr>
          <tr><td><b>Data riepilogo</b></td><td>{esc(fmt_date8(head.get("DataRiepilogo","").strip()))}</td></tr>
          <tr><td><b>Generazione</b></td><td>{esc(fmt_date8(head.get("DataGenerazione","").strip()))} {esc(fmt_time6(head.get("OraGenerazione","").strip()))}</td></tr>
          <tr><td><b>Progressivo</b></td><td>{esc(head.get("ProgressivoGenerazione","").strip())}</td></tr>
          <tr><td><b>Versione</b></td><td>{esc(head.get("Versione","").strip())}</td></tr>
        </tbody></table>
        """

    sost_block = ""
    if sost:
        sost_block = f"""
        <div class="card">
          <h3>Sostituzione (record S)</h3>
          <table class="kv"><tbody>
            <tr><td><b>CFTitolareCA</b></td><td>{esc(sost.get("CFTitolareCA",""))}</td></tr>
            <tr><td><b>SistemaCA</b></td><td>{esc(sost.get("SistemaCA",""))}</td></tr>
            <tr><td><b>Tipo riepilogo sostituito</b></td><td>{esc(sost.get("TipoRiepilogoSostituito",""))}</td></tr>
            <tr><td><b>Evento sostituito</b></td><td>{esc(sost.get("CFOrganizzatore",""))} / {esc(sost.get("CodiceLocale",""))} / {esc(fmt_date8(sost.get("DataInizioEvento","")))} {esc(fmt_time4(sost.get("OraInizioEvento","")))}</td></tr>
          </tbody></table>
        </div>
        """

    # Build Event table
    ev_rows = []
    for k, e in events.items():
        ev_rows.append([
            fmt_date8(e.get("DataInizioEvento","").strip()),
            fmt_time4(e.get("OraInizioEvento","").strip()),
            e.get("CodiceLocale","").strip(),
            e.get("DenomLocale","").strip(),
            e.get("TitoloEvento","").strip(),
            e.get("CFOrganizzatore","").strip(),
            e.get("DenomOrganizzatore","").strip(),
            e.get("TipoEvento","").strip(),
            e.get("TipologiaOrganizzatore","").strip(),
        ])

    ev_table = ""
    if ev_rows:
        trs = []
        for i, r in enumerate(ev_rows, start=1):
            filter_blob = " ".join(r).lower()
            trs.append(
                f"<tr class='row' data-filter=\"{hattr(filter_blob)}\">"
                + td(str(i), str(i))
                + td(r[0], r[0].replace("/",""))
                + td(r[1], r[1].replace(":",""))
                + td(r[2], r[2])
                + td(r[3], r[3].lower())
                + td(r[4], r[4].lower())
                + td(r[5], r[5])
                + td(r[6], r[6].lower())
                + td(r[7], r[7])
                + td(r[8], r[8])
                + "</tr>"
            )

        ev_table = f"""
        <div class="card">
          <h2>Eventi (record 01)</h2>
          <div class="tablewrap">
            <table id="t_events">
              <thead><tr>
                {th("#","num")}
                {th("Data","date")}
                {th("Ora","time")}
                {th("CodiceLocale","text")}
                {th("Locale","text")}
                {th("Titolo","text")}
                {th("CF Org","text")}
                {th("Organizzatore","text")}
                {th("Tipo evento","text")}
                {th("Tip. Org","text")}
              </tr></thead>
              <tbody>
                {''.join(trs)}
              </tbody>
            </table>
          </div>
        </div>
        """

    def build_riepilogo_table(table_id: str, title: str, recs: List[Dict[str, object]], totals: Dict[str,int]) -> str:
        if not recs:
            return f"<div class='card'><h2>{esc(title)}</h2><div class='muted'>Nessun record</div></div>"

        # main rows
        trs = []
        details = []
        for idx, r in enumerate(recs, start=1):
            cf_org = str(r.get("CFOrganizzatore","")).strip()
            codloc = str(r.get("CodiceLocale","")).strip()
            d = str(r.get("DataInizioEvento","")).strip()
            o = str(r.get("OraInizioEvento","")).strip()

            k = evkey(cf_org, codloc, d, o)
            ev = events.get(k, {})

            sistema_em = str(r.get("SistemaEmissione","")).strip()
            ordine = str(r.get("OrdinePosto","")).strip()
            cap = str(r.get("Capienza","")).strip()
            occ = str(r.get("OccorrenzeTipiTitolo","")).strip()

            t = r.get("Totali", {})
            tot_lta = int(t.get("TotaleLTA", 0)) if isinstance(t, dict) else 0

            # per filtro: include anche valori evento + emissione + ordine
            fparts = [
                title, fmt_date8(d), fmt_time4(o), codloc,
                ev.get("TitoloEvento",""), ev.get("DenomLocale",""),
                cf_org, sistema_em, ordine, cap, str(tot_lta)
            ] + [str(t.get(k2,0)) for k2 in STATUS_ORDER]  # include counts
            filter_blob = " ".join([str(x).strip() for x in fparts if str(x).strip()]).lower()

            trs.append(
                f"<tr class='row' data-filter=\"{hattr(filter_blob)}\" data-idx=\"{idx}\">"
                + td(str(idx), str(idx))
                + td(fmt_date8(d), d)
                + td(fmt_time4(o), o)
                + td(codloc, codloc)
                + td(ev.get("TitoloEvento","").strip(), ev.get("TitoloEvento","").strip().lower())
                + td(sistema_em, sistema_em.lower())
                + td(ordine, ordine.lower())
                + td(cap, cap)
                + td(occ, occ)
                + td(str(tot_lta), str(tot_lta))
                + td(str(t.get("VT",0)), str(t.get("VT",0)))
                + td(str(t.get("VD",0)), str(t.get("VD",0)))
                + td(str(t.get("ZT",0)), str(t.get("ZT",0)))
                + td(str(t.get("ZD",0)), str(t.get("ZD",0)))
                + td(str(t.get("MT",0)), str(t.get("MT",0)))
                + td(str(t.get("MD",0)), str(t.get("MD",0)))
                + td(str(t.get("AT",0)), str(t.get("AT",0)))
                + td(str(t.get("AD",0)), str(t.get("AD",0)))
                + td(str(t.get("DT",0)), str(t.get("DT",0)))
                + td(str(t.get("DD",0)), str(t.get("DD",0)))
                + td(str(t.get("FT",0)), str(t.get("FT",0)))
                + td(str(t.get("FD",0)), str(t.get("FD",0)))
                + td(str(t.get("BT",0)), str(t.get("BT",0)))
                + td(str(t.get("BD",0)), str(t.get("BD",0)))
                + "</tr>"
            )

            # details breakdown per tipo titolo
            groups = r.get("Gruppi", [])
            gtrs = []
            if isinstance(groups, list) and groups:
                for g in groups:
                    gtrs.append(
                        "<tr>"
                        + f"<td>{esc(str(g.get('TipoTitolo','')))}</td>"
                        + "".join(f"<td>{esc(str(g.get(k2,0)))}</td>" for k2 in STATUS_ORDER)
                        + "</tr>"
                    )
            else:
                gtrs.append("<tr><td colspan='16' class='muted'>Nessun gruppo</td></tr>")

            details.append(f"""
            <details class="det" data-filter="{hattr(filter_blob)}">
              <summary>{esc(title)} — {esc(fmt_date8(d))} {esc(fmt_time4(o))} — {esc(codloc)} — {esc(sistema_em)} — {esc(ordine)} (cap {esc(cap)})</summary>
              <div class="pad">
                <div class="muted">Evento: {esc(ev.get("TitoloEvento","").strip())} — {esc(ev.get("DenomLocale","").strip())}</div>
                <h4>Dettaglio per TipoTitolo (gruppo ripetuto “Occorrenze tipi-titolo”)</h4>
                <div class="tablewrap small">
                  <table>
                    <thead>
                      <tr>
                        <th>TipoTitolo</th>
                        {''.join(f"<th>{k2}</th>" for k2 in STATUS_ORDER)}
                      </tr>
                    </thead>
                    <tbody>{''.join(gtrs)}</tbody>
                  </table>
                </div>
                <h4>Raw</h4>
                <pre class="raw">{esc(str(r.get("Raw","")))}</pre>
              </div>
            </details>
            """)

        # Totals row for whole table
        tot_row = (
            "<tr class='tot'>"
            "<td colspan='9'><b>Totali</b></td>"
            + f"<td><b>{totals['TotaleLTA']}</b></td>"
            + "".join(f"<td><b>{totals[k2]}</b></td>" for k2 in STATUS_ORDER[1:])
            + "</tr>"
        )

        return f"""
        <div class="card">
          <h2>{esc(title)}</h2>
          <div class="tablewrap">
            <table id="{hattr(table_id)}">
              <thead><tr>
                {th("#","num")}
                {th("Data","date")}
                {th("Ora","time")}
                {th("CodiceLocale","text")}
                {th("Titolo evento","text")}
                {th("SistemaEmiss.","text")}
                {th("Ord","text")}
                {th("Capienza","num")}
                {th("Occ","num")}
                {th("TotLTA","num")}
                {th("VT","num")}{th("VD","num")}{th("ZT","num")}{th("ZD","num")}
                {th("MT","num")}{th("MD","num")}{th("AT","num")}{th("AD","num")}
                {th("DT","num")}{th("DD","num")}{th("FT","num")}{th("FD","num")}
                {th("BT","num")}{th("BD","num")}
              </tr></thead>
              <tbody>
                {''.join(trs)}
                {tot_row}
              </tbody>
            </table>
          </div>
          <h3>Dettaglio</h3>
          {''.join(details)}
        </div>
        """

    titoli_block = build_riepilogo_table("t_14", "Riepilogo Titoli (record 14)", rec14, tot14)
    abb_block = build_riepilogo_table("t_15", "Riepilogo Abbonamenti (record 15)", rec15, tot15)

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    h2{margin:0 0 10px 0;}
    h3{margin:14px 0 8px 0;}
    h4{margin:12px 0 6px 0;}
    .muted{color:#666;font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;margin-top:12px;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;margin-top:12px;}
    input{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    .status{color:#666;font-size:12px;margin-top:-4px;margin-bottom:8px;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    .tablewrap.small{max-height:35vh;}
    table{border-collapse:collapse;width:100%;font-size:12.5px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    pre.raw{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid #eee;border-radius:10px;padding:10px;}
    table.kv td{white-space:normal;}
    table.kv td:first-child{width:220px;}
    tr.tot td{background:#fafafa;font-weight:700;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyFilter(){
      const qraw = norm(document.getElementById('q').value).trim();
      const toks = qraw.split(/\\s+/).filter(Boolean);

      const els = document.querySelectorAll('[data-filter]');
      let shown = 0, rows = 0;

      const match = (el) => {
        const hay = norm(el.getAttribute('data-filter'));
        for(const t of toks){
          if(!hay.includes(t)) return false;
        }
        return true;
      };

      els.forEach(el=>{
        const ok = match(el);
        // table rows and details both
        el.style.display = ok ? "" : "none";
        if(el.tagName === 'TR'){ rows++; if(ok) shown++; }
      });

      const st = document.getElementById('status');
      if(st){
        st.textContent = toks.length ? `Righe mostrate: ${shown} / ${rows}` : `Righe totali: ${rows}`;
      }
    }

    function clearSortStyles(table){
      table.querySelectorAll('th.sortable').forEach(th=>{
        th.classList.remove('sorted-asc','sorted-desc');
      });
    }

    function sortTableByCol(table, colIndex, type, asc){
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr')).filter(r=>!r.classList.contains('tot'));

      const getKey = (tr) => {
        const td = tr.children[colIndex];
        if(!td) return "";
        return td.getAttribute('data-sort') || td.textContent || "";
      };

      const cmp = (a,b) => {
        const ka = getKey(a);
        const kb = getKey(b);
        if(['num','date','time'].includes(type)){
          const na = parseFloat(ka) || 0;
          const nb = parseFloat(kb) || 0;
          return na - nb;
        }
        return ka.localeCompare(kb, undefined, {numeric:true, sensitivity:'base'});
      };

      rows.sort((a,b)=> asc ? cmp(a,b) : -cmp(a,b));
      rows.forEach(r=>tbody.appendChild(r));

      // keep totals row at end
      const tot = tbody.querySelector('tr.tot');
      if(tot) tbody.appendChild(tot);

      clearSortStyles(table);
      const ths = table.querySelectorAll('th.sortable');
      const th = ths[colIndex];
      if(th) th.classList.add(asc ? 'sorted-asc' : 'sorted-desc');
    }

    function initSorting(){
      document.querySelectorAll('table').forEach(table=>{
        const ths = table.querySelectorAll('th.sortable');
        ths.forEach((th, idx) => {
          th.addEventListener('click', () => {
            const type = th.getAttribute('data-type') || 'text';
            const isAsc = !th.classList.contains('sorted-asc');
            sortTableByCol(table, idx, type, isAsc);
          });
        });
      });
    }

    function init(){
      const q = document.getElementById('q');
      q.addEventListener('input', applyFilter);
      initSorting();
      applyFilter();
    }

    if(document.readyState === 'loading'){
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
    """

    legend_rows = "".join(
        f"<tr><td><code>{esc(code)}</code></td><td>{esc(STATUS_LABELS[code])}</td></tr>"
        for code in STATUS_LEGEND_ORDER
    )
    legend_block = f"""
  <div class="card">
    <h3>Legenda stati</h3>
    <div class="muted">T = tradizionale, D = digitale. TotLTA = somma di VT, VD, ZT, ZD, MT, MD, AT, AD, DT, DD, FT, FD, BT, BD.</div>
    <div class="tablewrap" style="margin-top:10px;">
      <table class="kv">
        <thead><tr><th>Codice</th><th>Significato</th></tr></thead>
        <tbody>{legend_rows}</tbody>
      </table>
    </div>
  </div>
"""

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>RCA Reader</title>
<style>{css}</style>
</head>
<body>
  <h1>RCA Reader (TXT)</h1>
  <div class="muted">{esc(filename)}</div>

  <div class="grid">
    <div class="card">
      <h3>Testa (record H)</h3>
      {head_block}
    </div>
    <div class="card">
      <h3>Riepilogo</h3>
      <table class="kv"><tbody>
        <tr><td><b>Eventi</b></td><td>{n_events}</td></tr>
        <tr><td><b>Record 14</b></td><td>{n14}</td></tr>
        <tr><td><b>Record 15</b></td><td>{n15}</td></tr>
      </tbody></table>
      <div class="muted" style="margin-top:8px;">Nota: i record 14/15 hanno lunghezza variabile in base alle “Occorrenze tipi-titolo”.</div>
    </div>
  </div>

  {sost_block}

  <input id="q" placeholder="Cerca (es: 25/02/2026 P0002267 TN CALCIO VT 3 …)" />
  <div id="status" class="status"></div>

  {ev_table}
  {titoli_block}
  {abb_block}
  {legend_block}

<script>{js}</script>
</body>
</html>
"""


# =========================
# Main
# =========================
def strip_ext_for_output(name: str) -> str:
    low = name.lower()
    if low.endswith(".p7m"):
        name = name[:-4]
        low = name.lower()
    for ext in (".txt", ".rca"):
        if low.endswith(ext):
            name = name[: -len(ext)]
            low = name.lower()
    return name

def open_in_browser(path: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", path], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", path], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore

def main():
    ap = argparse.ArgumentParser(description="RCA TXT Reader (HTML viewer con ricerca + sorting).")
    ap.add_argument("files", nargs="+", help="File RCA .txt (o .p7m se firmato)")
    ap.add_argument("--open", action="store_true", help="Apri il report nel browser")
    args = ap.parse_args()

    for in_path in args.files:
        p = pathlib.Path(in_path)
        if not p.exists():
            print(f"SKIP: non trovato: {in_path}", file=sys.stderr)
            continue

        actual_path = str(p)
        temp_to_cleanup = None

        if p.name.lower().endswith(".p7m"):
            temp_to_cleanup = extract_p7m_to_temp_file(str(p))
            actual_path = temp_to_cleanup

        content = read_text(actual_path)
        recs = split_records(content)

        head = None
        sost = None
        events: Dict[str, Dict[str, str]] = {}
        rec14: List[Dict[str, object]] = []
        rec15: List[Dict[str, object]] = []

        def evkey(cf_org: str, codloc: str, d: str, o: str) -> str:
            return f"{cf_org.strip()}|{codloc.strip()}|{d.strip()}|{o.strip()}"

        for rec in recs:
            if len(rec) < 2:
                continue
            rtype = rec[0:2].strip()
            if rtype == "H":
                head = parse_record_H(rec)
            elif rtype == "S":
                sost = parse_record_S(rec)
            elif rtype == "01":
                e = parse_record_01(rec)
                k = evkey(e.get("CFOrganizzatore",""), e.get("CodiceLocale",""),
                          e.get("DataInizioEvento",""), e.get("OraInizioEvento",""))
                events[k] = e
            elif rtype == "14":
                rec14.append(parse_record_14_15(rec))
            elif rtype == "15":
                rec15.append(parse_record_14_15(rec))
            else:
                # record ignoto: lo si potrebbe collezionare in una sezione "raw"
                pass

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".rca.html"))

        html_doc = build_html(p.name, head, sost, events, rec14, rec15)
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

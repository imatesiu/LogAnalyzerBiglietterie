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
from typing import Optional, List, Dict, Tuple

# -------------------------
# XML helpers (namespace-safe)
# -------------------------
def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag and "}" in tag else (tag or "")

def child(elem: Optional[ET.Element], name: str) -> Optional[ET.Element]:
    if elem is None:
        return None
    for c in list(elem):
        if localname(c.tag) == name:
            return c
    return None

def children(elem: Optional[ET.Element], name: str) -> List[ET.Element]:
    if elem is None:
        return []
    return [c for c in list(elem) if localname(c.tag) == name]

def text_of(elem: Optional[ET.Element], default: str = "") -> str:
    if elem is None or elem.text is None:
        return default
    return elem.text.strip()

def text_path(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    cur = elem
    for part in path.split("/"):
        cur = child(cur, part)
        if cur is None:
            return default
    return text_of(cur, default)

def int_or0(s: str) -> int:
    s = (s or "").strip()
    if not re.fullmatch(r"-?\d+", s):
        return 0
    return int(s)

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
# Accessi fields (da accessi.xsd)
# -------------------------
TITOLI_FIELDS = [
    ("LTA", "TotaleTitoliLTA"),
    ("NoAcc T", "TotaleTitoliNoAccessoTradiz"),
    ("NoAcc D", "TotaleTitoliNoAccessoDigitali"),
    ("Auto T", "TotaleTitoliAutomatizzatiTradiz"),
    ("Auto D", "TotaleTitoliAutomatizzatiDigitali"),
    ("Man T", "TotaleTitoliManualiTradiz"),
    ("Man D", "TotaleTitoliManualiDigitali"),
    ("Ann T", "TotaleTitoliAnnullatiTradiz"),
    ("Ann D", "TotaleTitoliAnnullatiDigitali"),
    ("Dasp T", "TotaleTitoliDaspatiTradiz"),
    ("Dasp D", "TotaleTitoliDaspatiDigitali"),
    ("Rub T", "TotaleTitoliRubatiTradiz"),
    ("Rub D", "TotaleTitoliRubatiDigitali"),
    ("BL T", "TotaleTitoliBLTradiz"),
    ("BL D", "TotaleTitoliBLDigitali"),
]

ABB_FIELDS = [
    ("LTA", "TotaleTitoliAbbLTA"),
    ("NoAcc T", "TotaleTitoliAbbNoAccessoTradiz"),
    ("NoAcc D", "TotaleTitoliAbbNoAccessoDigitali"),
    ("Auto T", "TotaleTitoliAbbAutomatizzatiTradiz"),
    ("Auto D", "TotaleTitoliAbbAutomatizzatiDigitali"),
    ("Man T", "TotaleTitoliAbbManualiTradiz"),
    ("Man D", "TotaleTitoliAbbManualiDigitali"),
    ("Ann T", "TotaleTitoliAbbAnnullatiTradiz"),
    ("Ann D", "TotaleTitoliAbbAnnullatiDigitali"),
    ("Dasp T", "TotaleTitoliAbbDaspatiTradiz"),
    ("Dasp D", "TotaleTitoliAbbDaspatiDigitali"),
    ("Rub T", "TotaleTitoliAbbRubatiTradiz"),
    ("Rub D", "TotaleTitoliAbbRubatiDigitali"),
    ("BL T", "TotaleTitoliAbbBLTradiz"),
    ("BL D", "TotaleTitoliAbbBLDigitali"),
]

# -------------------------
# Aggregations
# -------------------------
def sum_fields(tt: ET.Element, fields: List[Tuple[str, str]]) -> int:
    return sum(int_or0(text_path(tt, xml_name, "0")) for _, xml_name in fields)

def aggregate_event(event_el: ET.Element) -> Dict[str, int]:
    """
    Ritorna totali aggregati (titoli + abbonamenti) per categorie principali.
    """
    agg = {
        "LTA": 0,
        "NoAccesso": 0,
        "Automatizzati": 0,
        "Manuali": 0,
        "Annullati": 0,
        "Daspati": 0,
        "Rubati": 0,
        "BL": 0,
        "Totale": 0,
    }

    for sys_el in children(event_el, "SistemaEmissione"):
        # Titoli
        for tit_block in children(sys_el, "Titoli"):
            for tt in children(tit_block, "TotaleTipoTitolo"):
                lta = int_or0(text_path(tt, "TotaleTitoliLTA", "0"))
                noacc = int_or0(text_path(tt, "TotaleTitoliNoAccessoTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliNoAccessoDigitali", "0"))
                auto = int_or0(text_path(tt, "TotaleTitoliAutomatizzatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAutomatizzatiDigitali", "0"))
                man  = int_or0(text_path(tt, "TotaleTitoliManualiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliManualiDigitali", "0"))
                ann  = int_or0(text_path(tt, "TotaleTitoliAnnullatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAnnullatiDigitali", "0"))
                dasp = int_or0(text_path(tt, "TotaleTitoliDaspatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliDaspatiDigitali", "0"))
                rub  = int_or0(text_path(tt, "TotaleTitoliRubatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliRubatiDigitali", "0"))
                bl   = int_or0(text_path(tt, "TotaleTitoliBLTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliBLDigitali", "0"))

                agg["LTA"] += lta
                agg["NoAccesso"] += noacc
                agg["Automatizzati"] += auto
                agg["Manuali"] += man
                agg["Annullati"] += ann
                agg["Daspati"] += dasp
                agg["Rubati"] += rub
                agg["BL"] += bl

        # Abbonamenti
        for abb_block in children(sys_el, "Abbonamenti"):
            for tt in children(abb_block, "TotaleTipoTitoloAbbonamento"):
                lta = int_or0(text_path(tt, "TotaleTitoliAbbLTA", "0"))
                noacc = int_or0(text_path(tt, "TotaleTitoliAbbNoAccessoTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbNoAccessoDigitali", "0"))
                auto = int_or0(text_path(tt, "TotaleTitoliAbbAutomatizzatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbAutomatizzatiDigitali", "0"))
                man  = int_or0(text_path(tt, "TotaleTitoliAbbManualiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbManualiDigitali", "0"))
                ann  = int_or0(text_path(tt, "TotaleTitoliAbbAnnullatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbAnnullatiDigitali", "0"))
                dasp = int_or0(text_path(tt, "TotaleTitoliAbbDaspatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbDaspatiDigitali", "0"))
                rub  = int_or0(text_path(tt, "TotaleTitoliAbbRubatiTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbRubatiDigitali", "0"))
                bl   = int_or0(text_path(tt, "TotaleTitoliAbbBLTradiz", "0")) + int_or0(text_path(tt, "TotaleTitoliAbbBLDigitali", "0"))

                agg["LTA"] += lta
                agg["NoAccesso"] += noacc
                agg["Automatizzati"] += auto
                agg["Manuali"] += man
                agg["Annullati"] += ann
                agg["Daspati"] += dasp
                agg["Rubati"] += rub
                agg["BL"] += bl

    agg["Totale"] = agg["LTA"] + agg["NoAccesso"] + agg["Automatizzati"] + agg["Manuali"] + agg["Annullati"] + agg["Daspati"] + agg["Rubati"] + agg["BL"]
    return agg

# -------------------------
# HTML builder
# -------------------------
def build_accessi_html(root: ET.Element, file_title: str) -> str:
    root_tag = localname(root.tag)
    sost = root.attrib.get("Sostituzione", "")

    tit = child(root, "Titolare")
    tit_info = {
        "Denominazione": text_path(tit, "DenominazioneTitolareCA"),
        "CF": text_path(tit, "CFTitolareCA"),
        "CodiceSistemaCA": text_path(tit, "CodiceSistemaCA"),
        "DataRiepilogo": text_path(tit, "DataRiepilogo"),
        "DataGenerazione": text_path(tit, "DataGenerazioneRiepilogo"),
        "OraGenerazione": text_path(tit, "OraGenerazioneRiepilogo"),
        "Progressivo": text_path(tit, "ProgressivoRiepilogo"),
    }

    events = children(root, "Evento")

    # Tabella Eventi
    tbody_rows: List[str] = []
    details_blocks: List[str] = []

    for idx, e in enumerate(events, start=1):
        cf_org = text_path(e, "CFOrganizzatore")
        den_org = text_path(e, "DenominazioneOrganizzatore")
        tip_org = text_path(e, "TipologiaOrganizzatore")
        spett = text_path(e, "SpettacoloIntrattenimento")
        inc = text_path(e, "IncidenzaIntrattenimento")

        loc = text_path(e, "DenominazioneLocale")
        cod_loc = text_path(e, "CodiceLocale")
        data_ev = text_path(e, "DataEvento")
        ora_ev = text_path(e, "OraEvento")
        gen = text_path(e, "TipoGenere")
        titolo = text_path(e, "TitoloEvento")
        autore = text_path(e, "Autore")
        esec = text_path(e, "Esecutore")
        naz = text_path(e, "NazionalitaFilm")
        num_op = text_path(e, "NumOpereRappresentate")

        systems = children(e, "SistemaEmissione")
        nsys = len(systems)

        agg = aggregate_event(e)

        # filtro
        filter_blob = " ".join([
            str(idx), cf_org, den_org, tip_org, spett, inc,
            loc, cod_loc, data_ev, ora_ev, gen, titolo, autore, esec, naz, num_op,
            str(nsys),
            " ".join([text_path(s, "CodiceSistemaEmissione") for s in systems]),
        ]).lower()

        # sort keys
        sort_idx = str(idx)
        sort_date = data_ev if (data_ev.isdigit() and len(data_ev) == 8) else data_ev
        sort_time = ora_ev if ora_ev.isdigit() else ora_ev

        def td(display: str, sort_key: str = "") -> str:
            d = html.escape(display)
            sk = sort_key if sort_key != "" else display.strip().lower()
            return f"<td data-sort='{html.escape(sk)}'>{d}</td>"

        tbody_rows.append(
            f"<tr class='eventrow' data-filter='{html.escape(filter_blob)}' data-idx='{idx}'>"
            + td(str(idx), sort_idx)
            + td(fmt_date(data_ev), sort_date)
            + td(fmt_time(ora_ev), sort_time)
            + td(loc, loc.lower())
            + td(cod_loc, cod_loc.lower())
            + td(gen, gen.lower())
            + td(titolo, titolo.lower())
            + td(den_org, den_org.lower())
            + td(str(nsys), str(nsys))
            + td(str(agg["Totale"]), str(agg["Totale"]))
            + td(str(agg["Annullati"]), str(agg["Annullati"]))
            + "</tr>"
        )

        # Dettaglio: sistemi -> titoli/abbonamenti
        sys_blocks = []
        for s_i, s in enumerate(systems, start=1):
            code_sys = text_path(s, "CodiceSistemaEmissione")

            # Titoli per ordine di posto
            tit_sections = []
            for tblock in children(s, "Titoli"):
                cod_op = text_path(tblock, "CodiceOrdinePosto")
                cap = text_path(tblock, "Capienza")
                rows = []
                for tt in children(tblock, "TotaleTipoTitolo"):
                    tipo = text_path(tt, "TipoTitolo")
                    vals = [str(int_or0(text_path(tt, xmln, "0"))) for _, xmln in TITOLI_FIELDS]
                    rows.append((tipo, vals))

                if rows:
                    header_cols = "".join(f"<th>{html.escape(lbl)}</th>" for lbl, _ in TITOLI_FIELDS)
                    body = ""
                    for tipo, vals in rows:
                        tds = f"<td>{html.escape(tipo)}</td>" + "".join(f"<td>{html.escape(v)}</td>" for v in vals)
                        body += f"<tr>{tds}</tr>"
                    table = f"""
                    <div class="subhead">Titoli — Ordine posto <b>{html.escape(cod_op)}</b> (Capienza {html.escape(cap)})</div>
                    <div class="tablewrap">
                      <table class="mini">
                        <thead><tr><th>TipoTitolo</th>{header_cols}</tr></thead>
                        <tbody>{body}</tbody>
                      </table>
                    </div>
                    """
                else:
                    table = f"<div class='muted'>Titoli — Ordine posto {html.escape(cod_op)}: nessun dato</div>"
                tit_sections.append(table)

            # Abbonamenti per ordine di posto
            abb_sections = []
            for ablock in children(s, "Abbonamenti"):
                cod_op = text_path(ablock, "CodiceOrdinePosto")
                cap = text_path(ablock, "Capienza")
                rows = []
                for tt in children(ablock, "TotaleTipoTitoloAbbonamento"):
                    tipo = text_path(tt, "TipoTitoloAbbonamento")
                    vals = [str(int_or0(text_path(tt, xmln, "0"))) for _, xmln in ABB_FIELDS]
                    rows.append((tipo, vals))

                if rows:
                    header_cols = "".join(f"<th>{html.escape(lbl)}</th>" for lbl, _ in ABB_FIELDS)
                    body = ""
                    for tipo, vals in rows:
                        tds = f"<td>{html.escape(tipo)}</td>" + "".join(f"<td>{html.escape(v)}</td>" for v in vals)
                        body += f"<tr>{tds}</tr>"
                    table = f"""
                    <div class="subhead">Abbonamenti — Ordine posto <b>{html.escape(cod_op)}</b> (Capienza {html.escape(cap)})</div>
                    <div class="tablewrap">
                      <table class="mini">
                        <thead><tr><th>TipoTitoloAbb</th>{header_cols}</tr></thead>
                        <tbody>{body}</tbody>
                      </table>
                    </div>
                    """
                else:
                    table = f"<div class='muted'>Abbonamenti — Ordine posto {html.escape(cod_op)}: nessun dato</div>"
                abb_sections.append(table)

            sys_blocks.append(f"""
              <details class="sys">
                <summary>Sistema emissione {s_i}: <b>{html.escape(code_sys)}</b></summary>
                <div class="pad">
                  {''.join(tit_sections) if tit_sections else "<div class='muted'>Nessun blocco Titoli</div>"}
                  <div style="height:10px;"></div>
                  {''.join(abb_sections) if abb_sections else "<div class='muted'>Nessun blocco Abbonamenti</div>"}
                </div>
              </details>
            """)

        pill = f"<span class='pill'>Sistemi: {nsys}</span> <span class='pill'>Totale: {agg['Totale']}</span> <span class='pill pill-warn'>Annullati: {agg['Annullati']}</span>"

        details_blocks.append(f"""
        <details class="event" data-filter="{html.escape(filter_blob)}" data-idx="{idx}">
          <summary>
            Evento {idx}: <b>{html.escape(fmt_date(data_ev))} {html.escape(fmt_time(ora_ev))}</b> — {html.escape(loc)} ({html.escape(cod_loc)}) — {html.escape(titolo)} {pill}
          </summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h4>Dati evento</h4>
                <ul>
                  <li><b>Organizzatore</b>: {html.escape(den_org)} — CF {html.escape(cf_org)} — {html.escape(tip_org)}</li>
                  <li><b>Spettacolo/Intrattenimento</b>: {html.escape(spett)} — Incidenza {html.escape(inc)}%</li>
                  <li><b>Genere</b>: {html.escape(gen)}</li>
                  <li><b>Titolo</b>: {html.escape(titolo)}</li>
                  <li><b>Autore</b>: {html.escape(autore)}</li>
                  <li><b>Esecutore</b>: {html.escape(esec)}</li>
                  <li><b>Nazionalità film</b>: {html.escape(naz)}</li>
                  <li><b># opere rappresentate</b>: {html.escape(num_op)}</li>
                </ul>
              </div>

              <div class="card2">
                <h4>Accessi aggregati</h4>
                <table>
                  <thead><tr><th>Categoria</th><th>Totale</th></tr></thead>
                  <tbody>
                    <tr><td>LTA</td><td>{agg["LTA"]}</td></tr>
                    <tr><td>No accesso</td><td>{agg["NoAccesso"]}</td></tr>
                    <tr><td>Automatizzati</td><td>{agg["Automatizzati"]}</td></tr>
                    <tr><td>Manuali</td><td>{agg["Manuali"]}</td></tr>
                    <tr><td>Annullati</td><td>{agg["Annullati"]}</td></tr>
                    <tr><td>Daspati</td><td>{agg["Daspati"]}</td></tr>
                    <tr><td>Rubati</td><td>{agg["Rubati"]}</td></tr>
                    <tr><td>Blacklist</td><td>{agg["BL"]}</td></tr>
                    <tr><td><b>Totale</b></td><td><b>{agg["Totale"]}</b></td></tr>
                  </tbody>
                </table>
                <div class="muted" style="margin-top:6px;">
                  (Somma di titoli + abbonamenti, tradizionali e digitali)
                </div>
              </div>
            </div>

            <h3>Sistemi di emissione</h3>
            {''.join(sys_blocks) if sys_blocks else "<div class='muted'>Nessun SistemaEmissione</div>"}
          </div>
        </details>
        """)

    # Page header
    def esc(s: str) -> str:
        return html.escape(s or "")

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    .muted{color:#666;font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px;}
    .grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;margin-top:10px;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;}
    .card2{border:1px solid #eee;border-radius:12px;padding:12px;background:#fff;}
    ul{margin:8px 0 0 18px;}
    table{border-collapse:collapse;width:100%;margin-top:10px;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    .pill{display:inline-block;margin-left:8px;padding:2px 8px;border-radius:999px;background:#f0f0f0;font-weight:700;font-size:12px;color:#333;}
    .pill-warn{background:#fff2cc;color:#6a4b00;}
    .search{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    .mini th,.mini td{font-size:12px;padding:5px 6px;}
    .subhead{margin:8px 0 4px 0;font-weight:700;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyFilter(){
      const q = norm(document.getElementById('q').value).trim();
      const rows = document.querySelectorAll('#evBody tr.eventrow');
      const dets = document.querySelectorAll('details.event');

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
      const table = document.getElementById('eventTable');
      const ths = table.querySelectorAll('th.sortable');
      ths.forEach((th, idx) => {
        th.addEventListener('click', () => {
          const type = th.getAttribute('data-type') || 'text';
          const isAsc = !th.classList.contains('sorted-asc');
          sortTableByCol('eventTable', idx, type, isAsc);
        });
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('input', applyFilter);
      initSorting();
    });
    """

    header = f"""
    <h1>Accessi Reader</h1>
    <div class="muted">{esc(file_title)} — root: <code>{esc(root_tag)}</code></div>

    <div class="grid">
      <div class="card">
        <h2>Titolare</h2>
        <ul>
          <li><b>Denominazione</b>: {esc(tit_info["Denominazione"])}</li>
          <li><b>CF</b>: {esc(tit_info["CF"])}</li>
          <li><b>Codice sistema CA</b>: {esc(tit_info["CodiceSistemaCA"])}</li>
          <li><b>Data riepilogo</b>: {esc(fmt_date(tit_info["DataRiepilogo"]))}</li>
          <li><b>Generazione</b>: {esc(fmt_date(tit_info["DataGenerazione"]))} {esc(fmt_time(tit_info["OraGenerazione"]))}</li>
          <li><b>Progressivo</b>: {esc(tit_info["Progressivo"])}</li>
          <li><b>Sostituzione</b>: {esc(sost)}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Riepilogo</h2>
        <ul>
          <li><b>Eventi</b>: {len(events)}</li>
        </ul>
        <div class="muted">
          Suggerimento: usa il filtro per cercare per locale, titolo, CF organizzatore, codice sistema emissione…
        </div>
      </div>
    </div>
    """

    table = f"""
    <div class="card" style="margin-top:12px;">
      <h2>Eventi</h2>
      <input id="q" class="search" placeholder="Filtra per data, locale, titolo, organizzatore, sistema emissione..." />
      <div class="tablewrap">
        <table id="eventTable">
          <thead>
            <tr>
              <th class="sortable" data-type="num">#</th>
              <th class="sortable" data-type="date">Data</th>
              <th class="sortable" data-type="time">Ora</th>
              <th class="sortable" data-type="text">Locale</th>
              <th class="sortable" data-type="text">Cod. locale</th>
              <th class="sortable" data-type="text">Genere</th>
              <th class="sortable" data-type="text">Titolo</th>
              <th class="sortable" data-type="text">Organizzatore</th>
              <th class="sortable" data-type="num"># Sistemi</th>
              <th class="sortable" data-type="num">Totale</th>
              <th class="sortable" data-type="num">Annullati</th>
            </tr>
          </thead>
          <tbody id="evBody">
            {''.join(tbody_rows)}
          </tbody>
        </table>
      </div>

      <h3>Dettaglio</h3>
      {''.join(details_blocks)}
    </div>
    """

    return f"<!doctype html><html><head><meta charset='utf-8'><title>Accessi Reader</title><style>{css}</style></head><body>{header}{table}<script>{js}</script></body></html>"


# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="Accessi Reader: genera un report HTML (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File Accessi .xml/.xsi oppure firmati .p7m")
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
        out_path = str(p.with_name(out_base + ".accessi.html"))

        html_doc = build_accessi_html(root, p.name)
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

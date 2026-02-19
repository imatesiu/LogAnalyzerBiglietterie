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
from typing import Optional, List

# -------------------------
# XML helpers (namespace-safe)
# -------------------------
def localname(tag: str) -> str:
    if not tag:
        return ""
    return tag.split("}", 1)[-1] if "}" in tag else tag

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

def find_path(elem: Optional[ET.Element], path: str) -> Optional[ET.Element]:
    if elem is None:
        return None
    cur = elem
    for part in path.split("/"):
        cur = child(cur, part)
        if cur is None:
            return None
    return cur

def text_path(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    n = find_path(elem, path)
    if n is None or n.text is None:
        return default
    return n.text.strip()

def attr_path(elem: Optional[ET.Element], path: str, attr: str, default: str = "") -> str:
    n = find_path(elem, path)
    if n is None:
        return default
    return n.attrib.get(attr, default)

def first_text(elem: Optional[ET.Element], paths: List[str], default: str = "") -> str:
    for p in paths:
        v = text_path(elem, p, "")
        if v != "":
            return v
    return default

def int_or0(s: str) -> int:
    s = (s or "").strip()
    if not s:
        return 0
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

def money_from_cents(value: str, cents_mode: bool = True) -> str:
    s = (value or "").strip()
    if not s:
        return ""
    if not re.fullmatch(r"-?\d+", s):
        return html.escape(s)
    n = int(s)
    amount = (n / 100.0) if cents_mode else float(n)
    us = f"{amount:,.2f}"
    it = us.replace(",", "X").replace(".", ",").replace("X", ".")
    return it + " EUR"

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
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return tmp_path
    except Exception:
        pass

    # 2) macOS security cms -D
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
# HTML helpers (sorting)
# -------------------------
def th(label: str, dtype: str) -> str:
    # dtype: text|num|date|time|money
    return f"<th class='sortable' data-type='{html.escape(dtype)}'>{html.escape(label)}</th>"

def td(display_html: str, sort_key: str = "") -> str:
    # display_html è già safe/escaped (o testo semplice)
    if sort_key == "":
        sk = re.sub(r"<[^>]+>", "", display_html).strip().lower()
    else:
        sk = sort_key
    return f"<td data-sort='{html.escape(sk)}'>{display_html}</td>"

# -------------------------
# RPM HTML builder
# -------------------------
def build_html(root: ET.Element, file_title: str, cents_mode: bool = True) -> str:
    attrs = root.attrib or {}
    mese = attrs.get("Mese", "")
    dg = attrs.get("DataGenerazione", "")
    og = attrs.get("OraGenerazione", "")
    prog = attrs.get("ProgressivoGenerazione", "")
    sost = attrs.get("Sostituzione", "")

    tit = child(root, "Titolare")
    org = child(root, "Organizzatore")

    # Abbonamenti block (se presente)
    abbo_html = ""
    abbo = child(org, "Abbonamenti") if org is not None else None
    if abbo is not None:
        em = child(abbo, "AbbonamentiEmessi")
        an = child(abbo, "AbbonamentiAnnullati")
        # AbbonamentoIVAPreassolta / AbbonamentoIVAPreassoltaAnnullati
        anip = child(abbo,"AbbonamentoIVAPreassolta")
        anipa = child(abbo,"AbbonamentoIVAPreassoltaAnnullati")

        def sec_row(label: str, el: Optional[ET.Element]) -> List[str]:
            if el is None:
                return [html.escape(label), "", "", "", ""]
            return [
                html.escape(label),
                html.escape(text_path(el, "Quantita")),
                html.escape(money_from_cents(text_path(el, "CorrispettivoLordo"), cents_mode)),
                html.escape(money_from_cents(text_path(el, "Prevendita"), cents_mode)),
                html.escape(money_from_cents(text_path(el, "IVACorrispettivo"), cents_mode)),
            ]

        rows = [sec_row("Emessi", em), sec_row("Annullati", an),
                sec_row("IVAPreassolta", anip), sec_row("IVAPreassoltaAnnullati", anipa)]
        abbo_table = (
            "<table><thead><tr>"
            "<th>Sezione</th><th>Quantità</th><th>Corrispettivo</th><th>Prevendita</th><th>IVA Corrisp.</th>"
            "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
            + "</tbody></table>"
        )

        abbo_html = f"""
        <div class="card">
          <h2>Abbonamenti</h2>
          <ul>
            <li><b>Codice Abbonamento</b>: {html.escape(text_path(abbo,'CodiceAbbonamento'))}</li>
            <li><b>Validità</b>: {html.escape(fmt_date(text_path(abbo,'Validita')))}</li>
            <li><b>Tipo Tassazione</b>: {html.escape(attr_path(abbo,'TipoTassazione','valore'))}</li>
            <li><b>Turno</b>: {html.escape(attr_path(abbo,'Turno','valore'))}</li>
            <li><b>Codice Ordine</b>: {html.escape(text_path(abbo,'CodiceOrdine'))}</li>
            <li><b>Tipo Titolo</b>: {html.escape(text_path(abbo,'TipoTitolo'))}</li>
            <li><b>Q.tà eventi abilitati</b>: {html.escape(text_path(abbo,'QuantitaEventiAbilitati'))}</li>
          </ul>
          {abbo_table}
        </div>
        """

    # Eventi
    events = children(org, "Evento") if org is not None else []

    # Tabella eventi (ordinabile) + dettagli eventi (expand)
    tbody_rows = []
    ev_details = []

    for idx, e in enumerate(events, start=1):
        loc = child(e, "Locale")
        loc_name = text_path(loc, "Denominazione")
        loc_code = text_path(loc, "CodiceLocale")

        date = text_path(e, "DataEvento")
        time = text_path(e, "OraEvento")

        intr = child(e, "Intrattenimento")
        tass = attr_path(intr, "TipoTassazione", "valore", "")
        inc_intr = text_path(intr, "Incidenza", "")
        imp_intr = text_path(intr, "ImponibileIntrattenimenti", "")

        title = text_path(e, "MultiGenere/TitoliOpere/Titolo")

        # Totali evento: accesso, annullati, eccedenza omaggi e IVA eccedenza omaggi
        tot_qty_accesso = 0
        tot_qty_ann = 0
        tot_corr_accesso = 0
        tot_prev_accesso = 0
        tot_corr_ann = 0
        tot_prev_ann = 0
        tot_ecc_omaggi = 0
        tot_iva_ecc_omaggi = 0

        tot_qty_biglabb = 0
        tot_corr_biglabb = 0
        tot_prev_biglabb = 0

        tot_qty_ann_biglabb = 0
        tot_corr_ann_biglabb = 0
        tot_prev_ann_biglabb = 0

        tot_qty_ann_abfissi  = 0
        tot_corr_ann_abfissi  = 0
        tot_prev_ann_abfissi  = 0

        for od in children(e, "OrdineDiPosto"):
            ecc = first_text(od, ["EccedenzaOmaggi", "ImportoEccedenzaOmaggi", "EccedenzaOmaggiImporto"], "")
            iva_ecc = first_text(od, ["IVAEccedenteOmaggi", "IVAEccedenzaOmaggi"], "")

            tot_ecc_omaggi += int_or0(ecc)
            tot_iva_ecc_omaggi += int_or0(iva_ecc)

            for ta in children(od, "TitoliAccesso"):
                tot_qty_accesso += int_or0(text_path(ta, "Quantita", "0"))
                tot_corr_accesso += int_or0(text_path(ta, "CorrispettivoLordo", "0"))
                tot_prev_accesso += int_or0(text_path(ta, "Prevendita", "0"))

            for tn in children(od, "TitoliAnullati"):
                tot_qty_ann += int_or0(text_path(tn, "Quantita", "0"))
                tot_corr_ann += int_or0(text_path(ta, "CorrispettivoLordo", "0"))
                tot_prev_ann += int_or0(text_path(ta, "Prevendita", "0"))

            #  BigliettiAbbonamento
            for ba in children(od, "BigliettiAbbonamento"):
                tot_qty_biglabb += int_or0(text_path(ba, "Quantita", "0"))
                tot_corr_biglabb += int_or0(text_path(ta, "CorrispettivoLordo", "0"))
                tot_prev_biglabb += int_or0(text_path(ta, "Prevendita", "0"))


            #  BigliettiAbbonamentoAnnullati
            for ba in children(od, "BigliettiAbbonamentoAnnullati"):
                tot_qty_ann_biglabb += int_or0(text_path(ba, "Quantita", "0"))
                tot_corr_ann_biglabb += int_or0(text_path(ta, "CorrispettivoLordo", "0"))
                tot_prev_ann_biglabb += int_or0(text_path(ta, "Prevendita", "0"))

            # (opzionale) AbbonamentiFissiAnnullati
            for af in children(od, "AbbonamentiFissiAnnullati"):
                tot_qty_ann_abfissi += int_or0(text_path(af, "Quantita", "0"))
                tot_corr_ann_abfissi += int_or0(text_path(ta, "CorrispettivoLordo", "0"))
                tot_prev_ann_abfissi += int_or0(text_path(ta, "Prevendita", "0"))


        # ---- TABELLINA EVENTI (con sorting)
        # filtro testuale (per ricerca)
        filter_blob = " ".join([
            str(idx), date, time, loc_name, loc_code, title, tass,
            imp_intr, str(tot_qty_accesso), str(tot_qty_ann),
        ]).lower()

        # chiavi sort
        sort_idx = str(idx)
        sort_date = date if (date.isdigit() and len(date) == 8) else date
        sort_time = time if time.isdigit() else time
        sort_qty = str(tot_qty_accesso)
        sort_ann = str(tot_qty_ann)
        sort_corr = str(tot_corr_accesso)
        sort_prev = str(tot_prev_accesso)
        sort_imp = str(int_or0(imp_intr))
        sort_iva_ecc = str(tot_iva_ecc_omaggi)

        disp_imp = money_from_cents(imp_intr, cents_mode) if imp_intr else "n/d"
        disp_iva_ecc = money_from_cents(str(tot_iva_ecc_omaggi), cents_mode) if tot_iva_ecc_omaggi else "0,00 EUR"

        tbody_rows.append(
            f"<tr class='eventrow' data-filter='{html.escape(filter_blob)}' data-idx='{idx}'>"
            + td(html.escape(str(idx)), sort_idx)
            + td(html.escape(fmt_date(date)), sort_date)
            + td(html.escape(fmt_time(time)), sort_time)
            + td(html.escape(loc_name), loc_name.lower())
            + td(html.escape(title), title.lower())
            + td(html.escape(tass if tass else "n/d"), (tass or "").lower())
            + td(html.escape(disp_imp), sort_imp)
            + td(html.escape(disp_iva_ecc), sort_iva_ecc)
            + td(html.escape(str(tot_qty_accesso)), sort_qty)
            + td(html.escape(str(tot_qty_ann)), sort_ann)
            + td(html.escape(money_from_cents(str(tot_corr_accesso), cents_mode)), sort_corr)
            + td(html.escape(money_from_cents(str(tot_prev_accesso), cents_mode)), sort_prev)
            + "</tr>"
        )

        # ---- DETTAGLIO EVENTO
        mg_items = []
        for mg in children(e, "MultiGenere"):
            tg = text_path(mg, "TipoGenere")
            inc = text_path(mg, "IncidenzaGenere")
            titles = []
            for op in children(mg, "TitoliOpere"):
                t = text_path(op, "Titolo")
                a = text_path(op, "Autore")
                ex = text_path(op, "Esecutore")
                parts = [p for p in [t, a, ex] if p]
                if parts:
                    titles.append(" — ".join(parts))
            mg_items.append(
                f"<li><b>Genere</b> {html.escape(tg)} (incidenza {html.escape(inc)}%)"
                + (f"<br><span class='muted'>{html.escape(' | '.join(titles))}</span>" if titles else "")
                + "</li>"
            )
        mg_block = f"<ul>{''.join(mg_items)}</ul>" if mg_items else "<div class='muted'>Nessun MultiGenere</div>"

        ordine_blocks = []
        for od_i, od in enumerate(children(e, "OrdineDiPosto"), start=1):
            cod = text_path(od, "CodiceOrdine")
            cap = text_path(od, "Capienza")

            ecc = first_text(od, ["EccedenzaOmaggi", "ImportoEccedenzaOmaggi", "EccedenzaOmaggiImporto"], "")
            iva_ecc = first_text(od, ["IVAEccedenteOmaggi", "IVAEccedenzaOmaggi"], "")

            ecc_fmt = money_from_cents(ecc, cents_mode) if ecc else "0,00 EUR"
            iva_ecc_fmt = money_from_cents(iva_ecc, cents_mode) if iva_ecc else "0,00 EUR"

            # TitoliAccesso
            ta_rows = []
            for ta in children(od, "TitoliAccesso"):
                ta_rows.append([
                    html.escape(text_path(ta, "TipoTitolo")),
                    html.escape(text_path(ta, "Quantita")),
                    html.escape(money_from_cents(text_path(ta, "CorrispettivoLordo"), cents_mode)),
                    html.escape(money_from_cents(text_path(ta, "Prevendita"), cents_mode)),
                    html.escape(money_from_cents(text_path(ta, "IVACorrispettivo"), cents_mode)),
                    html.escape(money_from_cents(text_path(ta, "IVAPrevendita"), cents_mode)),
                    html.escape(money_from_cents(text_path(ta, "ImportoPrestazione"), cents_mode)),
                ])
            ta_table = (
                "<table><thead><tr>"
                "<th>Tipo</th><th>Q.tà</th><th>Corrispettivo</th><th>Prevendita</th><th>IVA Corr.</th><th>IVA Prev.</th><th>Prest.</th>"
                "</tr></thead><tbody>"
                + ("".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in ta_rows) if ta_rows else
                   "<tr><td colspan='7' class='muted'>Nessun TitoliAccesso</td></tr>")
                + "</tbody></table>"
            )

            # TitoliAnnullati
            tn_rows = []
            for tn in children(od, "TitoliAnnullati"):
                tn_rows.append([
                    html.escape(text_path(tn, "TipoTitolo")),
                    html.escape(text_path(tn, "Quantita")),
                    html.escape(money_from_cents(text_path(tn, "CorrispettivoLordo"), cents_mode)),
                    html.escape(money_from_cents(text_path(tn, "Prevendita"), cents_mode)),
                    html.escape(money_from_cents(text_path(tn, "IVACorrispettivo"), cents_mode)),
                    html.escape(money_from_cents(text_path(tn, "IVAPrevendita"), cents_mode)),
                    html.escape(money_from_cents(text_path(tn, "ImportoPrestazione"), cents_mode)),
                ])
            tn_table = (
                "<table><thead><tr>"
                "<th>Tipo</th><th>Q.tà</th><th>Corrispettivo</th><th>Prevendita</th><th>IVA Corr.</th><th>IVA Prev.</th><th>Prest.</th>"
                "</tr></thead><tbody>"
                + ("".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in tn_rows) if tn_rows else
                   "<tr><td colspan='7' class='muted'>Nessun TitoliAnnullati</td></tr>")
                + "</tbody></table>"
            )

            # AbbonamentiFissi / BigliettiAbbonamento (se presenti)
            def abbo_table(tag: str) -> str:
                rows = []
                for ab in children(od, tag):
                    rows.append([
                        html.escape(text_path(ab, "CodiceFiscale")),
                        html.escape(text_path(ab, "CodiceAbbonamento")),
                        html.escape(text_path(ab, "TipoTitolo")),
                        html.escape(text_path(ab, "Quantita")),
                        html.escape(money_from_cents(text_path(ab, "ImportoFigurativo"), cents_mode)),
                        html.escape(money_from_cents(text_path(ab, "IVAFigurativa"), cents_mode)),
                    ])
                if not rows:
                    return ""
                return (
                    f"<h4>{html.escape(tag)}</h4>"
                    "<table><thead><tr>"
                    "<th>CF</th><th>Codice abb.</th><th>Tipo</th><th>Q.tà</th><th>Importo fig.</th><th>IVA fig.</th>"
                    "</tr></thead><tbody>"
                    + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
                    + "</tbody></table>"
                )

            extra = abbo_table("BigliettiAbbonamento") + abbo_table("AbbonamentiFissi") + abbo_table("BigliettiAbbonamentoAnnullati")

            # TitoliAccessoIVAPreassolta / TitoliIVAPreassoltaAnnullati (se presenti)
            def ivapre_table(tag: str) -> str:
                rows = []
                for ab in children(od, tag):
                    rows.append([
                        html.escape(text_path(ab, "TipoTitolo")),
                        html.escape(text_path(ab, "Quantita")),
                        html.escape(money_from_cents(text_path(ab, "ImportoFigurativo"), cents_mode)),
                        html.escape(money_from_cents(text_path(ab, "IVAFigurativa"), cents_mode)),
                    ])
                if not rows:
                    return ""
                return (
                        f"<h4>{html.escape(tag)}</h4>"
                        "<table><thead><tr>"
                        "<th>Tipo</th><th>Q.tà</th><th>Importo fig.</th><th>IVA fig.</th>"
                        "</tr></thead><tbody>"
                        + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
                        + "</tbody></table>"
                )

            extra += ivapre_table("TitoliAccessoIVAPreassolta") + ivapre_table("TitoliIVAPreassoltaAnnullati")
            ordine_blocks.append(f"""
              <details>
                <summary>Ordine di posto {od_i}: <b>{html.escape(cod)}</b> — Capienza {html.escape(cap)}</summary>
                <div class="pad">
                  <div><b>IVA eccedenza omaggi</b>: {html.escape(iva_ecc_fmt)}</div>

                  <h4>TitoliAccesso</h4>
                  {ta_table}

                  <h4>TitoliAnnullati</h4>
                  {tn_table}

                  {extra}
                </div>
              </details>
            """)

        ord_block = "".join(ordine_blocks) if ordine_blocks else "<div class='muted'>Nessun OrdineDiPosto</div>"

        imp_show = money_from_cents(imp_intr, cents_mode) if imp_intr else "n/d"
        inc_show = inc_intr if inc_intr else "n/d"
        ecc_ev_show = money_from_cents(str(tot_ecc_omaggi), cents_mode) if tot_ecc_omaggi else "0,00 EUR"
        iva_ecc_ev_show = money_from_cents(str(tot_iva_ecc_omaggi), cents_mode) if tot_iva_ecc_omaggi else "0,00 EUR"

        ev_details.append(f"""
          <details class="event" data-filter="{html.escape(filter_blob)}" data-idx="{idx}">
            <summary>
              Evento {idx}: <b>{html.escape(fmt_date(date))} {html.escape(fmt_time(time))}</b> — {html.escape(loc_name)} ({html.escape(loc_code)})
              <span class="pill">Tassazione {html.escape(tass if tass else "n/d")}</span>
            </summary>
            <div class="pad">
              <div><b>Titolo</b>: {html.escape(title)}</div>
              <div><b>Incidenza intrattenimento</b>: {html.escape(inc_show)}</div>
              <div><b>Imponibile intrattenimenti</b>: {html.escape(imp_show)}</div>
              <div><b>IVA eccedenza (tot.)</b>: {html.escape(iva_ecc_ev_show)}</div>

              <h3>Generi / Opere</h3>
              {mg_block}

              <h3>Ordini di posto</h3>
              {ord_block}
            </div>
          </details>
        """)

    # --- Header cards
    top = f"""
    <h1>RPM Reader</h1>
    <div class="muted">{html.escape(file_title)}</div>

    <div class="grid">
      <div class="card">
        <h2>Intestazione</h2>
        <ul>
          <li><b>Mese</b>: {html.escape(mese)}</li>
          <li><b>Generazione</b>: {html.escape(fmt_date(dg))} {html.escape(fmt_time(og))}</li>
          <li><b>Progressivo</b>: {html.escape(prog)}</li>
          <li><b>Sostituzione</b>: {html.escape(sost)}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Titolare</h2>
        <ul>
          <li><b>Denominazione</b>: {html.escape(text_path(tit,'Denominazione'))}</li>
          <li><b>Codice Fiscale</b>: {html.escape(text_path(tit,'CodiceFiscale'))}</li>
          <li><b>Sistema Emissione</b>: {html.escape(text_path(tit,'SistemaEmissione'))}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Organizzatore</h2>
        <ul>
          <li><b>Denominazione</b>: {html.escape(text_path(org,'Denominazione'))}</li>
          <li><b>Codice Fiscale</b>: {html.escape(text_path(org,'CodiceFiscale'))}</li>
          <li><b>Tipo organizzatore</b>: {html.escape(attr_path(org,'TipoOrganizzatore','valore'))}</li>
        </ul>
      </div>
    </div>
    """

    # --- Eventi table (sortable) + filter
    events_table = f"""
    <div class="card" style="margin-top:12px;">
      <h2>Eventi ({len(events)})</h2>
      <input id="q" class="search" placeholder="Filtra per locale, titolo, data, tassazione..." />
      <div class="tablewrap">
        <table id="eventTable">
          <thead>
            <tr>
              {th("#","num")}
              {th("Data","date")}
              {th("Ora","time")}
              {th("Locale","text")}
              {th("Titolo","text")}
              {th("Tass.","text")}
              {th("ImponibileIntr.","money")}
              {th("Iva Ecc. omaggi","money")}
              {th("Q.tà","num")}
              {th("Q.tà ann.","num")}
              {th("Corrispettivo","money")}
              {th("Prevendita","money")}
            </tr>
          </thead>
          <tbody id="evBody">
            {''.join(tbody_rows)}
          </tbody>
        </table>
      </div>

      <h3>Dettaglio</h3>
      {''.join(ev_details)}
    </div>
    """

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    .muted{color:#666;font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;}
    ul{margin:8px 0 0 18px;}
    table{border-collapse:collapse;width:100%;margin-top:10px;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    .pill{display:inline-block;margin-left:8px;padding:2px 8px;border-radius:999px;background:#f0f0f0;font-weight:700;font-size:12px;color:#333;}
    .search{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    h3{margin:14px 0 6px;}
    h4{margin:12px 0 6px;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
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
        if(type === 'num' || type === 'money' || type === 'date' || type === 'time'){
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

    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>RPM Reader</title>"
        f"<style>{css}</style></head><body>"
        f"{top}{abbo_html}{events_table}"
        f"<script>{js}</script></body></html>"
    )

# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="RPM Reader: genera un report HTML (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File RPM .xml/.xsi o firmati .p7m")
    ap.add_argument("--no-cents", action="store_true", help="Non dividere per 100 gli importi (default: centesimi)")
    ap.add_argument("--open", action="store_true", help="Apri il report nel browser a fine generazione")
    args = ap.parse_args()

    cents_mode = not args.no_cents

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
        out_path = str(p.with_name(out_base + ".rpm.html"))

        html_doc = build_html(root, p.name, cents_mode=cents_mode)
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


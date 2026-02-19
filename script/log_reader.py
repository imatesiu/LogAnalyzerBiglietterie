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
from collections import Counter
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

def text_path(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    cur = elem
    for part in path.split("/"):
        cur = child(cur, part)
        if cur is None:
            return default
    return (cur.text or default).strip()

def int_or0(s: str) -> int:
    s = (s or "").strip()
    if not re.fullmatch(r"-?\d+", s):
        return 0
    return int(s)

def extract_kv(elem: Optional[ET.Element]) -> List[Tuple[str, str]]:
    """
    Estrae coppie (chiave,valore) da:
    - attributi dell'elemento
    - figli immediati (tag -> text)
    """
    if elem is None:
        return []
    pairs: List[Tuple[str, str]] = []
    # attributi
    for k, v in (elem.attrib or {}).items():
        v = (v or "").strip()
        if v != "":
            pairs.append((f"@{k}", v))
    # figli
    for c in list(elem):
        key = localname(c.tag)
        val = (c.text or "").strip()
        if val != "":
            pairs.append((key, val))
    return pairs

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
# HTML helpers for sorting
# -------------------------
def td(text: str, sort_key: str = "") -> str:
    safe = text if text.startswith("<") else html.escape(text)
    if sort_key == "":
        sk = re.sub(r"<[^>]+>", "", safe).strip().lower()
    else:
        sk = sort_key
    return f"<td data-sort='{html.escape(sk)}'>{safe}</td>"

def th(label: str, dtype: str) -> str:
    return f"<th class='sortable' data-type='{html.escape(dtype)}'>{html.escape(label)}</th>"

# -------------------------
# Parse LOG into structured rows
# -------------------------
def parse_log(root: ET.Element) -> List[Dict[str, str]]:
    txs = children(root, "Transazione")
    out: List[Dict[str, str]] = []

    for t in txs:
        ta = child(t, "TitoloAccesso")

        ann = ""
        if ta is not None:
            ann = (ta.attrib.get("Annullamento", "") or "").strip()

        corr = text_path(ta, "CorrispettivoLordo", "0")
        prev = text_path(ta, "Prevendita", "0")
        iva_c = text_path(ta, "IVACorrispettivo", "0")
        iva_p = text_path(ta, "IVAPrevendita", "0")

        # nuove sezioni (opzionali) secondo XSD
        acq_reg = child(t, "AcquirenteRegistrazione")
        acq_tx = child(t, "AcquirenteTransazione")
        rif_ann = child(t, "RiferimentoAnnullamento")

        def flatten(prefix: str, pairs: List[Tuple[str, str]]) -> Dict[str, str]:
            d: Dict[str, str] = {}
            for k, v in pairs:
                # es: @Autenticazione -> AcqReg_Autenticazione
                kk = k[1:] if k.startswith("@") else k
                d[f"{prefix}_{kk}"] = v
            return d

        row: Dict[str, str] = {
            "CFOrganizzatore": t.attrib.get("CFOrganizzatore", ""),
            "CFTitolare": t.attrib.get("CFTitolare", ""),
            "SistemaEmissione": t.attrib.get("SistemaEmissione", ""),

            "DataEmissione": t.attrib.get("DataEmissione", ""),
            "OraEmissione": t.attrib.get("OraEmissione", ""),
            "NumeroProgressivo": t.attrib.get("NumeroProgressivo", ""),

            "TipoTitolo": t.attrib.get("TipoTitolo", ""),
            "CodiceOrdine": t.attrib.get("CodiceOrdine", ""),
            "Posto": t.attrib.get("Posto", ""),
            "Causale": t.attrib.get("Causale", ""),

            "SigilloFiscale": t.attrib.get("SigilloFiscale", ""),
            "CartaAttivazione": t.attrib.get("CartaAttivazione", ""),
            "CodiceRichiedenteEmissioneSigillo": t.attrib.get("CodiceRichiedenteEmissioneSigillo", ""),
            "TipoTassazione": t.attrib.get("TipoTassazione", ""),
            "Valuta": t.attrib.get("Valuta", ""),

            "OriginaleAnnullato": t.attrib.get("OriginaleAnnullato", ""),
            "CartaOriginaleAnnullato": t.attrib.get("CartaOriginaleAnnullato", ""),
            "CausaleAnnullamento": t.attrib.get("CausaleAnnullamento", ""),

            "ImponibileIntrattenimenti": t.attrib.get("ImponibileIntrattenimenti", "0"),

            "Annullamento": ann or "N",
            "CodiceLocale": text_path(ta, "CodiceLocale", ""),
            "DataEvento": text_path(ta, "DataEvento", ""),
            "OraEvento": text_path(ta, "OraEvento", ""),
            "TipoGenere": text_path(ta, "TipoGenere", ""),
            "Titolo": text_path(ta, "Titolo", ""),

            "CorrispettivoLordo": corr,
            "Prevendita": prev,
            "IVACorrispettivo": iva_c,
            "IVAPrevendita": iva_p,
        }

        # flatten buyer/cancellation blocks into row dict
        row.update(flatten("AcqReg", extract_kv(acq_reg)))
        row.update(flatten("AcqTx", extract_kv(acq_tx)))
        row.update(flatten("RifAnn", extract_kv(rif_ann)))

        out.append(row)

    return out

# -------------------------
# Build HTML
# -------------------------
def build_log_html(rows_data: List[Dict[str, str]], file_title: str, cents_mode: bool = True) -> str:
    # Summary
    cforg = Counter([r.get("CFOrganizzatore", "") for r in rows_data])
    cftit = Counter([r.get("CFTitolare", "") for r in rows_data])
    sysEm = Counter([r.get("SistemaEmissione", "") for r in rows_data])

    dates = [r.get("DataEmissione", "") for r in rows_data if r.get("DataEmissione")]
    mind = min(dates) if dates else ""
    maxd = max(dates) if dates else ""

    def is_ann(v: str) -> bool:
        v = (v or "").strip().upper()
        return v in ("S", "Y", "1", "T", "TRUE")

    annulled = sum(1 for r in rows_data if is_ann(r.get("Annullamento", "")))

    tot_corr = sum(int_or0(r.get("CorrispettivoLordo", "0")) for r in rows_data)
    tot_prev = sum(int_or0(r.get("Prevendita", "0")) for r in rows_data)
    tot_iva_c = sum(int_or0(r.get("IVACorrispettivo", "0")) for r in rows_data)
    tot_iva_p = sum(int_or0(r.get("IVAPrevendita", "0")) for r in rows_data)
    tot_imp_intr = sum(int_or0(r.get("ImponibileIntrattenimenti", "0")) for r in rows_data)

    # Headers: Tipo genere prima di Titolo
    headers_html = (
            "<tr>"
            + th("#", "num")
            + th("Emiss.", "date")
            + th("Ora", "time")
            + th("Prog", "num")
            + th("Tipo", "text")
            + th("Ord", "text")
            + th("Locale", "text")
            + th("Data ev.", "date")
            + th("Ora ev.", "time")
            + th("Tipo genere", "text")
            + th("Titolo", "text")
            + th("Corr.", "money")
            + th("Prev.", "money")
            + th("IVA Corr.", "money")
            + th("IVA Prev.", "money")
            + th("ImponibileIntr.", "money")
            + th("Ann", "text")
            + "</tr>"
    )

    tbody_rows = []
    details_blocks = []

    def render_kv_block(title: str, d: Dict[str, str], prefix: str, preferred_order: List[str]) -> str:
        # estrai tutte le chiavi prefix_*
        items = []
        for k, v in d.items():
            if k.startswith(prefix + "_") and (v or "").strip() != "":
                items.append((k[len(prefix) + 1 :], v.strip()))

        if not items:
            return f"<div class='muted'>Nessun dato</div>"

        # ordina: prima preferred_order, poi il resto alfabetico
        order_index = {name: i for i, name in enumerate(preferred_order)}
        items.sort(key=lambda kv: (order_index.get(kv[0], 10_000), kv[0].lower()))

        lis = "".join(f"<li><b>{html.escape(k)}</b>: {html.escape(v)}</li>" for k, v in items)
        return f"<h4>{html.escape(title)}</h4><ul>{lis}</ul>"

    for idx, r in enumerate(rows_data, start=1):
        de = r.get("DataEmissione", "")
        oe = r.get("OraEmissione", "")
        prog = r.get("NumeroProgressivo", "")
        tip = r.get("TipoTitolo", "")
        ordc = r.get("CodiceOrdine", "")
        loc = r.get("CodiceLocale", "")
        dev = r.get("DataEvento", "")
        oev = r.get("OraEvento", "")
        tgen = r.get("TipoGenere", "")
        titolo = r.get("Titolo", "")

        corr = r.get("CorrispettivoLordo", "0")
        prev = r.get("Prevendita", "0")
        iva_c = r.get("IVACorrispettivo", "0")
        iva_p = r.get("IVAPrevendita", "0")
        imp = r.get("ImponibileIntrattenimenti", "0")

        ann = r.get("Annullamento", "N")
        ann_flag = is_ann(ann)

        # sort keys
        sort_date = de if de.isdigit() and len(de) == 8 else de
        sort_time = oe if oe.isdigit() else oe
        sort_prog = str(int_or0(prog))
        sort_corr = str(int_or0(corr))
        sort_prev = str(int_or0(prev))
        sort_ivac = str(int_or0(iva_c))
        sort_ivap = str(int_or0(iva_p))
        sort_imp = str(int_or0(imp))

        # filtro include anche campi acquirente e riferimento annullamento
        buyer_blob = " ".join([
            r.get("AcqReg_Autenticazione",""),
            r.get("AcqReg_CodiceUnivocoAcquirente",""),
            r.get("AcqReg_IndirizzoIPRegistrazione",""),
            r.get("AcqReg_DataOraRegistrazione",""),

            r.get("AcqTx_CodiceUnivocoNumeroTransazione",""),
            r.get("AcqTx_CellulareAcquirente",""),
            r.get("AcqTx_EmailAcquirente",""),
            r.get("AcqTx_IndirizzoIPTransazione",""),
            r.get("AcqTx_DataOraInizioCheckout",""),
            r.get("AcqTx_DataOraEsecuzionePagamento",""),
            r.get("AcqTx_CRO",""),
            r.get("AcqTx_MetodoSpedizioneTitolo",""),
            r.get("AcqTx_IndirizzoSpedizioneTitolo",""),

            r.get("RifAnn_OriginaleRiferimentoAnnullamento",""),
            r.get("RifAnn_CartaRiferimentoAnnullamento",""),
            r.get("RifAnn_CausaleRiferimentoAnnullamento",""),
        ])

        filter_blob = " ".join([
            str(idx), de, oe, prog, tip, ordc, loc, dev, oev, tgen, titolo,
            r.get("SigilloFiscale",""), r.get("CartaAttivazione",""),
            r.get("CFOrganizzatore",""), r.get("CFTitolare",""),
            r.get("Causale",""), r.get("CausaleAnnullamento",""),
            buyer_blob,
        ]).lower()

        tr_class = "txrow ann" if ann_flag else "txrow"
        tbody_rows.append(
            f"<tr class='{tr_class}' data-filter='{html.escape(filter_blob)}' data-idx='{idx}'>"
            + td(str(idx), str(idx))
            + td(fmt_date(de), sort_date)
            + td(fmt_time(oe), sort_time)
            + td(prog, sort_prog)
            + td(tip, tip.lower())
            + td(ordc, ordc.lower())
            + td(loc, loc.lower())
            + td(fmt_date(dev), dev if dev.isdigit() and len(dev)==8 else dev)
            + td(fmt_time(oev), oev if oev.isdigit() else oev)
            + td(tgen, tgen.lower())
            + td(titolo, titolo.lower())
            + td(money_from_cents(corr, cents_mode), sort_corr)
            + td(money_from_cents(prev, cents_mode), sort_prev)
            + td(money_from_cents(iva_c, cents_mode), sort_ivac)
            + td(money_from_cents(iva_p, cents_mode), sort_ivap)
            + td(money_from_cents(imp, cents_mode), sort_imp)
            + td(ann, ann.lower())
            + "</tr>"
        )

        pill = " <span class='pill pill-ann'>ANNULLATO</span>" if ann_flag else ""

        acq_reg_block = render_kv_block(
            "AcquirenteRegistrazione",
            r,
            "AcqReg",
            ["Autenticazione", "CodiceUnivocoAcquirente", "IndirizzoIPRegistrazione", "DataOraRegistrazione"],
        )
        acq_tx_block = render_kv_block(
            "AcquirenteTransazione",
            r,
            "AcqTx",
            ["CodiceUnivocoNumeroTransazione", "EmailAcquirente", "CellulareAcquirente", "IndirizzoIPTransazione",
             "DataOraInizioCheckout", "DataOraEsecuzionePagamento", "CRO", "MetodoSpedizioneTitolo", "IndirizzoSpedizioneTitolo"],
        )
        rif_ann_block = render_kv_block(
            "RiferimentoAnnullamento",
            r,
            "RifAnn",
            ["OriginaleRiferimentoAnnullamento", "CartaRiferimentoAnnullamento", "CausaleRiferimentoAnnullamento"],
        )

        details_blocks.append(f"""
        <details class="tx" data-filter="{html.escape(filter_blob)}" data-idx="{idx}">
          <summary>
            {html.escape(fmt_date(de))} {html.escape(fmt_time(oe))} — Prog {html.escape(prog)} — {html.escape(tip)} — {html.escape(titolo)}{pill}
          </summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h4>Transazione</h4>
                <ul>
                  <li><b>CF Organizzatore</b>: {html.escape(r.get('CFOrganizzatore',''))}</li>
                  <li><b>CF Titolare</b>: {html.escape(r.get('CFTitolare',''))}</li>
                  <li><b>Sistema Emissione</b>: {html.escape(r.get('SistemaEmissione',''))}</li>
                  <li><b>Richiedente</b>: {html.escape(r.get('CodiceRichiedenteEmissioneSigillo',''))}</li>
                  <li><b>Codice ordine</b>: {html.escape(ordc)}</li>
                  {f"<li><b>Posto</b>: {html.escape(r.get('Posto',''))}</li>" if r.get("Posto") else ""}
                  {f"<li><b>Causale</b>: {html.escape(r.get('Causale',''))}</li>" if r.get("Causale") else ""}
                  <li><b>Carta attivazione</b>: {html.escape(r.get('CartaAttivazione',''))}</li>
                  <li><b>Sigillo fiscale</b>: <code>{html.escape(r.get('SigilloFiscale',''))}</code></li>
                  <li><b>Tipo tassazione</b>: {html.escape(r.get('TipoTassazione',''))}</li>
                  <li><b>Valuta</b>: {html.escape(r.get('Valuta',''))}</li>
                  <li><b>Imponibile intrattenimenti</b>: {html.escape(money_from_cents(imp, cents_mode))}</li>
                  {f"<li><b>Originale annullato</b>: {html.escape(r.get('OriginaleAnnullato',''))}</li>" if r.get("OriginaleAnnullato") else ""}
                  {f"<li><b>Carta originale annullato</b>: {html.escape(r.get('CartaOriginaleAnnullato',''))}</li>" if r.get("CartaOriginaleAnnullato") else ""}
                  {f"<li><b>Causale annullamento</b>: {html.escape(r.get('CausaleAnnullamento',''))}</li>" if r.get("CausaleAnnullamento") else ""}
                </ul>
              </div>

              <div class="card2">
                <h4>Titolo di accesso</h4>
                <ul>
                  <li><b>Annullamento</b>: {html.escape(ann)}</li>
                  <li><b>Codice locale</b>: {html.escape(loc)}</li>
                  <li><b>Data/Ora evento</b>: {html.escape(fmt_date(dev))} {html.escape(fmt_time(oev))}</li>
                  <li><b>Tipo genere</b>: {html.escape(tgen)}</li>
                  <li><b>Titolo</b>: {html.escape(titolo)}</li>
                </ul>

                <h4>Importi</h4>
                <table>
                  <thead><tr><th>Voce</th><th>Valore</th></tr></thead>
                  <tbody>
                    <tr><td>Corrispettivo lordo</td><td>{html.escape(money_from_cents(corr, cents_mode))}</td></tr>
                    <tr><td>Prevendita</td><td>{html.escape(money_from_cents(prev, cents_mode))}</td></tr>
                    <tr><td>IVA Corrispettivo</td><td>{html.escape(money_from_cents(iva_c, cents_mode))}</td></tr>
                    <tr><td>IVA Prevendita</td><td>{html.escape(money_from_cents(iva_p, cents_mode))}</td></tr>
                  </tbody>
                </table>
              </div>

              <div class="card2">
                {acq_reg_block}
                {acq_tx_block}
                {rif_ann_block}
              </div>
            </div>
          </div>
        </details>
        """)

    def most_common(counter: Counter) -> str:
        return counter.most_common(1)[0][0] if counter else ""

    header = f"""
    <h1>LOG Reader</h1>
    <div class="muted">{html.escape(file_title)}</div>

    <div class="grid">
      <div class="card">
        <h2>Riepilogo</h2>
        <ul>
          <li><b>Transazioni</b>: {len(rows_data)}</li>
          <li><b>Annullate</b>: {annulled}</li>
          <li><b>Periodo emissione</b>: {html.escape(fmt_date(mind))} → {html.escape(fmt_date(maxd))}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Identificativi</h2>
        <ul>
          <li><b>CF Organizzatore</b>: {html.escape(most_common(cforg))}</li>
          <li><b>CF Titolare</b>: {html.escape(most_common(cftit))}</li>
          <li><b>Sistema Emissione</b>: {html.escape(most_common(sysEm))}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Totali (somma voci)</h2>
        <table>
          <thead><tr><th>Voce</th><th>Totale</th></tr></thead>
          <tbody>
            <tr><td>Corrispettivo lordo</td><td>{html.escape(money_from_cents(str(tot_corr), cents_mode))}</td></tr>
            <tr><td>Prevendita</td><td>{html.escape(money_from_cents(str(tot_prev), cents_mode))}</td></tr>
            <tr><td>IVA Corrispettivo</td><td>{html.escape(money_from_cents(str(tot_iva_c), cents_mode))}</td></tr>
            <tr><td>IVA Prevendita</td><td>{html.escape(money_from_cents(str(tot_iva_p), cents_mode))}</td></tr>
            <tr><td>Imponibile intrattenimenti</td><td>{html.escape(money_from_cents(str(tot_imp_intr), cents_mode))}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    """

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    h2{margin:0 0 8px 0;}
    .muted{color:#666;font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;}
    .grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;margin-top:10px;}
    .card2{border:1px solid #eee;border-radius:12px;padding:12px;background:#fff;}
    ul{margin:8px 0 0 18px;}
    table{border-collapse:collapse;width:100%;margin-top:10px;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    .wrap td{white-space:normal;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    .pill{display:inline-block;margin-left:8px;padding:2px 8px;border-radius:999px;background:#f0f0f0;font-weight:700;font-size:12px;color:#333;}
    .pill-ann{background:#ffe8e8;color:#8a1f1f;}
    .search{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;word-break:break-all;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
    tr.ann{background:#fff6f6;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyFilter(){
      const q = norm(document.getElementById('q').value).trim();
      const rows = document.querySelectorAll('#txBody tr.txrow');
      const dets = document.querySelectorAll('details.tx');

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
      const table = document.getElementById('txTable');
      const ths = table.querySelectorAll('th.sortable');
      ths.forEach((th, idx) => {
        th.addEventListener('click', () => {
          const type = th.getAttribute('data-type') || 'text';
          const isAsc = !th.classList.contains('sorted-asc');
          sortTableByCol('txTable', idx, type, isAsc);
        });
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('input', applyFilter);
      initSorting();
    });
    """

    table_html = f"""
    <div class="card" style="margin-top:12px;">
      <h2>Transazioni</h2>
      <input id="q" class="search"
             placeholder="Filtra per email, cellulare, IP, sigillo, carta, titolo, tipo genere, locale, progressivo..."
             oninput="applyFilter()" />
      <div class="tablewrap">
        <table id="txTable" class="wrap">
          <thead>{headers_html}</thead>
          <tbody id="txBody">
            {''.join(tbody_rows)}
          </tbody>
        </table>
      </div>

      <h3>Dettaglio</h3>
      {''.join(details_blocks)}
    </div>
    """

    body = header + table_html
    return f"<!doctype html><html><head><meta charset='utf-8'><title>LOG Reader</title><style>{css}</style></head><body>{body}<script>{js}</script></body></html>"

# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="LOG Reader: genera un report HTML (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File LOG .xsi/.xml oppure firmati .p7m")
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

        rows_data = parse_log(root)

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".log.html"))

        html_doc = build_log_html(rows_data, p.name, cents_mode=cents_mode)
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
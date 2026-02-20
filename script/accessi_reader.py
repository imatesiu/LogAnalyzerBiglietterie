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
from typing import Dict, List, Optional, Tuple


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

def esc(s: str) -> str:
    return html.escape(s or "")


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
# Domain mapping (Titoli / Abbonamenti)
# -------------------------
# Full fields exist in RCA (your sample confirms these for Titoli)
T_FIELDS = {
    "LTA": ("TotaleTitoliLTA", None),
    "NoAccesso": ("TotaleTitoliNoAccessoTradiz", "TotaleTitoliNoAccessoDigitali"),
    "Automatizzati": ("TotaleTitoliAutomatizzatiTradiz", "TotaleTitoliAutomatizzatiDigitali"),
    "Manuali": ("TotaleTitoliManualiTradiz", "TotaleTitoliManualiDigitali"),
    "Annullati": ("TotaleTitoliAnnullatiTradiz", "TotaleTitoliAnnullatiDigitali"),
    "Daspati": ("TotaleTitoliDaspatiTradiz", "TotaleTitoliDaspatiDigitali"),
    "Rubati": ("TotaleTitoliRubatiTradiz", "TotaleTitoliRubatiDigitali"),
    "Blacklist": ("TotaleTitoliBLTradiz", "TotaleTitoliBLDigitali"),
}

A_FIELDS = {
    "LTA": ("TotaleTitoliAbbLTA", None),
    "NoAccesso": ("TotaleTitoliAbbNoAccessoTradiz", "TotaleTitoliAbbNoAccessoDigitali"),
    "Automatizzati": ("TotaleTitoliAbbAutomatizzatiTradiz", "TotaleTitoliAbbAutomatizzatiDigitali"),
    "Manuali": ("TotaleTitoliAbbManualiTradiz", "TotaleTitoliAbbManualiDigitali"),
    "Annullati": ("TotaleTitoliAbbAnnullatiTradiz", "TotaleTitoliAbbAnnullatiDigitali"),
    "Daspati": ("TotaleTitoliAbbDaspatiTradiz", "TotaleTitoliAbbDaspatiDigitali"),
    "Rubati": ("TotaleTitoliAbbRubatiTradiz", "TotaleTitoliAbbRubatiDigitali"),
    "Blacklist": ("TotaleTitoliAbbBLTradiz", "TotaleTitoliAbbBLDigitali"),
}

ORDERED_CATS = ["LTA", "NoAccesso", "Automatizzati", "Manuali", "Annullati", "Daspati", "Rubati", "Blacklist"]


def read_counts(tt: ET.Element, fields: Dict[str, Tuple[str, Optional[str]]]) -> Dict[str, Dict[str, int]]:
    """
    Returns:
      {
        "LTA": {"T": n, "D": 0, "TOT": n},
        "NoAccesso": {"T": nT, "D": nD, "TOT": nT+nD},
        ...
      }
    """
    out: Dict[str, Dict[str, int]] = {}
    for cat, (t_name, d_name) in fields.items():
        t_val = int_or0(text_path(tt, t_name, "0"))
        d_val = int_or0(text_path(tt, d_name, "0")) if d_name else 0
        out[cat] = {"T": t_val, "D": d_val, "TOT": t_val + d_val}
    out["__TOTAL__"] = {
        "TOT": sum(out[c]["TOT"] for c in ORDERED_CATS),
        "T": sum(out[c]["T"] for c in ORDERED_CATS),
        "D": sum(out[c]["D"] for c in ORDERED_CATS),
    }
    return out


# -------------------------
# Parse RCA
# -------------------------
def parse_rca(root: ET.Element) -> Dict:
    # header
    sostituzione = root.attrib.get("Sostituzione", "")
    tit = child(root, "Titolare")
    header = {
        "Root": localname(root.tag),
        "Sostituzione": sostituzione,
        "Denominazione": text_path(tit, "DenominazioneTitolareCA"),
        "CF": text_path(tit, "CFTitolareCA"),
        "CodiceSistemaCA": text_path(tit, "CodiceSistemaCA"),
        "DataRiepilogo": text_path(tit, "DataRiepilogo"),
        "DataGenerazione": text_path(tit, "DataGenerazioneRiepilogo"),
        "OraGenerazione": text_path(tit, "OraGenerazioneRiepilogo"),
        "Progressivo": text_path(tit, "ProgressivoRiepilogo"),
    }

    events = []
    for ev in children(root, "Evento"):
        ev_info = {
            "CFOrganizzatore": text_path(ev, "CFOrganizzatore"),
            "DenominazioneOrganizzatore": text_path(ev, "DenominazioneOrganizzatore"),
            "TipologiaOrganizzatore": text_path(ev, "TipologiaOrganizzatore"),
            "SpettacoloIntrattenimento": text_path(ev, "SpettacoloIntrattenimento"),
            "IncidenzaIntrattenimento": text_path(ev, "IncidenzaIntrattenimento"),
            "DenominazioneLocale": text_path(ev, "DenominazioneLocale"),
            "CodiceLocale": text_path(ev, "CodiceLocale"),
            "DataEvento": text_path(ev, "DataEvento"),
            "OraEvento": text_path(ev, "OraEvento"),
            "TipoGenere": text_path(ev, "TipoGenere"),
            "TitoloEvento": text_path(ev, "TitoloEvento"),
            "Autore": text_path(ev, "Autore"),
            "Esecutore": text_path(ev, "Esecutore"),
            "NazionalitaFilm": text_path(ev, "NazionalitaFilm"),
            "NumOpereRappresentate": text_path(ev, "NumOpereRappresentate"),
        }

        systems = []
        for se in children(ev, "SistemaEmissione"):
            se_code = text_path(se, "CodiceSistemaEmissione")
            # blocks (Titoli + Abbonamenti) can repeat
            titoli_blocks = []
            for tb in children(se, "Titoli"):
                cod_op = text_path(tb, "CodiceOrdinePosto")
                cap = text_path(tb, "Capienza")
                tipos = []
                for tt in children(tb, "TotaleTipoTitolo"):
                    tipo = text_path(tt, "TipoTitolo")
                    counts = read_counts(tt, T_FIELDS)
                    tipos.append({"Tipo": tipo, "Counts": counts})
                titoli_blocks.append({"CodiceOrdinePosto": cod_op, "Capienza": cap, "Tipi": tipos})

            abb_blocks = []
            for ab in children(se, "Abbonamenti"):
                cod_op = text_path(ab, "CodiceOrdinePosto")
                cap = text_path(ab, "Capienza")
                tipos = []
                for tt in children(ab, "TotaleTipoTitoloAbbonamento"):
                    tipo = text_path(tt, "TipoTitoloAbbonamento")
                    counts = read_counts(tt, A_FIELDS)
                    tipos.append({"Tipo": tipo, "Counts": counts})
                abb_blocks.append({"CodiceOrdinePosto": cod_op, "Capienza": cap, "Tipi": tipos})

            systems.append({
                "CodiceSistemaEmissione": se_code,
                "TitoliBlocks": titoli_blocks,
                "AbbonamentiBlocks": abb_blocks,
            })

        events.append({"Info": ev_info, "Systems": systems})

    return {"Header": header, "Events": events}


def aggregate_event(ev: Dict) -> Dict[str, int]:
    """
    Aggregate totals for an event across all systems/blocks/types (Titoli + Abbonamenti)
    Returns totals by category (TOT).
    """
    tot = {c: 0 for c in ORDERED_CATS}
    tot_td = {c: {"T": 0, "D": 0} for c in ORDERED_CATS}

    for se in ev["Systems"]:
        for tb in se["TitoliBlocks"]:
            for t in tb["Tipi"]:
                c = t["Counts"]
                for cat in ORDERED_CATS:
                    tot[cat] += c[cat]["TOT"]
                    tot_td[cat]["T"] += c[cat]["T"]
                    tot_td[cat]["D"] += c[cat]["D"]
        for ab in se["AbbonamentiBlocks"]:
            for t in ab["Tipi"]:
                c = t["Counts"]
                for cat in ORDERED_CATS:
                    tot[cat] += c[cat]["TOT"]
                    tot_td[cat]["T"] += c[cat]["T"]
                    tot_td[cat]["D"] += c[cat]["D"]

    tot["Totale"] = sum(tot[c] for c in ORDERED_CATS)
    return {"by_cat": tot, "by_cat_td": tot_td}


def aggregate_file(data: Dict) -> Dict:
    by_cat = {c: 0 for c in ORDERED_CATS}
    top_tipi = Counter()
    n_systems = 0
    n_blocks = 0

    for ev in data["Events"]:
        n_systems += len(ev["Systems"])
        for se in ev["Systems"]:
            n_blocks += len(se["TitoliBlocks"]) + len(se["AbbonamentiBlocks"])
            for tb in se["TitoliBlocks"]:
                for t in tb["Tipi"]:
                    top_tipi[t["Tipo"]] += t["Counts"]["__TOTAL__"]["TOT"]
                    for c in ORDERED_CATS:
                        by_cat[c] += t["Counts"][c]["TOT"]
            for ab in se["AbbonamentiBlocks"]:
                for t in ab["Tipi"]:
                    top_tipi["(ABB) " + t["Tipo"]] += t["Counts"]["__TOTAL__"]["TOT"]
                    for c in ORDERED_CATS:
                        by_cat[c] += t["Counts"][c]["TOT"]

    by_cat["Totale"] = sum(by_cat[c] for c in ORDERED_CATS)

    return {
        "n_events": len(data["Events"]),
        "n_systems": n_systems,
        "n_blocks": n_blocks,
        "by_cat": by_cat,
        "top_tipi": top_tipi,
    }


# -------------------------
# HTML UI
# -------------------------
def badge(text: str, kind: str = "neutral") -> str:
    cls = {
        "neutral": "badge",
        "ok": "badge ok",
        "warn": "badge warn",
        "bad": "badge bad",
        "info": "badge info",
    }.get(kind, "badge")
    return f"<span class='{cls}'>{esc(text)}</span>"

def kpi(num: str, label: str) -> str:
    return f"<div class='kpi'><div class='knum'>{esc(num)}</div><div class='klabel'>{esc(label)}</div></div>"

def build_html(data: Dict, file_title: str) -> str:
    header = data["Header"]
    evs = data["Events"]
    agg = aggregate_file(data)

    # dashboard
    by_cat = agg["by_cat"]
    top5 = agg["top_tipi"].most_common(5)

    # Event table
    event_rows = []
    event_details = []

    for idx, ev in enumerate(evs, start=1):
        info = ev["Info"]
        systems = ev["Systems"]
        aev = aggregate_event(ev)
        cats = aev["by_cat"]

        filtro_blob = " ".join([
            str(idx),
            info.get("DenominazioneLocale",""),
            info.get("CodiceLocale",""),
            info.get("TitoloEvento",""),
            info.get("TipoGenere",""),
            info.get("CFOrganizzatore",""),
            info.get("DenominazioneOrganizzatore",""),
            " ".join([s.get("CodiceSistemaEmissione","") for s in systems]),
        ]).lower()

        def td(display: str, sort_key: str = "") -> str:
            sk = sort_key if sort_key != "" else display.strip().lower()
            return f"<td data-sort='{esc(sk)}'>{esc(display)}</td>"

        event_rows.append(
            f"<tr class='eventrow' data-filter='{esc(filtro_blob)}' data-idx='{idx}'>"
            + td(str(idx), str(idx))
            + td(fmt_date(info.get("DataEvento","")), info.get("DataEvento",""))
            + td(fmt_time(info.get("OraEvento","")), info.get("OraEvento",""))
            + td(info.get("DenominazioneLocale",""), info.get("DenominazioneLocale","").lower())
            + td(info.get("CodiceLocale",""), info.get("CodiceLocale",""))
            + td(info.get("TipoGenere",""), info.get("TipoGenere","").lower())
            + td(info.get("TitoloEvento",""), info.get("TitoloEvento","").lower())
            + td(info.get("DenominazioneOrganizzatore",""), info.get("DenominazioneOrganizzatore","").lower())
            + td(str(len(systems)), str(len(systems)))
            + td(str(cats["Totale"]), str(cats["Totale"]))
            + td(str(cats["Annullati"]), str(cats["Annullati"]))
            + "</tr>"
        )

        # detail blocks per system -> ordine posto
        sys_cards = []
        for s_i, se in enumerate(systems, start=1):
            se_code = se.get("CodiceSistemaEmissione","")
            # Titoli blocks
            tit_blocks_html = ""
            for b_i, tb in enumerate(se["TitoliBlocks"], start=1):
                cod_op = tb.get("CodiceOrdinePosto","")
                cap = tb.get("Capienza","")
                tipi = tb["Tipi"]

                # compact table (TOT per cat)
                rows = ""
                td_rows = ""  # expanded T/D table body
                for t in tipi:
                    tipo = t["Tipo"]
                    c = t["Counts"]
                    tot_row = [str(c[cat]["TOT"]) for cat in ORDERED_CATS]
                    tot_all = str(c["__TOTAL__"]["TOT"])
                    rows += (
                            "<tr>"
                            f"<td class='stickycol'>{esc(tipo)}</td>"
                            + "".join(f"<td>{esc(v)}</td>" for v in tot_row)
                            + f"<td class='tot'>{esc(tot_all)}</td>"
                              "</tr>"
                    )

                    # T/D row per tipo (single row with grouped values)
                    td_rows += (
                            "<tr>"
                            f"<td class='stickycol'>{esc(tipo)}</td>"
                            + "".join(
                        f"<td>{c[cat]['T']}</td><td>{c[cat]['D']}</td>"
                        for cat in ORDERED_CATS
                    )
                            + "</tr>"
                    )

                if not rows:
                    rows = "<tr><td colspan='10' class='muted'>(nessun TotaleTipoTitolo)</td></tr>"
                    td_rows = "<tr><td colspan='17' class='muted'>(nessun dettaglio)</td></tr>"

                compact = f"""
                <div class="tablewrap">
                  <table class="main mini">
                    <thead>
                      <tr>
                        <th class="stickycol">Tipo titolo</th>
                        <th>LTA</th><th>NoAcc</th><th>Auto</th><th>Man</th><th>Ann</th><th>Dasp</th><th>Rub</th><th>BL</th>
                        <th class="tot">Totale</th>
                      </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                  </table>
                </div>
                """

                td_header = (
                        "<tr><th class='stickycol'>Tipo titolo</th>"
                        + "".join(f"<th>{esc(cat)} T</th><th>{esc(cat)} D</th>" for cat in ORDERED_CATS)
                        + "</tr>"
                )

                td_detail = f"""
                <div class="tablewrap" style="margin-top:10px;">
                  <table class="main mini">
                    <thead>{td_header}</thead>
                    <tbody>{td_rows}</tbody>
                  </table>
                </div>
                """

                # block totals
                block_tot = {c: 0 for c in ORDERED_CATS}
                for t in tipi:
                    for c in ORDERED_CATS:
                        block_tot[c] += t["Counts"][c]["TOT"]
                block_sum = sum(block_tot[c] for c in ORDERED_CATS)

                pills = (
                        badge(f"Ordine posto {cod_op}", "info")
                        + " " + badge(f"Capienza {cap or 'n/d'}", "neutral")
                        + " " + badge(f"Totale {block_sum}", "ok")
                        + " " + badge(f"Annullati {block_tot['Annullati']}", "warn")
                )

                tit_blocks_html += f"""
                <details class="sub">
                  <summary>{pills}</summary>
                  <div class="pad">
                    <div class="muted" style="margin-bottom:8px;">
                      Vista compatta (totali per categoria). Sotto trovi il dettaglio <b>T/D</b>.
                    </div>
                    {compact}
                    <details class="sub2" style="margin-top:10px;">
                      <summary>{badge("Dettaglio Tradizionali/Digitali (T/D)", "neutral")}</summary>
                      <div class="pad">{td_detail}</div>
                    </details>
                  </div>
                </details>
                """

            if not tit_blocks_html:
                tit_blocks_html = "<div class='muted'>(nessun blocco Titoli)</div>"

            # Abbonamenti blocks (se presenti)
            abb_blocks_html = ""
            for b_i, ab in enumerate(se["AbbonamentiBlocks"], start=1):
                cod_op = ab.get("CodiceOrdinePosto","")
                cap = ab.get("Capienza","")
                tipi = ab["Tipi"]

                rows = ""
                td_rows = ""
                for t in tipi:
                    tipo = t["Tipo"]
                    c = t["Counts"]
                    tot_row = [str(c[cat]["TOT"]) for cat in ORDERED_CATS]
                    tot_all = str(c["__TOTAL__"]["TOT"])
                    rows += (
                            "<tr>"
                            f"<td class='stickycol'>{esc(tipo)}</td>"
                            + "".join(f"<td>{esc(v)}</td>" for v in tot_row)
                            + f"<td class='tot'>{esc(tot_all)}</td>"
                              "</tr>"
                    )
                    td_rows += (
                            "<tr>"
                            f"<td class='stickycol'>{esc(tipo)}</td>"
                            + "".join(
                        f"<td>{c[cat]['T']}</td><td>{c[cat]['D']}</td>"
                        for cat in ORDERED_CATS
                    )
                            + "</tr>"
                    )

                if not rows:
                    rows = "<tr><td colspan='10' class='muted'>(nessun TotaleTipoTitoloAbbonamento)</td></tr>"
                    td_rows = "<tr><td colspan='17' class='muted'>(nessun dettaglio)</td></tr>"

                compact = f"""
                <div class="tablewrap">
                  <table class="main mini">
                    <thead>
                      <tr>
                        <th class="stickycol">Tipo abb.</th>
                        <th>LTA</th><th>NoAcc</th><th>Auto</th><th>Man</th><th>Ann</th><th>Dasp</th><th>Rub</th><th>BL</th>
                        <th class="tot">Totale</th>
                      </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                  </table>
                </div>
                """

                td_header = (
                        "<tr><th class='stickycol'>Tipo abb.</th>"
                        + "".join(f"<th>{esc(cat)} T</th><th>{esc(cat)} D</th>" for cat in ORDERED_CATS)
                        + "</tr>"
                )

                td_detail = f"""
                <div class="tablewrap" style="margin-top:10px;">
                  <table class="main mini">
                    <thead>{td_header}</thead>
                    <tbody>{td_rows}</tbody>
                  </table>
                </div>
                """

                block_tot = {c: 0 for c in ORDERED_CATS}
                for t in tipi:
                    for c in ORDERED_CATS:
                        block_tot[c] += t["Counts"][c]["TOT"]
                block_sum = sum(block_tot[c] for c in ORDERED_CATS)

                pills = (
                        badge(f"Ordine posto {cod_op}", "info")
                        + " " + badge(f"Capienza {cap or 'n/d'}", "neutral")
                        + " " + badge(f"Totale {block_sum}", "ok")
                        + " " + badge(f"Annullati {block_tot['Annullati']}", "warn")
                )

                abb_blocks_html += f"""
                <details class="sub">
                  <summary>{pills}</summary>
                  <div class="pad">
                    <div class="muted" style="margin-bottom:8px;">
                      Vista compatta (totali per categoria). Sotto trovi il dettaglio <b>T/D</b>.
                    </div>
                    {compact}
                    <details class="sub2" style="margin-top:10px;">
                      <summary>{badge("Dettaglio Tradizionali/Digitali (T/D)", "neutral")}</summary>
                      <div class="pad">{td_detail}</div>
                    </details>
                  </div>
                </details>
                """

            if not abb_blocks_html:
                abb_blocks_html = "<div class='muted'>(nessun blocco Abbonamenti)</div>"

            sys_cards.append(f"""
            <details class="sys">
              <summary>{badge(f"Sistema emissione {s_i}", "neutral")} <code>{esc(se_code)}</code></summary>
              <div class="pad">
                <div class="grid2">
                  <div class="card2">
                    <h4>Titoli</h4>
                    {tit_blocks_html}
                  </div>
                  <div class="card2">
                    <h4>Abbonamenti</h4>
                    {abb_blocks_html}
                  </div>
                </div>
              </div>
            </details>
            """)

        # event detail header
        info_list = f"""
          <li><b>Organizzatore</b>: {esc(info.get("DenominazioneOrganizzatore",""))} — CF <code>{esc(info.get("CFOrganizzatore",""))}</code> — {esc(info.get("TipologiaOrganizzatore",""))}</li>
          <li><b>Spett./Intr.</b>: {esc(info.get("SpettacoloIntrattenimento",""))} — Incidenza {esc(info.get("IncidenzaIntrattenimento",""))}%</li>
          <li><b>Locale</b>: {esc(info.get("DenominazioneLocale",""))} (<code>{esc(info.get("CodiceLocale",""))}</code>)</li>
          <li><b>Data/Ora</b>: {esc(fmt_date(info.get("DataEvento","")))} {esc(fmt_time(info.get("OraEvento","")))}</li>
          <li><b>Genere</b>: {esc(info.get("TipoGenere",""))}</li>
          <li><b>Titolo</b>: {esc(info.get("TitoloEvento",""))}</li>
          <li><b>Autore</b>: {esc(info.get("Autore",""))}</li>
          <li><b>Esecutore</b>: {esc(info.get("Esecutore",""))}</li>
          <li><b>Nazionalità film</b>: {esc(info.get("NazionalitaFilm",""))}</li>
          <li><b># opere</b>: {esc(info.get("NumOpereRappresentate",""))}</li>
        """

        # KPI card event
        kpis = (
                kpi(str(len(systems)), "Sistemi")
                + kpi(str(cats["Totale"]), "Totale")
                + kpi(str(cats["LTA"]), "LTA")
                + kpi(str(cats["NoAccesso"]), "No accesso")
                + kpi(str(cats["Automatizzati"]), "Automatizzati")
                + kpi(str(cats["Manuali"]), "Manuali")
                + kpi(str(cats["Annullati"]), "Annullati")
        )

        pills = (
                badge(f"Totale {cats['Totale']}", "ok") + " "
                + badge(f"Annullati {cats['Annullati']}", "warn") + " "
                + badge(f"No accesso {cats['NoAccesso']}", "info")
        )

        event_details.append(f"""
        <details class="event" data-filter="{esc(filtro_blob)}" data-idx="{idx}">
          <summary>
            Evento {idx}: <b>{esc(fmt_date(info.get("DataEvento","")))} {esc(fmt_time(info.get("OraEvento","")))}</b> — {esc(info.get("DenominazioneLocale",""))}
            — {esc(info.get("TitoloEvento",""))} {pills}
          </summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h3>Info evento</h3>
                <ul>{info_list}</ul>
              </div>
              <div class="card2">
                <h3>Indicatori</h3>
                <div class="kpirow">{kpis}</div>
                <div class="muted" style="margin-top:10px;">
                  I conteggi includono Titoli e (se presenti) Abbonamenti, somma Tradizionali + Digitali.
                </div>
              </div>
            </div>

            <div style="margin-top:12px;">
              <h3>Sistemi di emissione</h3>
              {''.join(sys_cards) if sys_cards else "<div class='muted'>(nessun SistemaEmissione)</div>"}
            </div>
          </div>
        </details>
        """)

    top_tipi_list = ""
    if top5:
        top_tipi_list = "<ol>" + "".join(
            f"<li><b>{esc(name)}</b> — {val}</li>" for name, val in top5
        ) + "</ol>"
    else:
        top_tipi_list = "<div class='muted'>(nessun dato)</div>"

    # UI chrome
    css = """
    :root{
      --bg:#0b1220;
      --card:#ffffff;
      --line:#e6e8ee;
      --text:#0b1220;
      --muted:#667085;
      --shadow:0 6px 22px rgba(15, 23, 42, .08);
    }
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;color:var(--text);background:#f6f7fb;}
    .hero{
      background:linear-gradient(135deg, #0b1220, #182a4a);
      color:#fff; padding:22px 22px 18px 22px;
      position:sticky; top:0; z-index:20;
      box-shadow:0 8px 20px rgba(0,0,0,.10);
    }
    .hero h1{margin:0;font-size:20px;letter-spacing:.2px;}
    .hero .sub{margin-top:6px;color:rgba(255,255,255,.75);font-size:13px;}
    .wrap{max-width:1250px;margin:0 auto;padding:18px 18px 36px 18px;}
    h2{margin:0 0 10px 0;font-size:16px;}
    h3{margin:0 0 10px 0;font-size:15px;}
    h4{margin:0 0 8px 0;font-size:14px;}
    .muted{color:var(--muted);font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:12px;}
    .grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:12px;}
    .card{border:1px solid var(--line);border-radius:14px;padding:14px;background:var(--card);box-shadow:var(--shadow);}
    .card2{border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--card);box-shadow:0 4px 14px rgba(15,23,42,.06);}
    ul{margin:8px 0 0 18px;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;word-break:break-all;}
    .badge{display:inline-block;padding:2px 10px;border-radius:999px;background:#eef2ff;color:#233;padding-top:3px;font-weight:800;font-size:12px;border:1px solid #e1e6ff;}
    .badge.ok{background:#e7f8ef;border-color:#bfe9cf;color:#11643b;}
    .badge.warn{background:#fff5d6;border-color:#f1dea0;color:#6a4b00;}
    .badge.info{background:#e6f2ff;border-color:#bcdcff;color:#0b4aa5;}
    .kpirow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:6px;}
    .kpi{border:1px solid var(--line);border-radius:12px;padding:10px;background:#fbfcff;}
    .knum{font-size:18px;font-weight:900;}
    .klabel{color:var(--muted);font-size:12px;margin-top:2px;}
    .topline{display:flex;gap:12px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;}
    .right{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
    .search{width:min(620px, 92vw);padding:10px 12px;border:1px solid #d7dbe6;border-radius:12px;background:#fff;}
    .btn{padding:10px 12px;border-radius:12px;border:1px solid #d7dbe6;background:#fff;cursor:pointer;}
    .btn:hover{background:#f4f6fb;}
    .tablewrap{max-height:58vh;overflow:auto;border:1px solid var(--line);border-radius:14px;background:#fff;}
    table{border-collapse:collapse;width:100%;font-size:13px;}
    th,td{border-bottom:1px solid #eef0f6;padding:8px 10px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fbfcff;font-weight:900;position:sticky;top:0;z-index:5;}
    .mini th,.mini td{font-size:12px;padding:6px 8px;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#b7bdcc;font-weight:900;}
    .sorted-asc:after{content:" ↑";color:#30364a;}
    .sorted-desc:after{content:" ↓";color:#30364a;}
    details.event{border:1px solid var(--line);border-radius:14px;padding:10px 12px;margin-top:10px;background:#fff;box-shadow:0 4px 14px rgba(15,23,42,.06);}
    details.sys, details.sub, details.sub2{border:1px solid #eef0f6;border-radius:12px;padding:8px 10px;margin-top:10px;background:#fbfcff;}
    summary{cursor:pointer;font-weight:900;}
    .pad{padding-top:10px;}
    .stickycol{position:sticky;left:0;background:#fff;z-index:3;}
    .tot{font-weight:900;}
    ol{margin:8px 0 0 18px;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyGlobal(){
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

    function clearGlobal(){
      document.getElementById('q').value = '';
      applyGlobal();
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
      document.getElementById('q').addEventListener('input', applyGlobal);
      initSorting();
    });
    """

    hero = f"""
    <div class="hero">
      <h1>RCA / Controllo Accessi</h1>
      <div class="sub">
        {esc(file_title)} — Titolare <b>{esc(header.get("Denominazione",""))}</b>
        — CF <code>{esc(header.get("CF",""))}</code>
        — SistemaCA <code>{esc(header.get("CodiceSistemaCA",""))}</code>
        — Riepilogo {esc(fmt_date(header.get("DataRiepilogo","")))}
        {("— " + badge("Sostituzione " + header.get("Sostituzione",""), "warn")) if header.get("Sostituzione","") else ""}
      </div>
    </div>
    """

    header_cards = f"""
    <div class="grid">
      <div class="card">
        <h2>Intestazione</h2>
        <ul>
          <li><b>Generazione</b>: {esc(fmt_date(header.get("DataGenerazione","")))} {esc(fmt_time(header.get("OraGenerazione","")))}</li>
          <li><b>Progressivo</b>: {esc(header.get("Progressivo",""))}</li>
          <li><b>Root</b>: <code>{esc(header.get("Root",""))}</code></li>
        </ul>
      </div>

      <div class="card">
        <h2>Riepilogo</h2>
        <div class="kpirow">
          {kpi(str(agg["n_events"]), "Eventi")}
          {kpi(str(agg["n_systems"]), "Sistemi")}
          {kpi(str(agg["n_blocks"]), "Blocchi ord. posto")}
          {kpi(str(by_cat["Totale"]), "Totale")}
          {kpi(str(by_cat["LTA"]), "LTA")}
          {kpi(str(by_cat["Annullati"]), "Annullati")}
        </div>
        <div class="muted" style="margin-top:10px;">
          Totali = somma categorie (Tradizionali + Digitali). Include Titoli e (se presenti) Abbonamenti.
        </div>
      </div>

      <div class="card">
        <h2>Top tipi titolo</h2>
        <div class="muted">In base al totale accessi nel file</div>
        {top_tipi_list}
      </div>
    </div>
    """

    event_table = f"""
    <div class="card" style="margin-top:12px;">
      <div class="topline">
        <div>
          <h2>Eventi ({len(evs)})</h2>
          <div class="muted">Filtro globale (tabella + dettagli). Ordina cliccando le intestazioni.</div>
        </div>
        <div class="right">
          <input id="q" class="search" placeholder="Filtra per locale, titolo, CF, genere, sistema emissione..." />
          <button class="btn" type="button" onclick="clearGlobal()">Pulisci</button>
        </div>
      </div>

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
            {''.join(event_rows) if event_rows else "<tr><td colspan='11' class='muted'>(nessun evento)</td></tr>"}
          </tbody>
        </table>
      </div>

      <h3 style="margin-top:14px;">Dettaglio eventi</h3>
      {''.join(event_details) if event_details else "<div class='muted'>(nessun dettaglio)</div>"}
    </div>
    """

    body = f"""
    <div class="wrap">
      {header_cards}
      {event_table}
    </div>
    """

    return f"<!doctype html><html><head><meta charset='utf-8'><title>RCA Reader</title><style>{css}</style></head><body>{hero}{body}<script>{js}</script></body></html>"


# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="RCA/Accessi Reader: report HTML organizzato (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File RCA .xml/.xsi oppure firmati .p7m")
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
                try:
                    os.unlink(temp_to_cleanup)
                except Exception:
                    pass
            continue

        if localname(root.tag) != "RiepilogoControlloAccessi":
            # non blocco, ma avviso (può comunque funzionare parzialmente se i tag coincidono)
            print(f"NOTE: root tag inatteso: {localname(root.tag)}", file=sys.stderr)

        data = parse_rca(root)
        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".accessi.html"))

        html_doc = build_html(data, p.name)
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

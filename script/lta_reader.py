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

def children(elem: Optional[ET.Element], name: Optional[str] = None) -> List[ET.Element]:
    if elem is None:
        return []
    if name is None:
        return list(elem)
    return [c for c in list(elem) if localname(c.tag) == name]

def child(elem: Optional[ET.Element], name: str) -> Optional[ET.Element]:
    if elem is None:
        return None
    for c in list(elem):
        if localname(c.tag) == name:
            return c
    return None

def text_of(elem: Optional[ET.Element], default: str = "") -> str:
    if elem is None or elem.text is None:
        return default
    return elem.text.strip()

def text_path(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    cur = elem
    for p in path.split("/"):
        cur = child(cur, p)
        if cur is None:
            return default
    return text_of(cur, default)

def attr(elem: Optional[ET.Element], name: str, default: str = "") -> str:
    if elem is None:
        return default
    return (elem.attrib.get(name, default) or "").strip()

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

def money_from_cents(value: str, cents_mode: bool = True) -> str:
    """
    Nel tracciato LTA CorrispettivoLordo è stringa: spesso in centesimi (come altri tracciati SIAE).
    Se nel tuo caso è già in euro, usa --no-cents.
    """
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
# LTA parsing (da lta.xsd)
# -------------------------
EVENT_ATTRS = [
    ("CF Organizzatore", "CFOrganizzatore"),
    ("Cod. Locale", "CodiceLocale"),
    ("Data evento", "DataEvento"),
    ("Ora evento", "OraEvento"),
    ("Titolo", "Titolo"),
    ("Genere", "TipoGenere"),
    ("Data apertura", "DataApertura"),
    ("Ora apertura", "OraApertura"),
]

SUPPORT_ATTRS = [
    ("Tipo supporto", "TipoSupportoId"),
    ("Cod. supporto", "CodSupportoId"),
]

# Colonne "essenziali" TitoloAccesso
TA_CORE_COLS = [
    ("Stato", "Stato"),
    ("Data LTA", "DataLTA"),
    ("Ora LTA", "OraLTA"),
    ("Ingresso", "DataIngresso"),  # mostriamo come "Data/Ora" combinato
    ("Tipo titolo", "TipoTitolo"),
    ("Corrispettivo", "CorrispettivoLordo"),
    ("Abbon.", "Abbonamento"),
    ("Annull.", "Annullamento"),
    ("Cod. ordine", "CodiceOrdine"),
    ("Posto", "Posto"),
    ("Sistema em.", "SistemaEmissione"),
    ("Supporto", "CodSupporto"),  # combinato con IdSupporto in display
    ("Partecipante", "__partecipante__"),
]


def parse_lta(root: ET.Element) -> Dict:
    """
    Ritorna un dict strutturato:
    - header: attributi root
    - events: lista eventi con supporti + titoli accesso
    """
    root_tag = localname(root.tag)

    header = {
        "Root": root_tag,
        "SistemaCA": root.attrib.get("SistemaCA", ""),
        "CFTitolareCA": root.attrib.get("CFTitolareCA", ""),
        "DataLTA": root.attrib.get("DataLTA", ""),
    }

    events = []
    for ev in children(root, "LTA_Evento"):
        ev_data = {
            "attrs": dict(ev.attrib or {}),
            "supporti": [],
            "titoli": [],
        }

        for s in children(ev, "Supporto"):
            ev_data["supporti"].append(dict(s.attrib or {}))

        for t in children(ev, "TitoloAccesso"):
            t_data = {"attrs": dict(t.attrib or {}), "partecipante": {}}
            p = child(t, "Partecipante")
            if p is not None:
                t_data["partecipante"] = {
                    "Nome": text_path(p, "Nome"),
                    "Cognome": text_path(p, "Cognome"),
                    "DataNascita": text_path(p, "DataNascita"),
                    "LuogoNascita": text_path(p, "LuogoNascita"),
                }
            ev_data["titoli"].append(t_data)

        events.append(ev_data)

    return {"header": header, "events": events}


def compute_dashboard(data: Dict) -> Dict:
    events = data["events"]
    n_events = len(events)
    n_supporti = sum(len(e["supporti"]) for e in events)
    n_titoli = sum(len(e["titoli"]) for e in events)

    stato_counter = Counter()
    ann_counter = 0
    abb_counter = 0
    ingressi_counter = 0

    for e in events:
        for t in e["titoli"]:
            st = (t["attrs"].get("Stato", "") or "").strip()
            if st:
                stato_counter[st] += 1
            if (t["attrs"].get("Annullamento", "N") or "N").strip().upper() == "S":
                ann_counter += 1
            if (t["attrs"].get("Abbonamento", "N") or "N").strip().upper() == "S":
                abb_counter += 1
            if (t["attrs"].get("DataIngresso", "") or "").strip() or (t["attrs"].get("OraIngresso", "") or "").strip():
                ingressi_counter += 1

    # distribuzione per prima lettera (utile senza semantica ufficiale)
    group_letter = Counter()
    group_td = Counter()
    for k, v in stato_counter.items():
        if k:
            group_letter[k[0]] += v
            if k[-1] in ("T", "D"):
                group_td[k[-1]] += v

    return {
        "n_events": n_events,
        "n_supporti": n_supporti,
        "n_titoli": n_titoli,
        "n_ann": ann_counter,
        "n_abb": abb_counter,
        "n_ingressi": ingressi_counter,
        "stato_counter": stato_counter,
        "group_letter": group_letter,
        "group_td": group_td,
    }


# -------------------------
# HTML builder
# -------------------------
def badge(text: str, kind: str = "neutral") -> str:
    cls = {
        "neutral": "badge",
        "ok": "badge ok",
        "warn": "badge warn",
        "bad": "badge bad",
        "info": "badge info",
    }.get(kind, "badge")
    return f"<span class='{cls}'>{html.escape(text)}</span>"

def esc(s: str) -> str:
    return html.escape(s or "")

def build_lta_html(data: Dict, file_title: str, cents_mode: bool) -> str:
    header = data["header"]
    events = data["events"]
    dash = compute_dashboard(data)

    # Event table rows + details
    event_rows = []
    event_details = []

    for idx, e in enumerate(events, start=1):
        a = e["attrs"]
        supporti = e["supporti"]
        titoli = e["titoli"]

        # per-event counts
        tot_tit = len(titoli)
        tot_sup = len(supporti)
        tot_ann = sum(1 for t in titoli if (t["attrs"].get("Annullamento", "N") or "N").strip().upper() == "S")
        tot_abb = sum(1 for t in titoli if (t["attrs"].get("Abbonamento", "N") or "N").strip().upper() == "S")
        tot_ing = sum(1 for t in titoli if (t["attrs"].get("DataIngresso", "") or "").strip() or (t["attrs"].get("OraIngresso", "") or "").strip())

        titolo_ev = a.get("Titolo", "")
        data_ev = a.get("DataEvento", "")
        ora_ev = a.get("OraEvento", "")
        loc = a.get("CodiceLocale", "")
        gen = a.get("TipoGenere", "")
        cf_org = a.get("CFOrganizzatore", "")
        ap_d = a.get("DataApertura", "")
        ap_o = a.get("OraApertura", "")

        filter_blob = " ".join([
            str(idx), titolo_ev, data_ev, ora_ev, loc, gen, cf_org, ap_d, ap_o,
            " ".join([f"{s.get('TipoSupportoId','')} {s.get('CodSupportoId','')}" for s in supporti]),
            " ".join([t["attrs"].get("TipoTitolo","") for t in titoli]),
            " ".join([t["attrs"].get("SistemaEmissione","") for t in titoli]),
            " ".join([t["attrs"].get("Stato","") for t in titoli]),
        ]).lower()

        def td(display: str, sort_key: str = "") -> str:
            sk = sort_key if sort_key != "" else display.strip().lower()
            return f"<td data-sort='{esc(sk)}'>{esc(display)}</td>"

        # Row
        event_rows.append(
            f"<tr class='eventrow' data-filter='{esc(filter_blob)}' data-idx='{idx}'>"
            + td(str(idx), str(idx))
            + td(fmt_date(data_ev), data_ev)
            + td(fmt_time(ora_ev), ora_ev)
            + td(loc, loc)
            + td(gen, gen.lower())
            + td(titolo_ev, titolo_ev.lower())
            + td(cf_org, cf_org)
            + td(f\"{fmt_date(ap_d)} {fmt_time(ap_o)}\".strip(), ap_d + ap_o)
                   + td(str(tot_sup), str(tot_sup))
                   + td(str(tot_tit), str(tot_tit))
                   + td(str(tot_ing), str(tot_ing))
                   + td(str(tot_ann), str(tot_ann))
                   + td(str(tot_abb), str(tot_abb))
                   + "</tr>"
        )

        # Supporti table
        sup_body = ""
        for s in supporti:
            sup_body += "<tr>" + "".join(
                f"<td>{esc(s.get(attr_name, ''))}</td>"
                for _, attr_name in SUPPORT_ATTRS
            ) + "</tr>"
        sup_table = (
            f"<div class='tablewrap small'><table class='mini'>"
            f"<thead><tr>{''.join(f'<th>{esc(lbl)}</th>' for lbl,_ in SUPPORT_ATTRS)}</tr></thead>"
            f"<tbody>{sup_body or '<tr><td colspan=2 class=muted>(nessun supporto)</td></tr>'}</tbody>"
            f"</table></div>"
        )

        # Titoli table (core + expandable details)
        # We'll render an essential row + hidden detail row per title
        tit_rows = []
        for j, t in enumerate(titoli, start=1):
            ta = t["attrs"]
        p = t.get("partecipante", {}) or {}

        stato = (ta.get("Stato", "") or "").strip()
        # badge by last letter T/D
        bkind = "neutral"
        if stato.startswith("V"):
            bkind = "ok"
        elif stato.startswith(("A","B","Z")):
            bkind = "warn"
        elif stato.startswith(("D","F")):
            bkind = "info"

        stato_html = badge(stato or "n/d", bkind)

        d_lta = fmt_date(ta.get("DataLTA",""))
        o_lta = fmt_time(ta.get("OraLTA",""))
        d_in  = fmt_date(ta.get("DataIngresso",""))
        o_in  = fmt_time(ta.get("OraIngresso",""))
        ingresso = (d_in + (" " + o_in if o_in else "")).strip()

        tipo = ta.get("TipoTitolo","")
        corr = money_from_cents(ta.get("CorrispettivoLordo",""), cents_mode) if ta.get("CorrispettivoLordo","") else ""
        abbo = (ta.get("Abbonamento","N") or "N").strip().upper()
        annu = (ta.get("Annullamento","N") or "N").strip().upper()

        posto = ta.get("Posto","")
        codord = ta.get("CodiceOrdine","")
        sys_em = ta.get("SistemaEmissione","")

        codsup = ta.get("CodSupporto","")
        idsup = ta.get("IdSupporto","")
        supporto_disp = f"{codsup} / {idsup}".strip(" /")

        part_disp = ""
        if p.get("Nome") or p.get("Cognome"):
            part_disp = f"{p.get('Cognome','')} {p.get('Nome','')}".strip()
        else:
            part_disp = ""

        row_blob = " ".join([str(idx), str(j), stato, d_lta, o_lta, ingresso, tipo, corr, abbo, annu, codord, posto, sys_em, supporto_disp, part_disp]).lower()

        # main row
        tit_rows.append(
            f"<tr class='titrow' data-filter='{esc(row_blob)}' data-ev='{idx}'>"
            f"<td data-sort='{j}'>{j}</td>"
            f"<td data-sort='{esc(stato)}'>{stato_html}</td>"
            f"<td data-sort='{esc(ta.get('DataLTA',''))}'>{esc(d_lta)}</td>"
            f"<td data-sort='{esc(ta.get('OraLTA',''))}'>{esc(o_lta)}</td>"
            f"<td data-sort='{esc(ta.get('DataIngresso','') + ta.get('OraIngresso',''))}'>{esc(ingresso)}</td>"
            f"<td data-sort='{esc(tipo.lower())}'>{esc(tipo)}</td>"
            f"<td data-sort='{esc(ta.get('CorrispettivoLordo',''))}'>{corr}</td>"
            f"<td data-sort='{esc(abbo)}'>{badge('S' if abbo=='S' else 'N', 'info' if abbo=='S' else 'neutral')}</td>"
            f"<td data-sort='{esc(annu)}'>{badge('S' if annu=='S' else 'N', 'warn' if annu=='S' else 'neutral')}</td>"
            f"<td data-sort='{esc(codord)}'>{esc(codord)}</td>"
            f"<td data-sort='{esc(posto)}'>{esc(posto)}</td>"
            f"<td data-sort='{esc(sys_em.lower())}'>{esc(sys_em)}</td>"
            f"<td data-sort='{esc(supporto_disp)}'><code>{esc(supporto_disp)}</code></td>"
            f"<td data-sort='{esc(part_disp.lower())}'>{esc(part_disp)}</td>"
            f"<td><button class='btn-sm' type='button' onclick='toggleDetail(this)'>Dettagli</button></td>"
            f"</tr>"
        )

        # detail row (all attributes organized)
        # sections
        emissione = {
            "SistemaEmissione": ta.get("SistemaEmissione",""),
            "CartaAttivazione": ta.get("CartaAttivazione",""),
            "ProgressivoFiscale": ta.get("ProgressivoFiscale",""),
            "SigilloFiscale": ta.get("SigilloFiscale",""),
            "DataEmissione": fmt_date(ta.get("DataEmissione","")),
            "OraEmissione": fmt_time(ta.get("OraEmissione","")),
        }
        lta_info = {
            "DataLTA": fmt_date(ta.get("DataLTA","")),
            "OraLTA": fmt_time(ta.get("OraLTA","")),
            "DataIngresso": fmt_date(ta.get("DataIngresso","")),
            "OraIngresso": fmt_time(ta.get("OraIngresso","")),
            "Stato": ta.get("Stato",""),
        }
        ordine = {
            "TipoTitolo": ta.get("TipoTitolo",""),
            "CodiceOrdine": ta.get("CodiceOrdine",""),
            "Posto": ta.get("Posto",""),
            "CorrispettivoLordo": money_from_cents(ta.get("CorrispettivoLordo",""), cents_mode) if ta.get("CorrispettivoLordo","") else "",
        }
        abbon = {
            "Abbonamento": ta.get("Abbonamento","N"),
            "CFAbbonamento": ta.get("CFAbbonamento",""),
            "CodiceAbbonamento": ta.get("CodiceAbbonamento",""),
            "ProgressivoAbbonamento": ta.get("ProgressivoAbbonamento",""),
            "QEventiAbilitati": ta.get("QEventiAbilitati",""),
        }
        ann = {
            "Annullamento": ta.get("Annullamento","N"),
            "DataANN": fmt_date(ta.get("DataANN","")),
            "OraANN": fmt_time(ta.get("OraANN","")),
            "CartaAttivazioneANN": ta.get("CartaAttivazioneANN",""),
            "ProgressivoFiscaleANN": ta.get("ProgressivoFiscaleANN",""),
            "SigilloFiscaleANN": ta.get("SigilloFiscaleANN",""),
        }
        sup = {
            "CodSupporto": ta.get("CodSupporto",""),
            "IdSupporto": ta.get("IdSupporto",""),
            "IdSupAlt": ta.get("IdSupAlt",""),
        }
        part = {
            "Cognome": p.get("Cognome",""),
            "Nome": p.get("Nome",""),
            "DataNascita": fmt_date(p.get("DataNascita","")),
            "LuogoNascita": p.get("LuogoNascita",""),
        }

        def kv_table(d: Dict[str,str]) -> str:
            rows = ""
            for k,v in d.items():
                if v is None:
                    v = ""
                rows += f"<tr><td class='k'><code>{esc(k)}</code></td><td class='v'>{esc(v)}</td></tr>"
            return f"<table class='kv'><tbody>{rows}</tbody></table>"

        detail_html = f"""
            <div class="detailgrid">
              <div class="dcard"><div class="dtitle">Emissione</div>{kv_table(emissione)}</div>
              <div class="dcard"><div class="dtitle">LTA / Ingresso</div>{kv_table(lta_info)}</div>
              <div class="dcard"><div class="dtitle">Titolo / Ordine</div>{kv_table(ordine)}</div>
              <div class="dcard"><div class="dtitle">Abbonamento</div>{kv_table(abbon)}</div>
              <div class="dcard"><div class="dtitle">Annullamento</div>{kv_table(ann)}</div>
              <div class="dcard"><div class="dtitle">Supporto</div>{kv_table(sup)}</div>
              <div class="dcard"><div class="dtitle">Partecipante</div>{kv_table(part)}</div>
            </div>
            """

        tit_rows.append(
            f"<tr class='detailrow' style='display:none' data-ev='{idx}'>"
            f"<td colspan='16'>{detail_html}</td>"
            f"</tr>"
        )

    tit_table = f"""
        <div class="subbar">
          <div class="subleft">
            <h4>Titoli Accesso</h4>
            <div class="muted">Righe espandibili: clicca “Dettagli” per vedere tutti i campi, organizzati per sezioni.</div>
          </div>
          <div class="subright">
            <input class="mini-search" id="q_ev_{idx}" placeholder="Filtra titoli (solo questo evento)..." oninput="filterEventTitles({idx})" />
            <button class="btn-sm" type="button" onclick="clearEventTitles({idx})">Pulisci</button>
          </div>
        </div>

        <div class="tablewrap">
          <table class="main" id="titTable_{idx}">
            <thead>
              <tr>
                <th class="sortable" data-type="num">#</th>
                <th class="sortable" data-type="text">Stato</th>
                <th class="sortable" data-type="date">Data LTA</th>
                <th class="sortable" data-type="time">Ora LTA</th>
                <th class="sortable" data-type="text">Ingresso</th>
                <th class="sortable" data-type="text">Tipo</th>
                <th class="sortable" data-type="num">Corrispettivo</th>
                <th class="sortable" data-type="text">Abb.</th>
                <th class="sortable" data-type="text">Ann.</th>
                <th class="sortable" data-type="text">Cod. ordine</th>
                <th class="sortable" data-type="text">Posto</th>
                <th class="sortable" data-type="text">Sistema</th>
                <th class="sortable" data-type="text">Supporto</th>
                <th class="sortable" data-type="text">Partecipante</th>
                <th> </th>
              </tr>
            </thead>
            <tbody>
              {''.join(tit_rows) if tit_rows else "<tr><td colspan='15' class='muted'>(nessun TitoloAccesso)</td></tr>"}
            </tbody>
          </table>
        </div>
        """

    # Event info card
    info_list = ""
    for lbl, aname in EVENT_ATTRS:
        v = a.get(aname, "")
        if "Data" in aname:
            v = fmt_date(v)
        if "Ora" in aname:
            v = fmt_time(v)
        info_list += f"<li><b>{esc(lbl)}</b>: {esc(v)}</li>"

    pills = (
            badge(f"Supporti {tot_sup}", "neutral") + " "
            + badge(f"Titoli {tot_tit}", "info") + " "
            + badge(f"Ingressi {tot_ing}", "ok") + " "
            + badge(f"Annullati {tot_ann}", "warn") + " "
            + badge(f"Abb. {tot_abb}", "info")
    )

    event_details.append(f"""
        <details class="event" data-filter="{esc(filter_blob)}" data-idx="{idx}">
          <summary>
            Evento {idx}: <b>{esc(fmt_date(data_ev))} {esc(fmt_time(ora_ev))}</b> — Locale <code>{esc(loc)}</code> — {esc(titolo_ev)} {pills}
          </summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h3>Info evento</h3>
                <ul>{info_list}</ul>
              </div>

              <div class="card2">
                <h3>Supporti</h3>
                {sup_table}
                <div class="muted" style="margin-top:6px;">
                  I supporti sono definiti in evento; i titoli referenziano <code>CodSupporto</code>/<code>IdSupporto</code>.
                </div>
              </div>
            </div>

            <div style="margin-top:12px;">
              {tit_table}
            </div>
          </div>
        </details>
        """)

# Dashboard: stato distribution
stato_rows = ""
for k, v in dash["stato_counter"].most_common(20):
    stato_rows += f"<tr><td><code>{esc(k)}</code></td><td>{v}</td></tr>"
if not stato_rows:
    stato_rows = "<tr><td colspan='2' class='muted'>(nessuno stato presente)</td></tr>"

group_letter_rows = ""
for k, v in dash["group_letter"].most_common():
    group_letter_rows += f"<tr><td><code>{esc(k)}</code></td><td>{v}</td></tr>"
if not group_letter_rows:
    group_letter_rows = "<tr><td colspan='2' class='muted'>(n/d)</td></tr>"

group_td_rows = ""
for k, v in dash["group_td"].most_common():
    group_td_rows += f"<tr><td><code>{esc(k)}</code></td><td>{v}</td></tr>"
if not group_td_rows:
    group_td_rows = "<tr><td colspan='2' class='muted'>(n/d)</td></tr>"

# Event table HTML
event_table = f"""
    <div class="card" style="margin-top:12px;">
      <div class="topline">
        <div>
          <h2>Eventi ({len(events)})</h2>
          <div class="muted">Ordina cliccando le intestazioni. Il filtro agisce su tabella e dettagli.</div>
        </div>
        <div class="right">
          <input id="q" class="search" placeholder="Filtra per titolo, locale, CF, genere, stato, sistema emissione..." />
          <button class="btn" type="button" onclick="clearGlobal()">Pulisci</button>
        </div>
      </div>

      <div class="tablewrap">
        <table id="eventTable" class="main">
          <thead>
            <tr>
              <th class="sortable" data-type="num">#</th>
              <th class="sortable" data-type="date">Data</th>
              <th class="sortable" data-type="time">Ora</th>
              <th class="sortable" data-type="text">Cod. locale</th>
              <th class="sortable" data-type="text">Genere</th>
              <th class="sortable" data-type="text">Titolo</th>
              <th class="sortable" data-type="text">CF org.</th>
              <th class="sortable" data-type="text">Apertura</th>
              <th class="sortable" data-type="num"># Sup</th>
              <th class="sortable" data-type="num"># Tit</th>
              <th class="sortable" data-type="num">Ingressi</th>
              <th class="sortable" data-type="num">Annull.</th>
              <th class="sortable" data-type="num">Abb.</th>
            </tr>
          </thead>
          <tbody id="evBody">
            {''.join(event_rows) if event_rows else "<tr><td colspan='13' class='muted'>(nessun evento)</td></tr>"}
          </tbody>
        </table>
      </div>

      <h3 style="margin-top:14px;">Dettaglio eventi</h3>
      {''.join(event_details) if event_details else "<div class='muted'>(nessun dettaglio)</div>"}
    </div>
    """

# Header cards
header_cards = f"""
    <div class="grid">
      <div class="card">
        <h2>Intestazione</h2>
        <ul>
          <li><b>CF titolare</b>: <code>{esc(header.get("CFTitolareCA",""))}</code></li>
          <li><b>Sistema CA</b>: <code>{esc(header.get("SistemaCA",""))}</code></li>
          <li><b>Data LTA (file)</b>: {esc(fmt_date(header.get("DataLTA","")))}</li>
        </ul>
        <div class="muted" style="margin-top:10px;">
          File: <b>{esc(file_title)}</b>
        </div>
      </div>

      <div class="card">
        <h2>Riepilogo</h2>
        <div class="kpirow">
          <div class="kpi"><div class="knum">{dash["n_events"]}</div><div class="klabel">Eventi</div></div>
          <div class="kpi"><div class="knum">{dash["n_supporti"]}</div><div class="klabel">Supporti</div></div>
          <div class="kpi"><div class="knum">{dash["n_titoli"]}</div><div class="klabel">Titoli</div></div>
          <div class="kpi"><div class="knum">{dash["n_ingressi"]}</div><div class="klabel">Ingressi</div></div>
          <div class="kpi"><div class="knum">{dash["n_ann"]}</div><div class="klabel">Annullati</div></div>
          <div class="kpi"><div class="knum">{dash["n_abb"]}</div><div class="klabel">Abbonamenti</div></div>
        </div>
        <div class="muted" style="margin-top:10px;">
          Nota: “Ingressi” = titoli con <code>DataIngresso</code> o <code>OraIngresso</code> valorizzati.
        </div>
      </div>

      <div class="card">
        <h2>Stati</h2>
        <div class="grid2tight">
          <div>
            <div class="muted">Top stati (max 20)</div>
            <div class="tablewrap small">
              <table class="mini">
                <thead><tr><th>Stato</th><th>Q.tà</th></tr></thead>
                <tbody>{stato_rows}</tbody>
              </table>
            </div>
          </div>
          <div>
            <div class="muted">Raggruppamento (prima lettera)</div>
            <div class="tablewrap small">
              <table class="mini">
                <thead><tr><th>Gruppo</th><th>Q.tà</th></tr></thead>
                <tbody>{group_letter_rows}</tbody>
              </table>
            </div>
            <div class="muted" style="margin-top:10px;">T/D (ultimo char)</div>
            <div class="tablewrap small">
              <table class="mini">
                <thead><tr><th>T/D</th><th>Q.tà</th></tr></thead>
                <tbody>{group_td_rows}</tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="muted" style="margin-top:10px;">
          (Mantengo i codici “as-is”, senza interpretazioni non garantite dal tracciato.)
        </div>
      </div>
    </div>
    """

css = """
    :root{
      --bg:#0b1220;
      --panel:#0f172a;
      --card:#ffffff;
      --line:#e6e8ee;
      --text:#0b1220;
      --muted:#667085;
      --shadow:0 6px 22px rgba(15, 23, 42, .08);
    }
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;color:var(--text);background:#f6f7fb;}
    .hero{
      background:linear-gradient(135deg, #0b1220, #182a4a);
      color:#fff;
      padding:22px 22px 18px 22px;
      position:sticky; top:0; z-index:20;
      box-shadow:0 8px 20px rgba(0,0,0,.10);
    }
    .hero h1{margin:0;font-size:20px;letter-spacing:.2px;}
    .hero .sub{margin-top:6px;color:rgba(255,255,255,.75);font-size:13px;}
    .wrap{max-width:1200px;margin:0 auto;padding:18px 18px 36px 18px;}
    h2{margin:0 0 10px 0;font-size:16px;}
    h3{margin:0 0 10px 0;font-size:15px;}
    h4{margin:0 0 8px 0;font-size:14px;}
    .muted{color:var(--muted);font-size:13px;}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:12px;}
    .grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:12px;}
    .grid2tight{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;}
    .card{border:1px solid var(--line);border-radius:14px;padding:14px;background:var(--card);box-shadow:var(--shadow);}
    .card2{border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--card);box-shadow:0 4px 14px rgba(15,23,42,.06);}
    ul{margin:8px 0 0 18px;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;word-break:break-all;}
    .badge{display:inline-block;padding:2px 10px;border-radius:999px;background:#eef2ff;color:#233;padding-top:3px;font-weight:700;font-size:12px;border:1px solid #e1e6ff;}
    .badge.ok{background:#e7f8ef;border-color:#bfe9cf;color:#11643b;}
    .badge.warn{background:#fff5d6;border-color:#f1dea0;color:#6a4b00;}
    .badge.bad{background:#ffe4e4;border-color:#ffc2c2;color:#8a1f1f;}
    .badge.info{background:#e6f2ff;border-color:#bcdcff;color:#0b4aa5;}
    .kpirow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:6px;}
    .kpi{border:1px solid var(--line);border-radius:12px;padding:10px;background:#fbfcff;}
    .knum{font-size:18px;font-weight:900;}
    .klabel{color:var(--muted);font-size:12px;margin-top:2px;}
    .topline{display:flex;gap:12px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;}
    .right{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
    .search{width:min(560px, 90vw);padding:10px 12px;border:1px solid #d7dbe6;border-radius:12px;background:#fff;}
    .btn{padding:10px 12px;border-radius:12px;border:1px solid #d7dbe6;background:#fff;cursor:pointer;}
    .btn:hover{background:#f4f6fb;}
    .btn-sm{padding:7px 10px;border-radius:10px;border:1px solid #d7dbe6;background:#fff;cursor:pointer;font-size:12px;}
    .btn-sm:hover{background:#f4f6fb;}
    .mini-search{padding:8px 10px;border-radius:10px;border:1px solid #d7dbe6;background:#fff;min-width:280px;}
    .subbar{display:flex;gap:10px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;margin:6px 0 8px 0;}
    .tablewrap{max-height:58vh;overflow:auto;border:1px solid var(--line);border-radius:14px;background:#fff;}
    .tablewrap.small{max-height:220px;}
    table{border-collapse:collapse;width:100%;font-size:13px;}
    th,td{border-bottom:1px solid #eef0f6;padding:8px 10px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fbfcff;font-weight:800;position:sticky;top:0;z-index:5;}
    .mini th,.mini td{font-size:12px;padding:6px 8px;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#b7bdcc;font-weight:800;}
    .sorted-asc:after{content:" ↑";color:#30364a;}
    .sorted-desc:after{content:" ↓";color:#30364a;}
    details.event{border:1px solid var(--line);border-radius:14px;padding:10px 12px;margin-top:10px;background:#fff;box-shadow:0 4px 14px rgba(15,23,42,.06);}
    summary{cursor:pointer;font-weight:900;}
    .pad{padding-top:10px;}
    .detailgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;}
    .dcard{border:1px solid var(--line);border-radius:12px;padding:10px;background:#fbfcff;}
    .dtitle{font-weight:900;margin-bottom:6px;}
    table.kv{width:100%;border-collapse:collapse;font-size:12px;}
    table.kv td{border-bottom:1px solid #eef0f6;padding:6px 8px;white-space:normal;}
    table.kv td.k{width:44%;}
    table.kv td.v{color:#111;}
    tr.detailrow td{background:#fafbff;}
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

    function sortTableByCol(table, colIndex, type, asc){
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'))
        .filter(r => !r.classList.contains('detailrow')); // non sortare le detailrow

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

      // reinserisci mantenendo le detailrow sotto la loro riga principale
      rows.forEach(r=>{
        const detail = r.nextElementSibling && r.nextElementSibling.classList.contains('detailrow')
          ? r.nextElementSibling
          : null;
        tbody.appendChild(r);
        if(detail) tbody.appendChild(detail);
      });

      clearSortStyles(table);
      const ths = table.querySelectorAll('th.sortable');
      const th = ths[colIndex];
      if(th){
        th.classList.add(asc ? 'sorted-asc' : 'sorted-desc');
      }
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

    function toggleDetail(btn){
      const tr = btn.closest('tr');
      const next = tr.nextElementSibling;
      if(!next || !next.classList.contains('detailrow')) return;
      next.style.display = (next.style.display === 'none' || next.style.display === '') ? 'table-row' : 'none';
    }

    function filterEventTitles(evIdx){
      const q = norm(document.getElementById('q_ev_' + evIdx).value).trim();
      const table = document.getElementById('titTable_' + evIdx);
      if(!table) return;

      const rows = Array.from(table.querySelectorAll('tbody tr'));
      // rows include titrow + detailrow; we filter titrow and hide/show paired detailrow
      for(let i=0;i<rows.length;i++){
        const r = rows[i];
        if(!r.classList.contains('titrow')) continue;
        const detail = r.nextElementSibling && r.nextElementSibling.classList.contains('detailrow') ? r.nextElementSibling : null;
        const hay = norm(r.getAttribute('data-filter'));
        const show = (!q) ? true : hay.includes(q);
        r.style.display = show ? '' : 'none';
        if(detail){
          // se riga nascosta, nascondi anche dettagli
          if(!show) detail.style.display = 'none';
          else {
            // lascia com'è (se l’utente l’aveva aperta)
          }
        }
      }
    }

    function clearEventTitles(evIdx){
      const el = document.getElementById('q_ev_' + evIdx);
      if(el){ el.value=''; filterEventTitles(evIdx); }
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('q').addEventListener('input', applyGlobal);
      initSorting();
    });
    """

hero = f"""
    <div class="hero">
      <h1>LTA Reader</h1>
      <div class="sub">
        {esc(file_title)} — CF titolare <code>{esc(header.get("CFTitolareCA",""))}</code> — SistemaCA <code>{esc(header.get("SistemaCA",""))}</code> — DataLTA <b>{esc(fmt_date(header.get("DataLTA","")))}</b>
      </div>
    </div>
    """

body = f"""
    <div class="wrap">
      {header_cards}
      {event_table}
    </div>
    """

return f"<!doctype html><html><head><meta charset='utf-8'><title>LTA Reader</title><style>{css}</style></head><body>{hero}{body}<script>{js}</script></body></html>"


# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="LTA Reader: report HTML organizzato (anche da .p7m).")
    ap.add_argument("files", nargs="+", help="File LTA .xml/.xsi oppure firmati .p7m")
    ap.add_argument("--open", action="store_true", help="Apri il report nel browser a fine generazione")
    ap.add_argument("--no-cents", action="store_true", help="CorrispettivoLordo NON in centesimi (non dividere per 100)")
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
                try:
                    os.unlink(temp_to_cleanup)
                except Exception:
                    pass
            continue

        # check root tag (expected: LTA_Giornaliera)
        rt = localname(root.tag)
        if rt not in ("LTA_Giornaliera", "LTA_GiornalieraCA", "LTA_Giornaliera_SIAE"):
            # non blocco: lo visualizzo comunque
            pass

        data = parse_lta(root)

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".lta.html"))

        html_doc = build_lta_html(data, p.name, cents_mode=cents_mode)
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

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


# -------------------------
# XML helpers (namespace-safe)
# -------------------------
def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag and "}" in tag else (tag or "")

def children(elem: Optional[ET.Element], name: str) -> List[ET.Element]:
    if elem is None:
        return []
    return [c for c in list(elem) if localname(c.tag) == name]

def child(elem: Optional[ET.Element], name: str) -> Optional[ET.Element]:
    if elem is None:
        return None
    for c in list(elem):
        if localname(c.tag) == name:
            return c
    return None

def findall_anywhere(elem: ET.Element, name: str) -> List[ET.Element]:
    out = []
    for e in elem.iter():
        if localname(e.tag) == name:
            out.append(e)
    return out

def text_path(elem: Optional[ET.Element], path: str, default: str = "") -> str:
    cur = elem
    for p in path.split("/"):
        cur = child(cur, p)
        if cur is None:
            return default
    return (cur.text or "").strip() if cur.text else default

def esc(s: str) -> str:
    return html.escape(s or "")

def int_or0(s: str) -> int:
    s = (s or "").strip()
    return int(s) if re.fullmatch(r"-?\d+", s) else 0


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

def money_from_int(value: str, cents_mode: bool = True) -> str:
    """
    CorrispettivoLordo nello XSD è xs:string ma quasi sempre numerico.
    Per default lo tratto come centesimi (cents_mode=True). Se nel tuo caso è in euro interi: usa --no-cents.
    """
    s = (value or "").strip()
    if not s:
        return ""
    if not re.fullmatch(r"-?\d+", s):
        return esc(s)
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
# LTA semantics (from lta.xsd comments)
# -------------------------
STATUS_LABELS = {
    "VT": "Valido (tradizionale)",
    "VD": "Valido (digitale)",
    "ZT": "Accesso automatizzato (trad.)",
    "ZD": "Accesso automatizzato (dig.)",
    "MT": "Accesso manuale (trad.)",
    "MD": "Accesso manuale (dig.)",
    "DT": "Daspato (trad.)",
    "DD": "Daspato (dig.)",
    "FT": "Denuncia furto (trad.)",
    "FD": "Denuncia furto (dig.)",
    "AT": "Annullato (trad.)",
    "AD": "Annullato (dig.)",
    "BT": "Black list (trad.)",
    "BD": "Black list (dig.)",
}

GROUPS = [
    ("Validi", {"VT", "VD"}, "ok"),
    ("Automatizzati", {"ZT", "ZD"}, "info"),
    ("Manuali", {"MT", "MD"}, "info"),
    ("Daspati", {"DT", "DD"}, "warn"),
    ("Furto", {"FT", "FD"}, "warn"),
    ("Annullati", {"AT", "AD"}, "warn"),
    ("Blacklist", {"BT", "BD"}, "warn"),
]

EVENT_ATTRS = [
    ("CF Organizzatore", "CFOrganizzatore"),
    ("Codice Locale", "CodiceLocale"),
    ("Data Evento", "DataEvento"),
    ("Ora Evento", "OraEvento"),
    ("Titolo", "Titolo"),
    ("Genere", "TipoGenere"),
    ("Data Apertura", "DataApertura"),
    ("Ora Apertura", "OraApertura"),
]

TITLE_CORE_COLS = [
    ("Stato", "Stato"),
    ("Tipo titolo", "TipoTitolo"),
    ("Corrispettivo", "CorrispettivoLordo"),
    ("Emissione", "__emissione__"),
    ("LTA", "__lta__"),
    ("Ingresso", "__ingresso__"),
    ("Sistema", "SistemaEmissione"),
    ("Ordine", "CodiceOrdine"),
    ("Posto", "Posto"),
    ("Supporto", "__supporto__"),
    ("Partecipante", "__partecipante__"),
]


# -------------------------
# Parsing
# -------------------------
def parse_lta(root: ET.Element) -> Dict:
    """
    Parses LTA structure per lta.xsd (namespace-safe).
    Returns dict with header + events list.
    """
    header = {
        "Root": localname(root.tag),
        "SistemaCA": root.attrib.get("SistemaCA", ""),
        "CFTitolareCA": root.attrib.get("CFTitolareCA", ""),
        "DataLTA": root.attrib.get("DataLTA", ""),
    }

    # find events robustly
    events_nodes = children(root, "LTA_Evento")
    if not events_nodes:
        # fallback: search anywhere (still no raw xml rendering; just to parse)
        events_nodes = findall_anywhere(root, "LTA_Evento")

    events = []
    for ev in events_nodes:
        ev_attrs = dict(ev.attrib or {})
        supporti = [dict(s.attrib or {}) for s in children(ev, "Supporto")]
        titoli = []
        for t in children(ev, "TitoloAccesso"):
            ta = dict(t.attrib or {})
            p = child(t, "Partecipante")
            part = {}
            if p is not None:
                part = {
                    "Nome": text_path(p, "Nome"),
                    "Cognome": text_path(p, "Cognome"),
                    "DataNascita": text_path(p, "DataNascita"),
                    "LuogoNascita": text_path(p, "LuogoNascita"),
                }
            titoli.append({"attrs": ta, "partecipante": part})
        events.append({"attrs": ev_attrs, "supporti": supporti, "titoli": titoli})

    return {"header": header, "events": events}


def event_counts(event: Dict) -> Dict:
    st = Counter()
    td = Counter()
    gruppi = {name: 0 for name, _, _ in GROUPS}
    ingressi = 0
    abb = 0
    ann = 0
    sum_corr = 0
    sum_corr_count = 0

    for t in event["titoli"]:
        a = t["attrs"]
        stato = (a.get("Stato", "") or "").strip()
        if stato:
            st[stato] += 1
            td[stato[-1:]] += 1 if stato[-1:] in ("T", "D") else 0
            for name, codes, _ in GROUPS:
                if stato in codes:
                    gruppi[name] += 1
        if (a.get("DataIngresso", "") or "").strip() or (a.get("OraIngresso", "") or "").strip():
            ingressi += 1
        if (a.get("Abbonamento", "N") or "N").strip().upper() == "S":
            abb += 1
        if (a.get("Annullamento", "N") or "N").strip().upper() == "S":
            ann += 1

        corr = (a.get("CorrispettivoLordo", "") or "").strip()
        if re.fullmatch(r"-?\d+", corr):
            sum_corr += int(corr)
            sum_corr_count += 1

    # support mismatch: referenced supporto not defined
    defined = set((s.get("CodSupportoId",""), s.get("TipoSupportoId","")) for s in event["supporti"])
    ref_pairs = set()
    for t in event["titoli"]:
        a = t["attrs"]
        cod = (a.get("CodSupporto","") or "").strip()
        ids = (a.get("IdSupporto","") or "").strip()
        # in XSD, Supporto has TipoSupportoId + CodSupportoId,
        # while TitoloAccesso has CodSupporto + IdSupporto:
        # we can only check CodSupporto against CodSupportoId loosely.
        ref_pairs.add((cod, ids))

    return {
        "status": st,
        "td": td,
        "groups": gruppi,
        "ingressi": ingressi,
        "abbonamenti": abb,
        "annullamenti": ann,
        "sum_corr_int": sum_corr,
        "sum_corr_count": sum_corr_count,
        "defined_supporti": defined,
        "ref_supporti": ref_pairs,
    }


def file_dashboard(data: Dict) -> Dict:
    n_events = len(data["events"])
    n_supporti = sum(len(e["supporti"]) for e in data["events"])
    n_titoli = sum(len(e["titoli"]) for e in data["events"])

    st = Counter()
    gruppi = {name: 0 for name, _, _ in GROUPS}
    ingressi = 0
    abb = 0
    ann = 0
    sum_corr = 0
    sum_corr_count = 0

    for e in data["events"]:
        c = event_counts(e)
        st.update(c["status"])
        for k, v in c["groups"].items():
            gruppi[k] += v
        ingressi += c["ingressi"]
        abb += c["abbonamenti"]
        ann += c["annullamenti"]
        sum_corr += c["sum_corr_int"]
        sum_corr_count += c["sum_corr_count"]

    return {
        "n_events": n_events,
        "n_supporti": n_supporti,
        "n_titoli": n_titoli,
        "status": st,
        "groups": gruppi,
        "ingressi": ingressi,
        "abbonamenti": abb,
        "annullamenti": ann,
        "sum_corr_int": sum_corr,
        "sum_corr_count": sum_corr_count,
    }


def data_quality_issues(event: Dict) -> List[str]:
    issues = []
    # support definitions
    if not event["supporti"]:
        issues.append("Evento senza alcun elemento Supporto (lo XSD lo prevede minOccurs=1).")

    for i, t in enumerate(event["titoli"], start=1):
        a = t["attrs"]
        # required fields sanity checks (present but empty)
        required = ["SistemaEmissione","CartaAttivazione","ProgressivoFiscale","SigilloFiscale","DataEmissione","OraEmissione",
                    "DataLTA","OraLTA","TipoTitolo","CodiceOrdine","CorrispettivoLordo","CodSupporto","IdSupporto","Stato"]
        missing = [k for k in required if not (a.get(k, "") or "").strip()]
        if missing:
            issues.append(f"TitoloAccesso #{i}: campi obbligatori vuoti: {', '.join(missing)}")

        ann = (a.get("Annullamento", "N") or "N").strip().upper()
        if ann == "S":
            if not (a.get("DataANN","") or "").strip() or not (a.get("OraANN","") or "").strip():
                issues.append(f"TitoloAccesso #{i}: Annullamento=S ma DataANN/OraANN mancanti.")
            if not (a.get("ProgressivoFiscaleANN","") or "").strip():
                issues.append(f"TitoloAccesso #{i}: Annullamento=S ma ProgressivoFiscaleANN mancante (consigliato).")

        abb = (a.get("Abbonamento", "N") or "N").strip().upper()
        if abb == "S":
            if not (a.get("CFAbbonamento","") or "").strip():
                issues.append(f"TitoloAccesso #{i}: Abbonamento=S ma CFAbbonamento mancante.")
            if not (a.get("CodiceAbbonamento","") or "").strip():
                issues.append(f"TitoloAccesso #{i}: Abbonamento=S ma CodiceAbbonamento mancante.")
    return issues


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

def sort_key(val: str) -> str:
    v = (val or "").strip()
    if re.fullmatch(r"\d{8}", v):
        return v
    if re.fullmatch(r"\d{4}(\d{2})?", v):
        return v
    if re.fullmatch(r"-?\d+", v):
        return v
    return v.lower()

def build_html(data: Dict, file_title: str, cents_mode: bool) -> str:
    header = data["header"]
    dash = file_dashboard(data)
    events = data["events"]

    # status tables for dashboard
    status_rows = ""
    for code, cnt in dash["status"].most_common(20):
        status_rows += f"<tr><td><code>{esc(code)}</code></td><td>{cnt}</td><td class='muted'>{esc(STATUS_LABELS.get(code,'(non previsto nello XSD)'))}</td></tr>"
    if not status_rows:
        status_rows = "<tr><td colspan='3' class='muted'>(nessuno stato)</td></tr>"

    group_rows = ""
    for name, _, _kind in GROUPS:
        group_rows += f"<tr><td>{esc(name)}</td><td>{dash['groups'].get(name,0)}</td></tr>"

    # total corrispettivo (best effort)
    tot_corr = money_from_int(str(dash["sum_corr_int"]), cents_mode) if dash["sum_corr_count"] else ""

    # event table
    ev_rows = []
    ev_details = []

    for idx, ev in enumerate(events, start=1):
        a = ev["attrs"]
        counts = event_counts(ev)

        titolo = a.get("Titolo", "")
        gen = a.get("TipoGenere", "")
        cf = a.get("CFOrganizzatore", "")
        codloc = a.get("CodiceLocale", "")
        data_ev = a.get("DataEvento", "")
        ora_ev = a.get("OraEvento", "")
        ap_d = a.get("DataApertura", "")
        ap_o = a.get("OraApertura", "")

        tot_titles = len(ev["titoli"])
        tot_supporti = len(ev["supporti"])
        validi = counts["groups"].get("Validi", 0)
        annullati = counts["groups"].get("Annullati", 0)
        blacklist = counts["groups"].get("Blacklist", 0)

        filtro = " ".join([
            str(idx), titolo, gen, cf, codloc, data_ev, ora_ev, ap_d, ap_o,
            " ".join([t["attrs"].get("SistemaEmissione","") for t in ev["titoli"]]),
            " ".join([t["attrs"].get("TipoTitolo","") for t in ev["titoli"]]),
            " ".join([t["attrs"].get("Stato","") for t in ev["titoli"]]),
        ]).lower()

        def td(display: str, sk: str = "") -> str:
            return f"<td data-sort='{esc(sk or sort_key(display))}'>{esc(display)}</td>"

        ev_rows.append(
            f"<tr class='eventrow' data-filter='{esc(filtro)}' data-idx='{idx}'>"
            + td(str(idx), str(idx))
            + td(fmt_date(data_ev), data_ev)
            + td(fmt_time(ora_ev), ora_ev)
            + td(codloc, codloc)
            + td(gen, gen.lower())
            + td(titolo, titolo.lower())
            + td(cf, cf)
            + td(str(tot_supporti), str(tot_supporti))
            + td(str(tot_titles), str(tot_titles))
            + td(str(counts["ingressi"]), str(counts["ingressi"]))
            + td(str(validi), str(validi))
            + td(str(annullati), str(annullati))
            + td(str(blacklist), str(blacklist))
            + "</tr>"
        )

        # Info evento (card)
        info_list = ""
        for lbl, key in EVENT_ATTRS:
            v = a.get(key, "")
            if "Data" in key:
                v = fmt_date(v)
            if "Ora" in key:
                v = fmt_time(v)
            info_list += f"<li><b>{esc(lbl)}</b>: {esc(v)}</li>"

        # Supporti table
        sup_body = ""
        for s in ev["supporti"]:
            sup_body += f"<tr><td>{esc(s.get('TipoSupportoId',''))}</td><td><code>{esc(s.get('CodSupportoId',''))}</code></td></tr>"
        if not sup_body:
            sup_body = "<tr><td colspan='2' class='muted'>(nessun supporto)</td></tr>"

        supporti_table = f"""
        <div class="tablewrap small">
          <table class="mini main">
            <thead><tr><th>Tipo supporto</th><th>Codice</th></tr></thead>
            <tbody>{sup_body}</tbody>
          </table>
        </div>
        """

        # DQ issues
        issues = data_quality_issues(ev)
        issues_html = ""
        if issues:
            issues_html = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in issues[:25]) + "</ul>"
            if len(issues) > 25:
                issues_html += f"<div class='muted'>… e altre {len(issues)-25} segnalazioni</div>"
        else:
            issues_html = "<div class='muted'>(nessuna anomalia evidente)</div>"

        # Event KPIs
        kpi_html = (
                kpi(str(tot_titles), "Titoli")
                + kpi(str(counts["ingressi"]), "Ingressi")
                + kpi(str(validi), "Validi")
                + kpi(str(counts["groups"].get("Automatizzati",0)), "Automatizzati")
                + kpi(str(counts["groups"].get("Manuali",0)), "Manuali")
                + kpi(str(annullati), "Annullati")
                + kpi(str(blacklist), "Blacklist")
        )
        ev_sum_corr = money_from_int(str(counts["sum_corr_int"]), cents_mode) if counts["sum_corr_count"] else ""

        # Titoli table (expandable rows)
        tit_rows = []
        for j, t in enumerate(ev["titoli"], start=1):
            ta = t["attrs"]
            p = t.get("partecipante", {}) or {}

            stato = (ta.get("Stato","") or "").strip()
            stato_label = STATUS_LABELS.get(stato, "")
            # badge kind
            kind = "neutral"
            if stato in {"VT","VD"}:
                kind = "ok"
            elif stato in {"ZT","ZD","MT","MD"}:
                kind = "info"
            elif stato in {"AT","AD","BT","BD","DT","DD","FT","FD"}:
                kind = "warn"
            stato_html = badge(stato or "n/d", kind) + (f" <span class='muted'>({esc(stato_label)})</span>" if stato_label else "")

            emissione = f"{fmt_date(ta.get('DataEmissione',''))} {fmt_time(ta.get('OraEmissione',''))}".strip()
            lta = f"{fmt_date(ta.get('DataLTA',''))} {fmt_time(ta.get('OraLTA',''))}".strip()
            ingresso = f"{fmt_date(ta.get('DataIngresso',''))} {fmt_time(ta.get('OraIngresso',''))}".strip()

            supporto = f"{(ta.get('CodSupporto','') or '').strip()} / {(ta.get('IdSupporto','') or '').strip()}".strip(" /")
            partecipante = ""
            if p.get("Nome") or p.get("Cognome"):
                partecipante = f"{p.get('Cognome','')} {p.get('Nome','')}".strip()

            corr_disp = money_from_int(ta.get("CorrispettivoLordo",""), cents_mode)

            row_blob = " ".join([
                str(idx), str(j), stato, stato_label,
                ta.get("TipoTitolo",""), ta.get("SistemaEmissione",""),
                ta.get("CodiceOrdine",""), ta.get("Posto",""),
                ta.get("CodSupporto",""), ta.get("IdSupporto",""),
                partecipante,
                emissione, lta, ingresso,
            ]).lower()

            def tdd(display: str, sk: str = "") -> str:
                return f"<td data-sort='{esc(sk or sort_key(display))}'>{display}</td>"

            core_cells = []
            core_cells.append(f"<td data-sort='{j}'>{j}</td>")
            core_cells.append(f"<td data-sort='{esc(stato)}'>{stato_html}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('TipoTitolo','').lower())}'>{esc(ta.get('TipoTitolo',''))}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('CorrispettivoLordo',''))}'>{corr_disp}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('DataEmissione','')+ta.get('OraEmissione',''))}'>{esc(emissione)}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('DataLTA','')+ta.get('OraLTA',''))}'>{esc(lta)}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('DataIngresso','')+ta.get('OraIngresso',''))}'>{esc(ingresso)}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('SistemaEmissione','').lower())}'>{esc(ta.get('SistemaEmissione',''))}</td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('CodiceOrdine',''))}'><code>{esc(ta.get('CodiceOrdine',''))}</code></td>")
            core_cells.append(f"<td data-sort='{esc(ta.get('Posto',''))}'>{esc(ta.get('Posto',''))}</td>")
            core_cells.append(f"<td data-sort='{esc(supporto)}'><code>{esc(supporto)}</code></td>")
            core_cells.append(f"<td data-sort='{esc(partecipante.lower())}'>{esc(partecipante)}</td>")
            core_cells.append("<td><button class='btn-sm' type='button' onclick='toggleDetail(this)'>Dettagli</button></td>")

            tit_rows.append(
                f"<tr class='titrow' data-filter='{esc(row_blob)}' data-ev='{idx}'>"
                + "".join(core_cells) +
                "</tr>"
            )

            # Detail sections (organized)
            emissione_kv = {
                "SistemaEmissione": ta.get("SistemaEmissione",""),
                "CartaAttivazione": ta.get("CartaAttivazione",""),
                "ProgressivoFiscale": ta.get("ProgressivoFiscale",""),
                "SigilloFiscale": ta.get("SigilloFiscale",""),
                "DataEmissione": fmt_date(ta.get("DataEmissione","")),
                "OraEmissione": fmt_time(ta.get("OraEmissione","")),
            }
            lta_kv = {
                "DataLTA": fmt_date(ta.get("DataLTA","")),
                "OraLTA": fmt_time(ta.get("OraLTA","")),
                "DataIngresso": fmt_date(ta.get("DataIngresso","")),
                "OraIngresso": fmt_time(ta.get("OraIngresso","")),
                "Stato": ta.get("Stato",""),
            }
            ordine_kv = {
                "TipoTitolo": ta.get("TipoTitolo",""),
                "CodiceOrdine": ta.get("CodiceOrdine",""),
                "Posto": ta.get("Posto",""),
                "CorrispettivoLordo": money_from_int(ta.get("CorrispettivoLordo",""), cents_mode),
            }
            abb_kv = {
                "Abbonamento": ta.get("Abbonamento","N"),
                "CFAbbonamento": ta.get("CFAbbonamento",""),
                "CodiceAbbonamento": ta.get("CodiceAbbonamento",""),
                "ProgressivoAbbonamento": ta.get("ProgressivoAbbonamento",""),
                "QEventiAbilitati": ta.get("QEventiAbilitati",""),
            }
            ann_kv = {
                "Annullamento": ta.get("Annullamento","N"),
                "DataANN": fmt_date(ta.get("DataANN","")),
                "OraANN": fmt_time(ta.get("OraANN","")),
                "CartaAttivazioneANN": ta.get("CartaAttivazioneANN",""),
                "ProgressivoFiscaleANN": ta.get("ProgressivoFiscaleANN",""),
                "SigilloFiscaleANN": ta.get("SigilloFiscaleANN",""),
            }
            sup_kv = {
                "CodSupporto": ta.get("CodSupporto",""),
                "IdSupporto": ta.get("IdSupporto",""),
                "IdSupAlt": ta.get("IdSupAlt",""),
            }
            part_kv = {
                "Cognome": p.get("Cognome",""),
                "Nome": p.get("Nome",""),
                "DataNascita": fmt_date(p.get("DataNascita","")),
                "LuogoNascita": p.get("LuogoNascita",""),
            }

            def kv_table(d: Dict[str, str]) -> str:
                rows = ""
                for k, v in d.items():
                    vv = v if v is not None else ""
                    rows += f"<tr><td class='k'><code>{esc(k)}</code></td><td class='v'>{esc(vv)}</td></tr>"
                return f"<table class='kv'><tbody>{rows}</tbody></table>"

            detail_html = f"""
            <div class="detailgrid">
              <div class="dcard"><div class="dtitle">Emissione</div>{kv_table(emissione_kv)}</div>
              <div class="dcard"><div class="dtitle">LTA / Ingresso</div>{kv_table(lta_kv)}</div>
              <div class="dcard"><div class="dtitle">Titolo / Ordine</div>{kv_table(ordine_kv)}</div>
              <div class="dcard"><div class="dtitle">Abbonamento</div>{kv_table(abb_kv)}</div>
              <div class="dcard"><div class="dtitle">Annullamento</div>{kv_table(ann_kv)}</div>
              <div class="dcard"><div class="dtitle">Supporto</div>{kv_table(sup_kv)}</div>
              <div class="dcard"><div class="dtitle">Partecipante</div>{kv_table(part_kv)}</div>
            </div>
            """

            tit_rows.append(
                f"<tr class='detailrow' style='display:none' data-ev='{idx}'>"
                f"<td colspan='13'>{detail_html}</td>"
                f"</tr>"
            )

        tit_table = f"""
        <div class="subbar">
          <div>
            <h4>Titoli accesso</h4>
            <div class="muted">Clicca “Dettagli” per vedere tutti i campi organizzati per sezioni.</div>
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
                <th class="sortable" data-type="text">Tipo titolo</th>
                <th class="sortable" data-type="num">Corrispettivo</th>
                <th class="sortable" data-type="text">Emissione</th>
                <th class="sortable" data-type="text">LTA</th>
                <th class="sortable" data-type="text">Ingresso</th>
                <th class="sortable" data-type="text">Sistema</th>
                <th class="sortable" data-type="text">Ordine</th>
                <th class="sortable" data-type="text">Posto</th>
                <th class="sortable" data-type="text">Supporto</th>
                <th class="sortable" data-type="text">Partecipante</th>
                <th> </th>
              </tr>
            </thead>
            <tbody>
              {''.join(tit_rows) if tit_rows else "<tr><td colspan='13' class='muted'>(nessun TitoloAccesso)</td></tr>"}
            </tbody>
          </table>
        </div>
        """

        pills = (
                badge(f"Supporti {tot_supporti}", "neutral") + " "
                + badge(f"Titoli {tot_titles}", "info") + " "
                + badge(f"Ingressi {counts['ingressi']}", "ok") + " "
                + badge(f"Annullati {annullati}", "warn")
        )

        ev_details.append(f"""
        <details class="event" data-filter="{esc(filtro)}" data-idx="{idx}">
          <summary>
            Evento {idx}: <b>{esc(fmt_date(data_ev))} {esc(fmt_time(ora_ev))}</b> — Locale <code>{esc(codloc)}</code> — {esc(titolo)} {pills}
          </summary>
          <div class="pad">
            <div class="grid2">
              <div class="card2">
                <h3>Info evento</h3>
                <ul>{info_list}</ul>
              </div>

              <div class="card2">
                <h3>Indicatori</h3>
                <div class="kpirow">{kpi_html}</div>
                <div class="muted" style="margin-top:10px;">
                  Somma corrispettivi (best effort): <b>{esc(ev_sum_corr) if ev_sum_corr else "n/d"}</b>
                </div>
              </div>
            </div>

            <div class="grid2" style="margin-top:12px;">
              <div class="card2">
                <h3>Supporti</h3>
                {supporti_table}
              </div>
              <div class="card2">
                <h3>Qualità dati</h3>
                {issues_html}
              </div>
            </div>

            <div style="margin-top:12px;">
              {tit_table}
            </div>
          </div>
        </details>
        """)

    # page-level layout
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
    .badge.bad{background:#ffe4e4;border-color:#ffc2c2;color:#8a1f1f;}
    .kpirow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:6px;}
    .kpi{border:1px solid var(--line);border-radius:12px;padding:10px;background:#fbfcff;}
    .knum{font-size:18px;font-weight:900;}
    .klabel{color:var(--muted);font-size:12px;margin-top:2px;}
    .topline{display:flex;gap:12px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;}
    .right{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
    .search{width:min(620px, 92vw);padding:10px 12px;border:1px solid #d7dbe6;border-radius:12px;background:#fff;}
    .btn{padding:10px 12px;border-radius:12px;border:1px solid #d7dbe6;background:#fff;cursor:pointer;}
    .btn:hover{background:#f4f6fb;}
    .btn-sm{padding:7px 10px;border-radius:10px;border:1px solid #d7dbe6;background:#fff;cursor:pointer;font-size:12px;}
    .btn-sm:hover{background:#f4f6fb;}
    .mini-search{padding:8px 10px;border-radius:10px;border:1px solid #d7dbe6;background:#fff;min-width:280px;}
    .subbar{display:flex;gap:10px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;margin:6px 0 8px 0;}
    .subright{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
    .tablewrap{max-height:58vh;overflow:auto;border:1px solid var(--line);border-radius:14px;background:#fff;}
    .tablewrap.small{max-height:220px;}
    table{border-collapse:collapse;width:100%;font-size:13px;}
    th,td{border-bottom:1px solid #eef0f6;padding:8px 10px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fbfcff;font-weight:900;position:sticky;top:0;z-index:5;}
    .mini th,.mini td{font-size:12px;padding:6px 8px;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#b7bdcc;font-weight:900;}
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

      // reinserisci mantenendo la detailrow sotto la sua riga
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
      for(let i=0;i<rows.length;i++){
        const r = rows[i];
        if(!r.classList.contains('titrow')) continue;
        const detail = r.nextElementSibling && r.nextElementSibling.classList.contains('detailrow') ? r.nextElementSibling : null;
        const hay = norm(r.getAttribute('data-filter'));
        const show = (!q) ? true : hay.includes(q);
        r.style.display = show ? '' : 'none';
        if(detail && !show) detail.style.display = 'none';
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
        {esc(file_title)} — CF titolare <code>{esc(header.get("CFTitolareCA",""))}</code>
        — SistemaCA <code>{esc(header.get("SistemaCA",""))}</code>
        — DataLTA <b>{esc(fmt_date(header.get("DataLTA","")))}</b>
      </div>
    </div>
    """

    header_cards = f"""
    <div class="grid">
      <div class="card">
        <h2>Intestazione</h2>
        <ul>
          <li><b>Root</b>: <code>{esc(header.get("Root",""))}</code></li>
          <li><b>CF titolare</b>: <code>{esc(header.get("CFTitolareCA",""))}</code></li>
          <li><b>Sistema CA</b>: <code>{esc(header.get("SistemaCA",""))}</code></li>
          <li><b>Data LTA</b>: {esc(fmt_date(header.get("DataLTA","")))}</li>
        </ul>
      </div>

      <div class="card">
        <h2>Riepilogo</h2>
        <div class="kpirow">
          {kpi(str(dash["n_events"]), "Eventi")}
          {kpi(str(dash["n_supporti"]), "Supporti")}
          {kpi(str(dash["n_titoli"]), "Titoli")}
          {kpi(str(dash["ingressi"]), "Ingressi")}
          {kpi(str(dash["annullamenti"]), "Annullamento=S")}
          {kpi(str(dash["abbonamenti"]), "Abbonamento=S")}
        </div>
        <div class="muted" style="margin-top:10px;">
          Somma corrispettivi (best effort): <b>{esc(tot_corr) if tot_corr else "n/d"}</b>
        </div>
      </div>

      <div class="card">
        <h2>Distribuzione stati</h2>
        <div class="tablewrap small">
          <table class="mini main">
            <thead><tr><th>Stato</th><th>Q.tà</th><th>Descrizione</th></tr></thead>
            <tbody>{status_rows}</tbody>
          </table>
        </div>
        <div class="muted" style="margin-top:10px;">
          Gruppi:
          {" ".join(badge(f"{name}: {dash['groups'].get(name,0)}", kind) for name,_,kind in GROUPS)}
        </div>
      </div>
    </div>
    """

    event_table = f"""
    <div class="card" style="margin-top:12px;">
      <div class="topline">
        <div>
          <h2>Eventi ({len(events)})</h2>
          <div class="muted">Filtro globale (tabella + dettagli). Ordina cliccando le intestazioni.</div>
        </div>
        <div class="right">
          <input id="q" class="search" placeholder="Filtra per titolo, locale, CF, genere, stato, sistema..." />
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
              <th class="sortable" data-type="num">Supporti</th>
              <th class="sortable" data-type="num">Titoli</th>
              <th class="sortable" data-type="num">Ingressi</th>
              <th class="sortable" data-type="num">Validi</th>
              <th class="sortable" data-type="num">Annullati</th>
              <th class="sortable" data-type="num">Blacklist</th>
            </tr>
          </thead>
          <tbody id="evBody">
            {''.join(ev_rows) if ev_rows else "<tr><td colspan='13' class='muted'>(nessun evento)</td></tr>"}
          </tbody>
        </table>
      </div>

      <h3 style="margin-top:14px;">Dettaglio eventi</h3>
      {''.join(ev_details) if ev_details else "<div class='muted'>(nessun dettaglio)</div>"}
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
                try: os.unlink(temp_to_cleanup)
                except Exception: pass
            continue

        data = parse_lta(root)

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".lta.html"))

        doc = build_html(data, p.name, cents_mode=cents_mode)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(doc)

        print(f"OK: {in_path} -> {out_path}")

        if args.open:
            open_in_browser(out_path)

        if temp_to_cleanup:
            try: os.unlink(temp_to_cleanup)
            except Exception: pass


if __name__ == "__main__":
    main()

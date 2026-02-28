#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verifica consistenza LOG / LTA / RCA / RPM (sistemi emissione titoli - biglietterie).

Cosa controlla (in sintesi):
1) LOG <-> LTA
   - ogni emissione presente nel LOG deve avere un TitoloAccesso in LTA (chiave: SistemaEmissione+Carta+Progressivo+Sigillo)
   - i dati principali (TipoTitolo, CodiceOrdine, CodiceLocale, Data/Ora evento) devono coincidere
   - coerenza importi: LTA.CorrispettivoLordo == LOG.CorrispettivoLordo + LOG.Prevendita
2) Annullamenti
   - ogni transazione LOG di annullamento deve riferirsi ad un titolo originario esistente
   - in LTA il titolo originario deve risultare Annullamento="S" e i riferimenti ANN devono combaciare
3) LTA <-> RCA
   - riconteggio per stato (VT/VD/ZT/...) e confronto con i totali presenti nel RCA
4) LOG <-> RPM (mensile)
   - aggregazioni per evento/ordine/tipo titolo su emissioni e annullamenti e confronto con RPM (TitoliAccesso / TitoliAnnullati)
5) Controlli generali
   - duplicati su chiavi e sigilli fiscali
   - campi obbligatori mancanti

Output:
- genera un report HTML autosufficiente (senza dipendenze esterne) con riepilogo e dettagli.

Uso tipico:
    python verifica_consistenza_biglietteria.py --dir /percorso/file --out report.html

Oppure specificando i file:
    python verifica_consistenza_biglietteria.py --log LOG_...xsi --lta LTA_...xsi --rca RCA_...xsi --rpm RPM_...xsi --out report.html
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import os
import re
import sys
import traceback
import xml.etree.ElementTree as ET
import csv
import math
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, DefaultDict
from collections import defaultdict, Counter


# ---------------------------
# Utility / helpers
# ---------------------------

def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    s = str(value).strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        # alcuni campi potrebbero avere leading zeros o formati non numerici:
        # in tal caso restituisco None
        return None

# --- Helpers per controlli fiscali (ISI / IVA / omaggi) ---------------------------------------------

def _dec(value: Any) -> Decimal:
    """Converte un valore in Decimal in modo robusto (utile per evitare errori di floating point)."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(0)


def round_half_up(value: Decimal) -> int:
    """Arrotondamento commerciale (0.5 -> 1) anche per valori negativi."""
    if value >= 0:
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return -int((-value).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calc_quota_intr(amount_cents: int, perc_intr: int) -> int:
    """Quota intrattenimento (in cent) dato importo lordo e % intrattenimento."""
    return round_half_up(_dec(amount_cents) * _dec(perc_intr) / _dec(100))


def calc_base_intr_for_log(gross_intr_cents: int, iva: Decimal, isi: Decimal) -> int:
    """Imponibile intrattenimento da quota intrattenimento (approccio coerente con LOG: scorporo sul lordo e arrotondamento)."""
    denom = _dec(1) + iva + isi
    if denom == 0:
        return 0
    return round_half_up(_dec(gross_intr_cents) / denom)


def calc_base_sp(gross_sp_cents: int, iva: Decimal) -> int:
    """Imponibile spettacolo (solo IVA) da quota spettacolo."""
    denom = _dec(1) + iva
    if denom == 0:
        return 0
    return round_half_up(_dec(gross_sp_cents) / denom)


def calc_expected_iva_total_from_gross(gross_total_cents: int, perc_intr: int, iva: Decimal, isi: Decimal) -> int:
    """IVA totale attesa su un importo lordo (corrispettivo+prevendita) applicando scorpori/arrotondamenti."""
    quota_intr = calc_quota_intr(gross_total_cents, perc_intr)
    quota_sp = gross_total_cents - quota_intr

    base_intr = calc_base_intr_for_log(quota_intr, iva, isi)
    isi_amount = round_half_up(_dec(base_intr) * isi)
    iva_intr = quota_intr - base_intr - isi_amount

    base_sp = calc_base_sp(quota_sp, iva)
    iva_sp = quota_sp - base_sp

    return iva_intr + iva_sp


def calc_imponibile_intr_notional_from_corr(corr_cents: int, perc_intr: int, iva: Decimal, isi: Decimal) -> int:
    """Imponibile intrattenimento per omaggi eccedenti (su corrispettivo figurativo): residuale dopo IVA+ISI arrotondati."""
    gross_intr = calc_quota_intr(corr_cents, perc_intr)
    denom = _dec(1) + iva + isi
    if denom == 0:
        return gross_intr
    iva_intr = round_half_up(_dec(gross_intr) * iva / denom)
    isi_intr = round_half_up(_dec(gross_intr) * isi / denom)
    return gross_intr - iva_intr - isi_intr


def calc_imponibile_intr_round_for_threshold(corr_cents: int, perc_intr: int, iva: Decimal, isi: Decimal) -> int:
    """Imponibile (arrotondato) usato per verificare la soglia IVA omaggi (L. 50.000 ≈ €25,82)."""
    gross_intr = calc_quota_intr(corr_cents, perc_intr)
    return calc_base_intr_for_log(gross_intr, iva, isi)


OMAGGIO_TIPO_EXTRA = {"WX", "YX", "ZX"}  # da TAB. 3 (omaggio generico)


def is_omaggio_tipo_titolo(tipo: Optional[str]) -> bool:
    if not tipo:
        return False
    t = tipo.strip().upper()
    return t.startswith("O") or (t in OMAGGIO_TIPO_EXTRA)




def _text(el: Optional[ET.Element]) -> Optional[str]:
    if el is None or el.text is None:
        return None
    t = el.text.strip()
    return t if t != "" else None


def _read_xml(path: str) -> ET.Element:
    # ElementTree è "tollerante" con DOCTYPE e senza risoluzione DTD.
    tree = ET.parse(path)
    return tree.getroot()


def _file_mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def _safe_basename(path: str) -> str:
    return os.path.basename(path)


def _now_iso() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _key_tuple(*parts: Any) -> Tuple[Any, ...]:
    return tuple(parts)


def _fmt_money_cents(v: Optional[int]) -> str:
    if v is None:
        return ""
    # assumo importi in centesimi (come nei file d'esempio)
    euros = v / 100.0
    return f"{euros:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------
# Data structures
# ---------------------------

@dataclass(frozen=True)
class TicketKey:
    sistema: str
    carta: str
    progressivo: str
    sigillo: str

    def as_tuple(self) -> Tuple[str, str, str, str]:
        return (self.sistema, self.carta, self.progressivo, self.sigillo)

    def short(self) -> str:
        return f"{self.sistema}|{self.carta}|{self.progressivo}|{self.sigillo}"


@dataclass
class Issue:
    severity: str   # "ERROR" | "WARN" | "INFO"
    check: str
    message: str
    context: Dict[str, Any]


# ---------------------------
# Parsers
# ---------------------------

def parse_log(paths: Iterable[str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in paths:
        root = _read_xml(path)
        if root.tag != "LogTransazione":
            continue
        for tr in root.findall("Transazione"):
            titolo = tr.find("TitoloAccesso")
            if titolo is None:
                continue

            rec: Dict[str, Any] = {}
            rec["_file"] = _safe_basename(path)
            rec["_type"] = "LOG"
            # attributi Transazione
            rec.update(tr.attrib)

            rec["Annullamento"] = titolo.attrib.get("Annullamento")
            # sotto-elementi TitoloAccesso
            for tag in ["CorrispettivoLordo", "Prevendita", "IVACorrispettivo", "IVAPrevendita",
                        "CodiceLocale", "DataEvento", "OraEvento", "TipoGenere", "Titolo"]:
                rec[tag] = _text(titolo.find(tag))

            # normalizzo numerici
            for tag in ["CorrispettivoLordo", "Prevendita", "IVACorrispettivo", "IVAPrevendita", "ImponibileIntrattenimenti",
                        "NumeroProgressivo", "OriginaleAnnullato"]:
                if tag in rec:
                    rec[tag] = _to_int(rec[tag]) if tag not in ("NumeroProgressivo", "OriginaleAnnullato") else rec[tag]

            # chiave del titolo (per le emissioni è 1:1 con LTA)
            rec["ProgressivoFiscale"] = str(rec.get("NumeroProgressivo", "")).strip()
            rec_key = TicketKey(
                sistema=str(rec.get("SistemaEmissione", "")).strip(),
                carta=str(rec.get("CartaAttivazione", "")).strip(),
                progressivo=str(rec.get("ProgressivoFiscale", "")).strip(),
                sigillo=str(rec.get("SigilloFiscale", "")).strip(),
            )
            rec["__key"] = rec_key

            # chiave originale annullata (solo se presente)
            if rec.get("Annullamento") == "S":
                orig_prog = str(rec.get("OriginaleAnnullato", "")).strip()
                orig_carta = str(rec.get("CartaOriginaleAnnullato", "")).strip()
                if orig_prog and orig_carta:
                    rec["__orig_key"] = TicketKey(
                        sistema=rec_key.sistema,
                        carta=orig_carta,
                        progressivo=orig_prog,
                        sigillo=""  # il sigillo originale non è sempre presente qui
                    )
            records.append(rec)
    return records


def parse_lta(paths: Iterable[str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in paths:
        root = _read_xml(path)
        if root.tag != "LTA_Giornaliera":
            continue
        header = dict(root.attrib)
        for ev in root.findall("LTA_Evento"):
            ev_attr = dict(ev.attrib)
            for ta in ev.findall("TitoloAccesso"):
                rec: Dict[str, Any] = {}
                rec["_file"] = _safe_basename(path)
                rec["_type"] = "LTA"
                rec.update(header)
                # contesto evento
                rec["CFOrganizzatore"] = ev_attr.get("CFOrganizzatore")
                rec["CodiceLocale"] = ev_attr.get("CodiceLocale")
                rec["DataEvento"] = ev_attr.get("DataEvento")
                rec["OraEvento"] = ev_attr.get("OraEvento")
                rec["TipoGenere"] = ev_attr.get("TipoGenere")
                rec["TitoloEvento"] = ev_attr.get("Titolo")
                # attributi titolo
                rec.update(dict(ta.attrib))

                rec_key = TicketKey(
                    sistema=str(rec.get("SistemaEmissione", "")).strip(),
                    carta=str(rec.get("CartaAttivazione", "")).strip(),
                    progressivo=str(rec.get("ProgressivoFiscale", "")).strip(),
                    sigillo=str(rec.get("SigilloFiscale", "")).strip(),
                )
                rec["__key"] = rec_key
                records.append(rec)
    return records


# --- Aliquote TAB. 1 (CSV) ------------------------------------------------------------------------

def _parse_rate_list(raw: Optional[str]) -> List[Decimal]:
    if not raw:
        return []
    s = str(raw).strip()
    if not s or s in {"-", "—", "–"}:
        return []
    parts = [p.strip() for p in re.split(r"[|/]", s) if p.strip()]
    rates: List[Decimal] = []
    for p in parts:
        p = p.replace("%", "").strip()
        try:
            rates.append(_dec(p) / _dec(100))
        except Exception:
            continue
    # de-dup mantenendo ordine
    seen = set()
    out: List[Decimal] = []
    for r in rates:
        if r in seen:
            continue
        seen.add(r)
        out.append(r)
    return out


def load_aliquote_tab1(csv_path: str) -> Dict[str, Dict[str, Any]]:
    """Carica la TAB.1 (aliquote IVA/ISI per TipoGenere) da CSV.

    Output:
      { "61": {"descr": "...", "iva_rates": [Decimal('0.22')], "isi_rates":[Decimal('0.16')], ... }, ... }
    """
    out: Dict[str, Dict[str, Any]] = {}
    if not csv_path or not os.path.exists(csv_path):
        return out
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (row.get("Codice") or "").strip()
            if not code:
                continue
            esente_iva = str(row.get("Esente_IVA") or "").strip() == "1"

            iva_rates = _parse_rate_list(row.get("IVA_rates_%"))
            isi_rates = _parse_rate_list(row.get("ISI_rates_%"))

            if esente_iva:
                iva_rates = [Decimal(0)]

            out[code] = {
                "descr": (row.get("Descrizione") or "").strip(),
                "iva_rates": iva_rates,
                "isi_rates": isi_rates,
                "iva_variable": str(row.get("IVA_variable") or "").strip() == "1",
                "isi_raw": (row.get("ISI_raw") or "").strip(),
                "esente_iva": esente_iva,
            }
    return out



def parse_rca(paths: Iterable[str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in paths:
        root = _read_xml(path)
        if root.tag != "RiepilogoControlloAccessi":
            continue
        tit = root.find("Titolare")
        tit_info = {}
        if tit is not None:
            for c in list(tit):
                tit_info[c.tag] = _text(c)

        for ev in root.findall("Evento"):
            ev_info = {}
            for c in list(ev):
                if c.tag == "SistemaEmissione":
                    continue
                ev_info[c.tag] = _text(c)

            for se in ev.findall("SistemaEmissione"):
                se_code = _text(se.find("CodiceSistemaEmissione"))
                # Titoli
                for titoli in se.findall("Titoli"):
                    cod_ordine = _text(titoli.find("CodiceOrdinePosto"))
                    capienza = _text(titoli.find("Capienza"))
                    for tot in titoli.findall("TotaleTipoTitolo"):
                        rec: Dict[str, Any] = {}
                        rec["_file"] = _safe_basename(path)
                        rec["_type"] = "RCA"
                        rec.update(tit_info)
                        rec.update(ev_info)
                        rec["CodiceSistemaEmissione"] = se_code
                        rec["CodiceOrdinePosto"] = cod_ordine
                        rec["Capienza"] = capienza
                        rec["TipoTitolo"] = _text(tot.find("TipoTitolo"))
                        # campi numerici
                        for tag in [
                            "TotaleTitoliLTA",
                            "TotaleTitoliNoAccessoTradiz", "TotaleTitoliNoAccessoDigitali",
                            "TotaleTitoliAutomatizzatiTradiz", "TotaleTitoliAutomatizzatiDigitali",
                            "TotaleTitoliManualiTradiz", "TotaleTitoliManualiDigitali",
                            "TotaleTitoliAnnullatiTradiz", "TotaleTitoliAnnullatiDigitali",
                            "TotaleTitoliDaspatiTradiz", "TotaleTitoliDaspatiDigitali",
                            "TotaleTitoliRubatiTradiz", "TotaleTitoliRubatiDigitali",
                            "TotaleTitoliBLTradiz", "TotaleTitoliBLDigitali",
                        ]:
                            rec[tag] = _to_int(_text(tot.find(tag)))
                        records.append(rec)
    return records


def parse_rpm(paths: Iterable[str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in paths:
        root = _read_xml(path)
        if root.tag != "RiepilogoMensile":
            continue

        month = root.attrib.get("Mese")
        meta = dict(root.attrib)

        # Titolare
        titolare = root.find("Titolare")
        tit_info = {}
        if titolare is not None:
            tit_info = {
                "Titolare_Denominazione": _text(titolare.find("Denominazione")),
                "Titolare_CF": _text(titolare.find("CodiceFiscale")),
                "Titolare_SistemaEmissione": _text(titolare.find("SistemaEmissione")),
            }

        for org in root.findall("Organizzatore"):
            org_info = {
                "Organizzatore_Denominazione": _text(org.find("Denominazione")),
                "Organizzatore_CF": _text(org.find("CodiceFiscale")),
            }
            tipo_org = org.find("TipoOrganizzatore")
            if tipo_org is not None:
                org_info["TipoOrganizzatore"] = tipo_org.attrib.get("valore") or _text(tipo_org)

            for evento in org.findall("Evento"):
                event_info: Dict[str, Any] = {}
                intr = evento.find("Intrattenimento")
                if intr is not None:
                    tt = intr.find("TipoTassazione")
                    if tt is not None:
                        event_info["TipoTassazione"] = tt.attrib.get("valore") or _text(tt)
                    inc = intr.find("Incidenza")
                    if inc is not None:
                        event_info["Incidenza"] = _to_int(_text(inc)) or 0
                    imp = intr.find("ImponibileIntrattenimenti")
                    if imp is not None:
                        event_info["ImponibileIntrattenimenti"] = _to_int(_text(imp)) or 0

                loc = evento.find("Locale")
                if loc is not None:
                    event_info["DenominazioneLocale"] = _text(loc.find("Denominazione"))
                    event_info["CodiceLocale"] = _text(loc.find("CodiceLocale"))

                event_info["DataEvento"] = _text(evento.find("DataEvento"))
                event_info["OraEvento"] = _text(evento.find("OraEvento"))

                # MultiGenere: salvo il primo (per display)
                mg = evento.find("MultiGenere")
                if mg is not None:
                    event_info["TipoGenere"] = _text(mg.find("TipoGenere"))
                    to = mg.find("TitoliOpere")
                    if to is not None:
                        event_info["TitoloEvento"] = _text(to.find("Titolo"))

                for od in evento.findall("OrdineDiPosto"):
                    cod_ordine = _text(od.find("CodiceOrdine"))
                    capienza = _to_int(_text(od.find("Capienza"))) or 0
                    iva_ecc_omaggi = _to_int(_text(od.find("IVAEccedenteOmaggi"))) or 0

                    def _parse_nodes(nodes: List[ET.Element], kind: str) -> None:
                        for node in nodes:
                            rec: Dict[str, Any] = {}
                            rec["_file"] = _safe_basename(path)
                            rec["_type"] = "RPM"
                            rec["Mese"] = month
                            rec.update(meta)
                            rec.update(tit_info)
                            rec.update(org_info)
                            rec.update(event_info)
                            rec["CodiceOrdine"] = cod_ordine
                            rec["Capienza"] = capienza
                            rec["IVAEccedenteOmaggi"] = iva_ecc_omaggi
                            rec["kind"] = kind
                            rec["TipoTitolo"] = _text(node.find("TipoTitolo"))
                            for tag in ["Quantita", "CorrispettivoLordo", "Prevendita", "IVACorrispettivo", "IVAPrevendita", "ImportoPrestazione"]:
                                rec[tag] = _to_int(_text(node.find(tag)))
                            records.append(rec)

                    _parse_nodes(od.findall("TitoliAccesso"), "TitoliAccesso")
                    _parse_nodes(od.findall("TitoliAnnullati"), "TitoliAnnullati")
                    _parse_nodes(od.findall("TitoliAccessoIVAPreassolta"), "TitoliAccessoIVAPreassolta")
                    _parse_nodes(od.findall("TitoliIVAPreassoltaAnnullati"), "TitoliIVAPreassoltaAnnullati")

    return records


# ---------------------------
# Consistency checks
# ---------------------------

STATE_TO_RCA_FIELD = {
    "VT": "TotaleTitoliNoAccessoTradiz",
    "VD": "TotaleTitoliNoAccessoDigitali",
    "ZT": "TotaleTitoliAutomatizzatiTradiz",
    "ZD": "TotaleTitoliAutomatizzatiDigitali",
    "MT": "TotaleTitoliManualiTradiz",
    "MD": "TotaleTitoliManualiDigitali",
    "AT": "TotaleTitoliAnnullatiTradiz",
    "AD": "TotaleTitoliAnnullatiDigitali",
    "DT": "TotaleTitoliDaspatiTradiz",
    "DD": "TotaleTitoliDaspatiDigitali",
    "FT": "TotaleTitoliRubatiTradiz",
    "FD": "TotaleTitoliRubatiDigitali",
    "BT": "TotaleTitoliBLTradiz",
    "BD": "TotaleTitoliBLDigitali",
}


def _rca_key(rec: Dict[str, Any]) -> Tuple[str, str, str, str]:
    # key = (CodiceLocale, DataEvento, OraEvento, CodiceOrdinePosto, TipoTitolo)
    return (
        str(rec.get("CodiceLocale", "")).strip(),
        str(rec.get("DataEvento", "")).strip(),
        str(rec.get("OraEvento", "")).strip(),
        str(rec.get("CodiceOrdinePosto", "")).strip(),
        str(rec.get("TipoTitolo", "")).strip(),
    )


def _lta_group_key(rec: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    # key = (CodiceLocale, DataEvento, OraEvento, CodiceOrdine, TipoTitolo)
    return (
        str(rec.get("CodiceLocale", "")).strip(),
        str(rec.get("DataEvento", "")).strip(),
        str(rec.get("OraEvento", "")).strip(),
        str(rec.get("CodiceOrdine", "")).strip(),
        str(rec.get("TipoTitolo", "")).strip(),
    )


def _rpm_key(rec: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
    # key = (CodiceLocale, DataEvento, OraEvento, CodiceOrdine, TipoTitolo, kind)
    return (
        str(rec.get("CodiceLocale", "")).strip(),
        str(rec.get("DataEvento", "")).strip(),
        str(rec.get("OraEvento", "")).strip(),
        str(rec.get("CodiceOrdine", "")).strip(),
        str(rec.get("TipoTitolo", "")).strip(),
        str(rec.get("kind", "")).strip(),
    )


def _log_group_key(rec: Dict[str, Any], kind: str) -> Tuple[str, str, str, str, str, str]:
    return (
        str(rec.get("CodiceLocale", "")).strip(),
        str(rec.get("DataEvento", "")).strip(),
        str(rec.get("OraEvento", "")).strip(),
        str(rec.get("CodiceOrdine", "")).strip(),
        str(rec.get("TipoTitolo", "")).strip(),
        kind,
    )


def run_checks(log_recs: List[Dict[str, Any]],
               lta_recs: List[Dict[str, Any]],
               rca_recs: List[Dict[str, Any]],
               rpm_recs: List[Dict[str, Any]],
               tolleranza_importi: int = 0,
               aliquote_tab1: Optional[Dict[str, Dict[str, Any]]] = None,
               omaggi_pct_capienza: float = 5.0,
               omaggi_soglia_iva_cent: int = 2582
               ) -> Tuple[Dict[str, Any], List[Issue], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    issues: List[Issue] = []
    metrics: Dict[str, Any] = {}
    aliquote_tab1 = aliquote_tab1 or {}

    # Indexes
    log_emissions = [r for r in log_recs if r.get("Annullamento") == "N"]
    log_cancellations = [r for r in log_recs if r.get("Annullamento") == "S"]

    metrics["log_files"] = sorted({r["_file"] for r in log_recs})
    metrics["lta_files"] = sorted({r["_file"] for r in lta_recs})
    metrics["rca_files"] = sorted({r["_file"] for r in rca_recs})
    metrics["rpm_files"] = sorted({r["_file"] for r in rpm_recs})

    metrics["log_transactions_total"] = len(log_recs)
    metrics["log_emissions"] = len(log_emissions)
    metrics["log_cancellations"] = len(log_cancellations)
    metrics["lta_tickets_total"] = len(lta_recs)
    metrics["lta_annullati"] = sum(1 for r in lta_recs if r.get("Annullamento") == "S")
    metrics["rca_rows"] = len(rca_recs)
    metrics["rpm_rows"] = len(rpm_recs)

    # Duplicates: LOG keys (emissions only)
    def count_dups(keys: List[Tuple[str, str, str, str]]) -> List[Tuple[Tuple[str, str, str, str], int]]:
        c = Counter(keys)
        return [(k, v) for k, v in c.items() if v > 1]

    log_em_keys = [r["__key"].as_tuple() for r in log_emissions]
    for k, v in count_dups(log_em_keys):
        issues.append(Issue(
            severity="ERROR",
            check="Duplicati",
            message=f"Chiave titolo duplicata nel LOG (emissioni): {v} occorrenze",
            context={"key": "|".join(k)}
        ))

    lta_keys = [r["__key"].as_tuple() for r in lta_recs]
    for k, v in count_dups(lta_keys):
        issues.append(Issue(
            severity="ERROR",
            check="Duplicati",
            message=f"Chiave titolo duplicata in LTA: {v} occorrenze",
            context={"key": "|".join(k)}
        ))

    # Duplicates: SigilloFiscale should be unique per file-set
    for name, recs, keyfield in [
        ("LOG", log_recs, "SigilloFiscale"),
        ("LTA", lta_recs, "SigilloFiscale"),
    ]:
        sigs = [str(r.get(keyfield, "")).strip() for r in recs if str(r.get(keyfield, "")).strip()]
        dups = [(k, v) for k, v in Counter(sigs).items() if v > 1]
        for sig, v in dups:
            issues.append(Issue(
                severity="WARN",
                check="Duplicati",
                message=f"SigilloFiscale duplicato in {name}: {sig} (x{v})",
                context={"sigillo": sig, "count": v}
            ))

    # Build map LTA by key
    lta_by_key: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}
    for r in lta_recs:
        lta_by_key[r["__key"].as_tuple()] = r

    # LOG <-> LTA: presence and amount checks
    missing_in_lta = []
    mism_amount = []
    mism_fields = []

    for r in log_emissions:
        k = r["__key"].as_tuple()
        lta = lta_by_key.get(k)
        if not lta:
            missing_in_lta.append(r)
            continue

        # campo principali
        for field_pair in [
            ("TipoTitolo", "TipoTitolo"),
            ("CodiceOrdine", "CodiceOrdine"),
            ("CodiceLocale", "CodiceLocale"),
            ("DataEvento", "DataEvento"),
            ("OraEvento", "OraEvento"),
        ]:
            lf, tf = field_pair
            if str(r.get(lf, "")).strip() != str(lta.get(tf, "")).strip():
                mism_fields.append((r, lta, lf, r.get(lf), lta.get(tf)))

        # importi: LTA CorrispettivoLordo (totale) = LOG Corr + Prev
        lta_tot = _to_int(lta.get("CorrispettivoLordo"))
        log_corr = _to_int(r.get("CorrispettivoLordo")) or 0
        log_prev = _to_int(r.get("Prevendita")) or 0
        if lta_tot is not None and (log_corr + log_prev) != lta_tot:
            mism_amount.append((r, lta, log_corr, log_prev, lta_tot))

    for r in missing_in_lta:
        issues.append(Issue(
            severity="ERROR",
            check="LOG_vs_LTA",
            message="Titolo presente nel LOG (emissione) ma mancante in LTA",
            context={
                "key": r["__key"].short(),
                "TipoTitolo": r.get("TipoTitolo"),
                "DataEvento": r.get("DataEvento"),
                "OraEvento": r.get("OraEvento"),
                "CodiceLocale": r.get("CodiceLocale"),
                "CodiceOrdine": r.get("CodiceOrdine"),
                "file": r.get("_file"),
            }
        ))

    # Extra in LTA vs LOG emissions
    log_em_key_set = set(log_em_keys)
    for r in lta_recs:
        k = r["__key"].as_tuple()
        if k not in log_em_key_set:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_LTA",
                message="Titolo presente in LTA ma non trovato nel LOG (emissioni)",
                context={"key": r["__key"].short(), "file": r.get("_file")}
            ))

    for (r, lta, lf, lv, tv) in mism_fields:
        issues.append(Issue(
            severity="ERROR",
            check="LOG_vs_LTA",
            message=f"Mismatch campo {lf} tra LOG e LTA",
            context={
                "key": r["__key"].short(),
                "field": lf,
                "LOG": lv,
                "LTA": tv,
                "log_file": r.get("_file"),
                "lta_file": lta.get("_file"),
            }
        ))

    for (r, lta, corr, prev, lta_tot) in mism_amount:
        issues.append(Issue(
            severity="ERROR",
            check="Importi_LOG_vs_LTA",
            message="Mismatch importi: LTA.CorrispettivoLordo != LOG.CorrispettivoLordo + LOG.Prevendita",
            context={
                "key": r["__key"].short(),
                "LOG_Corrispettivo": corr,
                "LOG_Prevendita": prev,
                "LOG_Totale": corr + prev,
                "LTA_CorrispettivoLordo": lta_tot,
            }
        ))

    # Annullamenti
    # Index LOG cancellation by cancellation-key and by "original key" (sistema + carta originale + prog originale)
    log_can_by_key: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {r["__key"].as_tuple(): r for r in log_cancellations}
    log_can_by_orig: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for r in log_cancellations:
        sistema = str(r.get("SistemaEmissione", "")).strip()
        carta_orig = str(r.get("CartaOriginaleAnnullato", "")).strip()
        prog_orig = str(r.get("OriginaleAnnullato", "")).strip()
        if sistema and carta_orig and prog_orig:
            log_can_by_orig[(sistema, carta_orig, prog_orig)] = r

    log_em_by_triplet = {(r["__key"].sistema, r["__key"].carta, r["__key"].progressivo): r for r in log_emissions}

    # LOG cancellation must refer to existing original
    for r in log_cancellations:
        sistema = str(r.get("SistemaEmissione", "")).strip()
        carta_orig = str(r.get("CartaOriginaleAnnullato", "")).strip()
        prog_orig = str(r.get("OriginaleAnnullato", "")).strip()
        if not (carta_orig and prog_orig):
            issues.append(Issue(
                severity="ERROR",
                check="Annullamenti",
                message="Transazione di annullamento LOG senza riferimenti all'originale (CartaOriginaleAnnullato/OriginaleAnnullato)",
                context={"key_ann": r["__key"].short(), "file": r.get("_file")}
            ))
            continue
        if (sistema, carta_orig, prog_orig) not in log_em_by_triplet:
            issues.append(Issue(
                severity="ERROR",
                check="Annullamenti",
                message="Transazione di annullamento LOG riferita ad un titolo originale non trovato tra le emissioni LOG",
                context={
                    "key_ann": r["__key"].short(),
                    "orig_triplet": f"{sistema}|{carta_orig}|{prog_orig}",
                    "file": r.get("_file"),
                }
            ))

        # in LTA l'originale deve essere marcato annullato
        # per individuare il record LTA uso la chiave completa (serve il sigillo originale). Lo cerco in LOG emissione.
        orig_em = log_em_by_triplet.get((sistema, carta_orig, prog_orig))
        if orig_em is None:
            continue
        orig_full_key = orig_em["__key"].as_tuple()
        lta_orig = lta_by_key.get(orig_full_key)
        if lta_orig is None:
            issues.append(Issue(
                severity="ERROR",
                check="Annullamenti",
                message="Titolo originale (da LOG) non trovato in LTA (atteso annullato)",
                context={"orig_key": "|".join(orig_full_key), "key_ann": r["__key"].short()}
            ))
            continue
        if lta_orig.get("Annullamento") != "S":
            issues.append(Issue(
                severity="ERROR",
                check="Annullamenti",
                message="Titolo originale presente in LTA ma non risulta Annullamento='S'",
                context={"orig_key": lta_orig["__key"].short(), "key_ann": r["__key"].short()}
            ))
        # confronta riferimenti ANN
        for (field_lta, field_log) in [
            ("CartaAttivazioneANN", "CartaAttivazione"),
            ("ProgressivoFiscaleANN", "ProgressivoFiscale"),
            ("SigilloFiscaleANN", "SigilloFiscale"),
        ]:
            lv = str(lta_orig.get(field_lta, "")).strip()
            rv = str(r.get(field_log, "")).strip()
            if lv and rv and lv != rv:
                issues.append(Issue(
                    severity="ERROR",
                    check="Annullamenti",
                    message=f"Mismatch riferimento annullamento (LTA.{field_lta} != LOG.{field_log})",
                    context={"orig_key": lta_orig["__key"].short(), "LTA": lv, "LOG": rv}
                ))

    # LTA annulled tickets must have matching LOG cancellation
    for r in lta_recs:
        if r.get("Annullamento") != "S":
            continue
        # campi obbligatori
        for f in ["DataANN", "OraANN", "CartaAttivazioneANN", "ProgressivoFiscaleANN", "SigilloFiscaleANN"]:
            if not str(r.get(f, "")).strip():
                issues.append(Issue(
                    severity="ERROR",
                    check="Annullamenti",
                    message="Titolo annullato in LTA senza tutti i campi ANN valorizzati",
                    context={"key": r["__key"].short(), "missing_field": f, "file": r.get("_file")}
                ))
        # trova transazione annullamento nel LOG
        sistema = str(r.get("SistemaEmissione", "")).strip()
        carta_ann = str(r.get("CartaAttivazioneANN", "")).strip()
        prog_ann = str(r.get("ProgressivoFiscaleANN", "")).strip()
        sig_ann = str(r.get("SigilloFiscaleANN", "")).strip()
        if sistema and carta_ann and prog_ann and sig_ann:
            can_key = TicketKey(sistema=sistema, carta=carta_ann, progressivo=prog_ann, sigillo=sig_ann).as_tuple()
            log_can = log_can_by_key.get(can_key)
            if log_can is None:
                issues.append(Issue(
                    severity="ERROR",
                    check="Annullamenti",
                    message="Titolo annullato in LTA ma transazione di annullamento non trovata nel LOG",
                    context={"key": r["__key"].short(), "expected_log_cancel_key": "|".join(can_key)}
                ))
            else:
                # verifica che LOG annullamento punti a questo originale
                orig_triplet = (sistema, str(r.get("CartaAttivazione", "")).strip(), str(r.get("ProgressivoFiscale", "")).strip())
                log_triplet = (sistema, str(log_can.get("CartaOriginaleAnnullato", "")).strip(), str(log_can.get("OriginaleAnnullato", "")).strip())
                if orig_triplet != log_triplet:
                    issues.append(Issue(
                        severity="ERROR",
                        check="Annullamenti",
                        message="La transazione LOG di annullamento trovata non punta allo stesso originale del titolo LTA",
                        context={
                            "lta_orig_triplet": "|".join(orig_triplet),
                            "log_orig_triplet": "|".join(log_triplet),
                            "key": r["__key"].short(),
                            "key_ann": log_can["__key"].short(),
                        }
                    ))

    # LTA <-> RCA
    # Compute counts from LTA
    lta_counts: Dict[Tuple[str, str, str, str, str], Dict[str, int]] = {}
    for r in lta_recs:
        gk = _lta_group_key(r)
        if gk not in lta_counts:
            # init all RCA fields
            lta_counts[gk] = {k: 0 for k in [
                "TotaleTitoliLTA",
                "TotaleTitoliNoAccessoTradiz", "TotaleTitoliNoAccessoDigitali",
                "TotaleTitoliAutomatizzatiTradiz", "TotaleTitoliAutomatizzatiDigitali",
                "TotaleTitoliManualiTradiz", "TotaleTitoliManualiDigitali",
                "TotaleTitoliAnnullatiTradiz", "TotaleTitoliAnnullatiDigitali",
                "TotaleTitoliDaspatiTradiz", "TotaleTitoliDaspatiDigitali",
                "TotaleTitoliRubatiTradiz", "TotaleTitoliRubatiDigitali",
                "TotaleTitoliBLTradiz", "TotaleTitoliBLDigitali",
            ]}
        lta_counts[gk]["TotaleTitoliLTA"] += 1
        stato = str(r.get("Stato", "")).strip()
        fld = STATE_TO_RCA_FIELD.get(stato)
        if fld is None:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RCA",
                message="Stato LTA non riconosciuto (non mappato in RCA)",
                context={"key": r["__key"].short(), "Stato": stato}
            ))
        else:
            lta_counts[gk][fld] += 1

    # RCA map
    rca_by_key: Dict[Tuple[str, str, str, str], Dict[str, Any]] = { _rca_key(r): r for r in rca_recs }

    # Compare each LTA group with RCA
    for gk, cnts in lta_counts.items():
        cod_loc, data_ev, ora_ev, cod_ordine, tipo = gk
        rkey = (cod_loc, data_ev, ora_ev, cod_ordine, tipo)
        rca = rca_by_key.get(rkey)
        if rca is None:
            issues.append(Issue(
                severity="ERROR",
                check="LTA_vs_RCA",
                message="Gruppo titoli calcolato da LTA non trovato in RCA",
                context={"group": {"CodiceLocale": cod_loc, "DataEvento": data_ev, "OraEvento": ora_ev, "CodiceOrdine": cod_ordine, "TipoTitolo": tipo}}
            ))
            continue
        # Compare fields
        for field, calc_val in cnts.items():
            rca_val = rca.get(field)
            if rca_val is None:
                continue
            if int(rca_val) != int(calc_val):
                issues.append(Issue(
                    severity="ERROR",
                    check="LTA_vs_RCA",
                    message=f"Mismatch conteggi {field} (RCA vs calcolo da LTA)",
                    context={
                        "group": {"CodiceLocale": cod_loc, "DataEvento": data_ev, "OraEvento": ora_ev, "CodiceOrdine": cod_ordine, "TipoTitolo": tipo},
                        "field": field,
                        "RCA": rca_val,
                        "LTA_calcolato": calc_val,
                        "rca_file": rca.get("_file"),
                    }
                ))

    # RCA rows without LTA group
    lta_group_set = set((k[0], k[1], k[2], k[3], k[4]) for k in lta_counts.keys())
    for rca in rca_recs:
        rk = _rca_key(rca)
        if rk not in lta_group_set:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RCA",
                message="Riga RCA senza corrispondenza in LTA (potrebbe essere OK se LTA mancante o giorni diversi)",
                context={"rca_key": {"CodiceLocale": rk[0], "DataEvento": rk[1], "OraEvento": rk[2], "CodiceOrdine": rk[3], "TipoTitolo": rk[4]}, "rca_file": rca.get("_file")}
            ))

    # RCA internal sum check
    for r in rca_recs:
        total = r.get("TotaleTitoliLTA")
        if total is None:
            continue
        s = 0
        for f in [
            "TotaleTitoliNoAccessoTradiz", "TotaleTitoliNoAccessoDigitali",
            "TotaleTitoliAutomatizzatiTradiz", "TotaleTitoliAutomatizzatiDigitali",
            "TotaleTitoliManualiTradiz", "TotaleTitoliManualiDigitali",
            "TotaleTitoliAnnullatiTradiz", "TotaleTitoliAnnullatiDigitali",
            "TotaleTitoliDaspatiTradiz", "TotaleTitoliDaspatiDigitali",
            "TotaleTitoliRubatiTradiz", "TotaleTitoliRubatiDigitali",
            "TotaleTitoliBLTradiz", "TotaleTitoliBLDigitali",
        ]:
            s += int(r.get(f) or 0)
        if int(total) != s:
            issues.append(Issue(
                severity="ERROR",
                check="RCA_interno",
                message="Somma categorie RCA != TotaleTitoliLTA",
                context={"rca_key": _rca_key(r), "TotaleTitoliLTA": total, "SommaCategorie": s, "file": r.get("_file")}
            ))

    # LOG <-> RPM
    # Aggregate LOG (emissions and cancellations)
    log_aggr: Dict[Tuple[str, str, str, str, str, str], Dict[str, int]] = {}
    for r in log_recs:
        kind = "TitoliAnnullati" if r.get("Annullamento") == "S" else "TitoliAccesso"
        gk = _log_group_key(r, kind)
        if gk not in log_aggr:
            log_aggr[gk] = {"Quantita": 0, "CorrispettivoLordo": 0, "Prevendita": 0, "IVACorrispettivo": 0, "IVAPrevendita": 0}
        log_aggr[gk]["Quantita"] += 1
        log_aggr[gk]["CorrispettivoLordo"] += _to_int(r.get("CorrispettivoLordo")) or 0
        log_aggr[gk]["Prevendita"] += _to_int(r.get("Prevendita")) or 0
        log_aggr[gk]["IVACorrispettivo"] += _to_int(r.get("IVACorrispettivo")) or 0
        log_aggr[gk]["IVAPrevendita"] += _to_int(r.get("IVAPrevendita")) or 0

    rpm_by_key: Dict[Tuple[str, str, str, str, str, str], Dict[str, Any]] = {}
    for r in rpm_recs:
        rpm_by_key[_rpm_key(r)] = r

    # Compare only groups where LOG has at least 1 transaction (avoid rumore)
    for gk, vals in log_aggr.items():
        rpm = rpm_by_key.get(gk)
        if rpm is None:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_RPM",
                message="Aggregato LOG non trovato in RPM",
                context={
                    "key": {"CodiceLocale": gk[0], "DataEvento": gk[1], "OraEvento": gk[2], "CodiceOrdine": gk[3], "TipoTitolo": gk[4], "kind": gk[5]},
                    "LOG": vals,
                }
            ))
            continue
        for f in ["Quantita", "CorrispettivoLordo", "Prevendita", "IVACorrispettivo", "IVAPrevendita"]:
            rpm_v = rpm.get(f)
            if rpm_v is None:
                continue
            if int(rpm_v) != int(vals.get(f, 0)):
                issues.append(Issue(
                    severity="ERROR",
                    check="LOG_vs_RPM",
                    message=f"Mismatch aggregato {f} (RPM vs LOG)",
                    context={
                        "key": {"CodiceLocale": gk[0], "DataEvento": gk[1], "OraEvento": gk[2], "CodiceOrdine": gk[3], "TipoTitolo": gk[4], "kind": gk[5]},
                        "RPM": int(rpm_v),
                        "LOG": int(vals.get(f, 0)),
                        "rpm_file": rpm.get("_file"),
                    }
                ))


    # Optional: RPM entries that have non-zero but no LOG.
    # Di default segnalo SOLO se l'evento/ordine è "in scope" (cioè presente nei LOG analizzati),
    # altrimenti è normale che un RPM mensile contenga righe non coperte da un singolo LOG giornaliero.
    log_aggr_keys = set(log_aggr.keys())
    log_scope_orders = set((k[0], k[1], k[2], k[3]) for k in log_aggr_keys)  # (loc,data,ora,ordine)

    extra_rpm_in_scope = 0
    extra_rpm_out_of_scope = 0

    for gk, rpm in rpm_by_key.items():
        # ignore zero rows
        if (rpm.get("Quantita") or 0) == 0 and (rpm.get("CorrispettivoLordo") or 0) == 0 and (rpm.get("Prevendita") or 0) == 0:
            continue
        if gk in log_aggr_keys:
            continue

        order_scope_key = (gk[0], gk[1], gk[2], gk[3])
        if order_scope_key in log_scope_orders:
            extra_rpm_in_scope += 1
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_RPM",
                message="Riga RPM con valori non-zero senza transazioni corrispondenti nel LOG (stesso evento/ordine)",
                context={
                    "key": {"CodiceLocale": gk[0], "DataEvento": gk[1], "OraEvento": gk[2], "CodiceOrdine": gk[3], "TipoTitolo": gk[4], "kind": gk[5]},
                    "RPM": {f: rpm.get(f) for f in ["Quantita","CorrispettivoLordo","Prevendita","IVACorrispettivo","IVAPrevendita"]},
                    "rpm_file": rpm.get("_file"),
                }
            ))
        else:
            extra_rpm_out_of_scope += 1

    metrics["rpm_extra_nonzero_in_scope"] = extra_rpm_in_scope
    metrics["rpm_extra_nonzero_out_of_scope_ignored"] = extra_rpm_out_of_scope


    # LTA <-> RPM sanity: quantities
    # Calcolo da LTA: totale titoli emessi (incl. annullati) e totale annullati, e confronto con RPM TitoliAccesso/TitoliAnnullati
    lta_qty_total: Dict[Tuple[str, str, str, str, str], int] = defaultdict(int)
    lta_qty_ann: Dict[Tuple[str, str, str, str, str], int] = defaultdict(int)
    for r in lta_recs:
        g = _lta_group_key(r)  # (loc, data, ora, ordine, tipo)
        lta_qty_total[g] += 1
        if r.get("Annullamento") == "S":
            lta_qty_ann[g] += 1

    for g, q in lta_qty_total.items():
        loc, data, ora, ordine, tipo = g
        k_access = (loc, data, ora, ordine, tipo, "TitoliAccesso")
        rpm_acc = rpm_by_key.get(k_access)
        if rpm_acc and (rpm_acc.get("Quantita") is not None) and int(rpm_acc["Quantita"]) != int(q):
            issues.append(Issue(
                severity="ERROR",
                check="LTA_vs_RPM",
                message="Quantità TitoliAccesso in RPM diversa dal conteggio titoli in LTA (incl. annullati)",
                context={"group": {"CodiceLocale": loc, "DataEvento": data, "OraEvento": ora, "CodiceOrdine": ordine, "TipoTitolo": tipo},
                         "RPM_Quantita": rpm_acc.get("Quantita"), "LTA_count": q, "rpm_file": rpm_acc.get("_file")}
            ))
        # annulled
        q_ann = lta_qty_ann.get(g, 0)
        k_ann = (loc, data, ora, ordine, tipo, "TitoliAnnullati")
        rpm_ann = rpm_by_key.get(k_ann)
        if rpm_ann:
            if int(rpm_ann.get("Quantita") or 0) != int(q_ann):
                issues.append(Issue(
                    severity="ERROR",
                    check="LTA_vs_RPM",
                    message="Quantità TitoliAnnullati in RPM diversa dal conteggio annullati in LTA",
                    context={"group": {"CodiceLocale": loc, "DataEvento": data, "OraEvento": ora, "CodiceOrdine": ordine, "TipoTitolo": tipo},
                             "RPM_Quantita": rpm_ann.get("Quantita"), "LTA_annullati": q_ann, "rpm_file": rpm_ann.get("_file")}
                ))
        else:
            if q_ann > 0:
                issues.append(Issue(
                    severity="ERROR",
                    check="LTA_vs_RPM",
                    message="A LTA risultano annullati ma manca la riga TitoliAnnullati in RPM",
                    context={"group": {"CodiceLocale": loc, "DataEvento": data, "OraEvento": ora, "CodiceOrdine": ordine, "TipoTitolo": tipo},
                             "LTA_annullati": q_ann}
                ))


    # --- Controlli fiscali (ISI / eccedenza omaggi) ------------------------------------------------
    fiscal_details: Dict[str, Any] = {
        "config": {
            "omaggi_pct_capienza": omaggi_pct_capienza,
            "omaggi_soglia_iva_cent": omaggi_soglia_iva_cent,
        },
        "events": [],
        "orders": [],
    }

    skipped_checks: set = set()

    if not aliquote_tab1:
        # Senza TAB.1 non possiamo ricalcolare correttamente ISI/IVA
        issues.append(Issue(check="Aliquote_TAB1", severity="WARN", message="TAB.1 aliquote (aliquote_tab1.csv) non caricata: controlli fiscali ISI/IVA limitati."))
        skipped_checks.update({"ISI_LOG", "ISI_RPM", "IVA_Omaggi_Ecc"})
    else:
        # Copertura TipoGenere -> aliquote
        genre_in_log = {str(r.get("TipoGenere") or "").strip() for r in log_recs if str(r.get("TipoGenere") or "").strip()}
        missing_genres = sorted([g for g in genre_in_log if g not in aliquote_tab1])
        if missing_genres:
            issues.append(Issue(check="Aliquote_TAB1", severity="WARN", message=f"TipoGenere presenti nei LOG ma non trovati in TAB.1: {', '.join(missing_genres)}", context={"TipoGenere": missing_genres}))

        # Indici RPM per evento/ordine
        # (Limitiamo i controlli fiscali agli eventi presenti nei LOG caricati)
        scope_events = {(str(lr.get("CodiceLocale") or ""), str(lr.get("DataEvento") or ""), str(lr.get("OraEvento") or "")) for lr in log_recs}

        rpm_event_info: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        rpm_order_info: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}
        rpm_titles_by_order: Dict[Tuple[str, str, str, str], List[Dict[str, Any]]] = defaultdict(list)

        for r in rpm_recs:
            ek = (str(r.get("CodiceLocale") or ""), str(r.get("DataEvento") or ""), str(r.get("OraEvento") or ""))
            if ek not in scope_events:
                continue
            ok = (ek[0], ek[1], ek[2], str(r.get("CodiceOrdine") or ""))
            if ek not in rpm_event_info:
                rpm_event_info[ek] = {
                    "TipoTassazione": str(r.get("TipoTassazione") or ""),
                    "Incidenza": int(r.get("Incidenza") or 0),
                    "ImponibileIntrattenimenti": int(r.get("ImponibileIntrattenimenti") or 0),
                }
            if ok not in rpm_order_info:
                rpm_order_info[ok] = {
                    "Capienza": int(r.get("Capienza") or 0),
                    "IVAEccedenteOmaggi": int(r.get("IVAEccedenteOmaggi") or 0),
                }
            rpm_titles_by_order[ok].append(r)

        # LOG: base netta intrattenimenti e omaggi netti per ordine
        base_net_by_event: Dict[Tuple[str, str, str], int] = defaultdict(int)
        omaggi_net_by_order: Dict[Tuple[str, str, str, str], int] = defaultdict(int)
        log_by_event: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
        genre_counts_by_event: Dict[Tuple[str, str, str], Counter] = defaultdict(Counter)

        for lr in log_recs:
            ek = (str(lr.get("CodiceLocale") or ""), str(lr.get("DataEvento") or ""), str(lr.get("OraEvento") or ""))
            ok = (ek[0], ek[1], ek[2], str(lr.get("CodiceOrdine") or ""))
            sign = -1 if str(lr.get("Annullamento") or "").upper() == "S" else 1

            base_net_by_event[ek] += sign * int(lr.get("ImponibileIntrattenimenti") or 0)
            if is_omaggio_tipo_titolo(lr.get("TipoTitolo")):
                omaggi_net_by_order[ok] += sign

            gross = int(lr.get("CorrispettivoLordo") or 0) + int(lr.get("Prevendita") or 0)
            if gross > 0:
                tg = str(lr.get("TipoGenere") or "").strip()
                if tg:
                    genre_counts_by_event[ek][tg] += 1
            log_by_event[ek].append(lr)

        # Selezione aliquote per evento (gestisce eventuali IVA/ISI variabili)
        def _pick_perc_intr(ek: Tuple[str, str, str]) -> int:
            info = rpm_event_info.get(ek)
            if info and info.get("Incidenza") is not None:
                return int(info.get("Incidenza") or 0)
            # fallback: se l'evento è "I" nei LOG, assumo 100
            for lr in log_by_event.get(ek, []):
                if str(lr.get("TipoTassazione") or "").upper() == "I":
                    return 100
            return 0

        def _select_rates_for_event(ek: Tuple[str, str, str]) -> Tuple[Optional[str], Optional[Decimal], Optional[Decimal], str]:
            perc_intr = _pick_perc_intr(ek)
            # preferisco il TipoGenere più frequente a pagamento nel LOG
            tg = genre_counts_by_event.get(ek, Counter()).most_common(1)[0][0] if genre_counts_by_event.get(ek) else ""
            if not tg:
                # fallback: primo TipoGenere trovato nei LOG
                for lr in log_by_event.get(ek, []):
                    tg = str(lr.get("TipoGenere") or "").strip()
                    if tg:
                        break
            if not tg:
                return None, None, None, "TipoGenere non determinabile dai LOG"

            info = aliquote_tab1.get(tg)
            if not info:
                return tg, None, None, f"TipoGenere {tg} non presente in TAB.1"

            iva_candidates: List[Decimal] = list(info.get("iva_rates") or [Decimal(0)])
            isi_candidates: List[Decimal] = list(info.get("isi_rates") or [Decimal(0)])

            if len(iva_candidates) == 1 and len(isi_candidates) == 1:
                return tg, iva_candidates[0], isi_candidates[0], ""

            # Fit su un piccolo campione di transazioni LOG con importo > 0
            samples = [r for r in log_by_event.get(ek, []) if (int(r.get("CorrispettivoLordo") or 0) + int(r.get("Prevendita") or 0)) > 0][:5]
            best: Optional[Tuple[int, Decimal, Decimal]] = None
            for iva in iva_candidates:
                for isi in isi_candidates:
                    err = 0
                    for lr in samples:
                        gross = int(lr.get("CorrispettivoLordo") or 0) + int(lr.get("Prevendita") or 0)
                        quota_intr = calc_quota_intr(gross, perc_intr)
                        exp_base = calc_base_intr_for_log(quota_intr, iva, isi)
                        exp_iva = calc_expected_iva_total_from_gross(gross, perc_intr, iva, isi)

                        obs_base = int(lr.get("ImponibileIntrattenimenti") or 0)
                        obs_iva = int(lr.get("IVACorrispettivo") or 0) + int(lr.get("IVAPrevendita") or 0)
                        err += abs(exp_base - obs_base) + abs(exp_iva - obs_iva)

                    if best is None or err < best[0]:
                        best = (err, iva, isi)

            if best is None:
                return tg, iva_candidates[0], isi_candidates[0], "Selezione aliquote: fallback"

            err, iva, isi = best
            note = f"Aliquote variabili: selezione per fit su LOG (err={err})"
            return tg, iva, isi, note

        rates_by_event: Dict[Tuple[str, str, str], Tuple[Optional[str], Optional[Decimal], Optional[Decimal], str]] = {}
        for ek in set(list(rpm_event_info.keys()) + list(log_by_event.keys())):
            rates_by_event[ek] = _select_rates_for_event(ek)

        # 1) Ricalcolo ISI/IVA su LOG (calcolo-ISI.txt)
        for lr in log_recs:
            ek = (str(lr.get("CodiceLocale") or ""), str(lr.get("DataEvento") or ""), str(lr.get("OraEvento") or ""))
            tg, iva, isi, note = rates_by_event.get(ek, (None, None, None, ""))
            if iva is None or isi is None:
                continue

            perc_intr = _pick_perc_intr(ek)
            gross_total = int(lr.get("CorrispettivoLordo") or 0) + int(lr.get("Prevendita") or 0)
            if gross_total <= 0:
                continue

            quota_intr = calc_quota_intr(gross_total, perc_intr)
            exp_base_intr = calc_base_intr_for_log(quota_intr, iva, isi)
            exp_iva_total = calc_expected_iva_total_from_gross(gross_total, perc_intr, iva, isi)

            obs_base_intr = int(lr.get("ImponibileIntrattenimenti") or 0)
            obs_iva_total = int(lr.get("IVACorrispettivo") or 0) + int(lr.get("IVAPrevendita") or 0)

            if abs(exp_base_intr - obs_base_intr) > 1:
                issues.append(Issue(check="ISI_LOG", severity="ERROR",
                                    message=f"ImponibileIntrattenimenti LOG non coerente con ricalcolo: atteso {exp_base_intr}, trovato {obs_base_intr}. {note}".strip(),
                                    context={"log_key": str(_log_key(lr))}))
            if abs(exp_iva_total - obs_iva_total) > 1:
                issues.append(Issue(check="ISI_LOG", severity="ERROR",
                                    message=f"IVA totale LOG non coerente con ricalcolo: atteso {exp_iva_total}, trovato {obs_iva_total}. {note}".strip(),
                                    context={"log_key": str(_log_key(lr))}))

        # 2) Omaggi eccedenti (5% capienza) e ImponibileIntrattenimenti evento in RPM
        #    e 3) IVA eccedenza omaggi (con soglia valore unitario intrattenimento: €25,82 -> omaggi_soglia_iva_cent)
        order_rows: List[Dict[str, Any]] = []

        for ok, info in rpm_order_info.items():
            ek = (ok[0], ok[1], ok[2])
            event = rpm_event_info.get(ek, {})
            tipo_tass = str(event.get("TipoTassazione") or "")
            perc_intr = int(event.get("Incidenza") or 0)

            tg, iva, isi, note_rates = rates_by_event.get(ek, (None, None, None, ""))
            if iva is None or isi is None:
                # senza aliquote non posso calcolare imponibile notionale né soglia
                continue

            capienza = int(info.get("Capienza") or 0)
            iva_ecc_rpm = int(info.get("IVAEccedenteOmaggi") or 0)

            omaggi_net = int(omaggi_net_by_order.get(ok, 0))
            limite = int(math.floor((capienza * omaggi_pct_capienza) / 100.0 + 1e-9)) if capienza > 0 else 0
            eccedenza = max(0, omaggi_net - limite)

            # Titolo di riferimento (a pagamento) da RPM per determinare IVA corrispettivo unitario
            ref_tipo = None
            ref_corr_unit = None
            ref_iva_corr_unit = None

            candidates = [r for r in rpm_titles_by_order.get(ok, []) if str(r.get("kind") or "") == "TitoliAccesso" and int(r.get("Quantita") or 0) > 0 and int(r.get("CorrispettivoLordo") or 0) > 0]
            if candidates:
                # preferisco "I*" (intero), altrimenti quello col corrispettivo unitario maggiore
                def unit_corr(rr: Dict[str, Any]) -> float:
                    q = int(rr.get("Quantita") or 1)
                    return (int(rr.get("CorrispettivoLordo") or 0) / q) if q else 0.0

                interi = [r for r in candidates if str(r.get("TipoTitolo") or "").upper().startswith("I")]
                chosen = max(interi or candidates, key=unit_corr)

                q = int(chosen.get("Quantita") or 1)
                ref_tipo = str(chosen.get("TipoTitolo") or "")
                ref_corr_unit = int(round(int(chosen.get("CorrispettivoLordo") or 0) / q)) if q else None
                ref_iva_corr_unit = int(round(int(chosen.get("IVACorrispettivo") or 0) / q)) if q else None

            imponibile_ref = None
            if ref_corr_unit is not None:
                imponibile_ref = calc_imponibile_intr_round_for_threshold(ref_corr_unit, perc_intr, iva, isi)

            iva_ecc_attesa: Optional[int]
            note = note_rates

            if eccedenza <= 0:
                iva_ecc_attesa = 0
            else:
                if tipo_tass.upper() == "I" and imponibile_ref is not None and imponibile_ref <= omaggi_soglia_iva_cent:
                    # Regola IVA intrattenimenti: non dovuta se valore unitario <= soglia
                    iva_ecc_attesa = 0
                elif ref_iva_corr_unit is not None:
                    iva_ecc_attesa = eccedenza * ref_iva_corr_unit
                else:
                    iva_ecc_attesa = None
                    note = (note + " | " if note else "") + "Manca titolo di riferimento a pagamento: IVA eccedenza non calcolabile"

            # Base notionale ISI per omaggi eccedenti (solo quota intrattenimento del corrispettivo)
            base_omaggi_ecc = None
            if eccedenza > 0 and ref_corr_unit is not None:
                base_unit = calc_imponibile_intr_notional_from_corr(ref_corr_unit, perc_intr, iva, isi)
                base_omaggi_ecc = eccedenza * base_unit

            order_rows.append({
                "CodiceLocale": ok[0],
                "DataEvento": ok[1],
                "OraEvento": ok[2],
                "CodiceOrdine": ok[3],
                "TipoTassazione": tipo_tass,
                "Incidenza": perc_intr,
                "TipoGenere": tg or "",
                "IVA_rate": float(iva) if iva is not None else None,
                "ISI_rate": float(isi) if isi is not None else None,
                "Capienza": capienza,
                "Omaggi_net": omaggi_net,
                "Limite_omaggi": limite,
                "Eccedenza_omaggi": eccedenza,
                "Titolo_rif": ref_tipo,
                "Corrispettivo_rif_unit": ref_corr_unit,
                "Imponibile_rif_unit": imponibile_ref,
                "IVACorrispettivo_rif_unit": ref_iva_corr_unit,
                "IVAEccedenteOmaggi_attesa": iva_ecc_attesa,
                "IVAEccedenteOmaggi_rpm": iva_ecc_rpm,
                "BaseOmaggiEcc_ISI": base_omaggi_ecc,
                "Note": note,
            })

        # Evento: confronto ImponibileIntrattenimenti RPM vs LOG + BaseOmaggiEcc
        event_rows: List[Dict[str, Any]] = []
        orders_by_event: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
        for row in order_rows:
            orders_by_event[(row["CodiceLocale"], row["DataEvento"], row["OraEvento"])].append(row)

        for ek, e_info in rpm_event_info.items():
            rpm_base_evento = int(e_info.get("ImponibileIntrattenimenti") or 0)
            tipo_tass = str(e_info.get("TipoTassazione") or "")
            perc_intr = int(e_info.get("Incidenza") or 0)

            base_log = int(base_net_by_event.get(ek, 0))
            base_omaggi = 0
            missing_orders = 0
            missing_eccedenza = 0

            for row in orders_by_event.get(ek, []):
                ecc = int(row.get("Eccedenza_omaggi") or 0)
                if ecc <= 0:
                    continue
                if row.get("BaseOmaggiEcc_ISI") is None:
                    missing_orders += 1
                    missing_eccedenza += ecc
                else:
                    base_omaggi += int(row.get("BaseOmaggiEcc_ISI") or 0)

            base_atteso_parziale = base_log + base_omaggi
            delta = rpm_base_evento - base_atteso_parziale

            note = ""
            if missing_eccedenza > 0:
                # Non ho il prezzo di riferimento per calcolare la base omaggi: non verificabile al 100%
                base_unit_inferita = int(round(delta / missing_eccedenza)) if missing_eccedenza else None
                note = f"Verifica parziale: manca riferimento prezzo per {missing_eccedenza} omaggi eccedenti. Base unit inferita ~{base_unit_inferita} cent" if base_unit_inferita is not None else "Verifica parziale: manca riferimento prezzo per omaggi eccedenti"
                issues.append(Issue(check="ISI_RPM", severity="WARN",
                                    message=f"{note}. ImponibileIntrattenimenti RPM={rpm_base_evento}, LOG={base_log}, BaseOmaggiEcc calcolata={base_omaggi}, delta residuo={delta}.",
                                    context={"evento": f"{ek[0]}|{ek[1]}|{ek[2]}"}))
            else:
                if delta != 0:
                    issues.append(Issue(check="ISI_RPM", severity="ERROR",
                                        message=f"ImponibileIntrattenimenti RPM non coerente: atteso {base_atteso_parziale} (=LOG {base_log} + BaseOmaggiEcc {base_omaggi}), trovato {rpm_base_evento} (delta {delta}).",
                                        context={"evento": f"{ek[0]}|{ek[1]}|{ek[2]}"}))

            # Check IVA ecc omaggi
            for row in orders_by_event.get(ek, []):
                att = row.get("IVAEccedenteOmaggi_attesa")
                if att is None:
                    # se RPM valorizza comunque, segnalo
                    if int(row.get("IVAEccedenteOmaggi_rpm") or 0) != 0:
                        issues.append(Issue(check="IVA_Omaggi_Ecc", severity="WARN",
                                            message="IVAEccedenteOmaggi presente in RPM ma non calcolabile per mancanza dati di riferimento.",
                                            context={"ordine": f"{row['CodiceLocale']}|{row['DataEvento']}|{row['OraEvento']}|{row['CodiceOrdine']}"}))
                    continue
                if int(row.get("IVAEccedenteOmaggi_rpm") or 0) != int(att):
                    issues.append(Issue(check="IVA_Omaggi_Ecc", severity="ERROR",
                                        message=f"IVAEccedenteOmaggi non coerente: atteso {att}, trovato {int(row.get('IVAEccedenteOmaggi_rpm') or 0)}. "
                                                f"(Eccedenza={int(row.get('Eccedenza_omaggi') or 0)}, soglia={omaggi_soglia_iva_cent})",
                                        context={"ordine": f"{row['CodiceLocale']}|{row['DataEvento']}|{row['OraEvento']}|{row['CodiceOrdine']}"}))

            # Row evento per report
            tg, iva, isi, note_rates = rates_by_event.get(ek, (None, None, None, ""))
            event_rows.append({
                "CodiceLocale": ek[0],
                "DataEvento": ek[1],
                "OraEvento": ek[2],
                "TipoTassazione": tipo_tass,
                "Incidenza": perc_intr,
                "TipoGenere": tg or "",
                "IVA_rate": float(iva) if iva is not None else None,
                "ISI_rate": float(isi) if isi is not None else None,
                "Imponibile_LOG_net": base_log,
                "BaseOmaggiEcc_ISI": base_omaggi,
                "Imponibile_atteso_parziale": base_atteso_parziale,
                "Imponibile_RPM": rpm_base_evento,
                "Delta": delta,
                "Note": note,
            })

        fiscal_details["events"] = event_rows
        fiscal_details["orders"] = order_rows

    # --- fine controlli fiscali --------------------------------------------------------------------


    # Scoreboard + elenco controlli eseguiti (inclusi quelli con 0 issue)
    per_check: Dict[str, Counter] = defaultdict(Counter)
    for iss in issues:
        per_check[iss.check][iss.severity] += 1

    check_catalog: List[Dict[str, str]] = [
        {
            "id": "Duplicati",
            "title": "Duplicati SigilloFiscale",
            "description": "Unicità del SigilloFiscale su LOG e LTA.",
        },
        {
            "id": "LOG_vs_LTA",
            "title": "LOG vs LTA (quantità/attivi)",
            "description": "Confronto quantità emesse/annullate e titoli attivi per evento/ordine/titolo.",
        },
        {
            "id": "Importi_LOG_vs_LTA",
            "title": "LOG vs LTA (importi)",
            "description": "Confronto corrispettivo, prevendita e IVA tra LOG e LTA per evento/ordine/titolo.",
        },
        {
            "id": "Annullamenti",
            "title": "Annullamenti LOG vs RPM",
            "description": "Confronto quantità annullate tra LOG e RPM per evento/ordine/titolo.",
        },
        {
            "id": "LTA_vs_RCA",
            "title": "LTA vs RCA (quantità)",
            "description": "Confronto quantità tra LTA e RCA per evento/ordine/titolo (attivi).",
        },
        {
            "id": "RCA_interno",
            "title": "RCA (coerenza interna)",
            "description": "Verifica che RCA sia internamente coerente (somma dettaglio = totale).",
        },
        {
            "id": "LOG_vs_RPM",
            "title": "LOG vs RPM (importi/quantità)",
            "description": "Confronto importi tra LOG e RPM per evento/ordine/titolo.",
        },
        {
            "id": "LTA_vs_RPM",
            "title": "LTA vs RPM (quantità)",
            "description": "Confronto quantità tra LTA e RPM per evento/ordine/titolo.",
        },
        {
            "id": "Aliquote_TAB1",
            "title": "Copertura aliquote (TAB.1)",
            "description": "Verifica presenza in TAB.1 dei TipoGenere incontrati (IVA/ISI).",
        },
        {
            "id": "ISI_LOG",
            "title": "Ricalcolo ISI/IVA su LOG",
            "description": "Ricalcolo imponibile intrattenimenti e IVA totale per transazione (calcolo-ISI).",
        },
        {
            "id": "ISI_RPM",
            "title": "ImponibileIntrattenimenti RPM (evento)",
            "description": "ImponibileIntrattenimenti RPM = imponibile netto LOG + imponibile omaggi eccedenti (5% capienza).",
        },
        {
            "id": "IVA_Omaggi_Ecc",
            "title": "IVAEccedenteOmaggi RPM",
            "description": "IVA su omaggi eccedenti: regola 5% capienza + soglia valore unitario (intrattenimenti, €25,82).",
        },
    ]

    check_results: List[Dict[str, Any]] = []
    all_checks_counts: Dict[str, Dict[str, int]] = {}

    for c in check_catalog:
        cnt = per_check.get(c["id"], Counter())
        errors = int(cnt.get("ERROR", 0))
        warns = int(cnt.get("WARN", 0))
        infos = int(cnt.get("INFO", 0))

        if c["id"] in skipped_checks:
            status = "SKIP"
        else:
            status = "ERROR" if errors else ("WARN" if warns else "OK")

        check_results.append({
            "id": c["id"],
            "title": c["title"],
            "description": c["description"],
            "status": status,
            "errors": errors,
            "warnings": warns,
            "infos": infos,
        })

        all_checks_counts[c["id"]] = {"ERROR": errors, "WARN": warns, "INFO": infos}

    summary = {
        "total_issues": len(issues),
        "errors": sum(1 for i in issues if i.severity == "ERROR"),
        "warnings": sum(1 for i in issues if i.severity == "WARN"),
        "infos": sum(1 for i in issues if i.severity == "INFO"),
        "checks": all_checks_counts,  # include anche i check con 0 issue
        "check_results": check_results,
    }

    return summary, issues, metrics, check_results, fiscal_details



# ---------------------------
# HTML report generation
# ---------------------------

def _badge(sev: str) -> str:
    sev = sev.upper()
    cls = {
        "ERROR": "badge badge-red",
        "WARN": "badge badge-yellow",
        "INFO": "badge badge-blue",
        "OK": "badge badge-green",
        "SKIP": "badge badge-gray",
    }.get(sev, "badge")
    return f'<span class="{cls}">{html.escape(sev)}</span>'


def _render_kv_table(d: Dict[str, Any]) -> str:
    rows = []
    for k, v in d.items():
        rows.append(f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>")
    return "<table class='kv'>" + "".join(rows) + "</table>"


def _render_issues_table(issues: List[Issue]) -> str:
    rows = []
    for i, iss in enumerate(issues, 1):
        ctx = "<br/>".join(f"<b>{html.escape(str(k))}</b>: {html.escape(str(v))}" for k, v in iss.context.items())
        rows.append(
            "<tr>"
            f"<td class='n'>{i}</td>"
            f"<td>{_badge(iss.severity)}</td>"
            f"<td>{html.escape(iss.check)}</td>"
            f"<td>{html.escape(iss.message)}</td>"
            f"<td class='ctx'>{ctx}</td>"
            "</tr>"
        )
    return (
            "<table class='tbl'>"
            "<thead><tr>"
            "<th>#</th><th>Severità</th><th>Controllo</th><th>Messaggio</th><th>Dettagli</th>"
            "</tr></thead>"
            "<tbody>"
            + "".join(rows) +
            "</tbody></table>"
    )


def _render_check_results_table(check_results: List[Dict[str, Any]]) -> str:
    if not check_results:
        return "<p class='muted'>Nessun controllo registrato.</p>"
    rows_html: List[str] = []
    for cr in check_results:
        cid = html.escape(str(cr.get("id", "")))
        title = html.escape(str(cr.get("title", "")))
        desc = html.escape(str(cr.get("description", "")))
        status = str(cr.get("status", "OK"))
        rows_html.append(
            "<tr>"
            f"<td><code>{cid}</code></td>"
            f"<td><b>{title}</b><br><span class='muted'>{desc}</span></td>"
            f"<td>{_badge(status)}</td>"
            f"<td class='num'>{int(cr.get('errors', 0))}</td>"
            f"<td class='num'>{int(cr.get('warnings', 0))}</td>"
            f"<td class='num'>{int(cr.get('infos', 0))}</td>"
            "</tr>"
        )
    header = "<tr><th>Check</th><th>Descrizione</th><th>Esito</th><th>ERROR</th><th>WARN</th><th>INFO</th></tr>"
    return "<table class='issues'>" + header + "".join(rows_html) + "</table>"


def _render_rows_table(rows: List[Dict[str, Any]], cols: List[Tuple[str, str, str]]) -> str:
    """Render tabella HTML.

    cols: lista di (chiave, etichetta, tipo) dove tipo è:
      - 'text' (default)
      - 'int'
      - 'money' (cent)
      - 'pct' (0.22 -> 22%)
    """
    if not rows:
        return "<p class='muted'>Nessun dato.</p>"

    def fmt(val: Any, kind: str) -> str:
        if val is None:
            return ""
        if kind == "money":
            return _fmt_money_cents(int(val))
        if kind == "pct":
            try:
                return f"{float(val) * 100:.2f}%"
            except Exception:
                return str(val)
        if kind == "int":
            try:
                return str(int(val))
            except Exception:
                return str(val)
        return html.escape(str(val))

    header = "<tr>" + "".join(f"<th>{html.escape(label)}</th>" for _, label, _ in cols) + "</tr>"
    rows_html: List[str] = []
    for r in rows:
        tds = []
        for key, _, kind in cols:
            tds.append(f"<td>{fmt(r.get(key), kind)}</td>")
        rows_html.append("<tr>" + "".join(tds) + "</tr>")
    return "<table class='issues'>" + header + "".join(rows_html) + "</table>"



def build_html_report(out_path: str, summary: Dict[str, Any], metrics: Dict[str, Any], issues: List[Issue],
                      check_results: Optional[List[Dict[str, Any]]] = None,
                      fiscal_details: Optional[Dict[str, Any]] = None) -> None:

    errors = summary.get("errors", 0)
    warnings = summary.get("warnings", 0)
    infos = summary.get("infos", 0)
    total_issues = summary.get("total_issues", 0)

    status = "ERROR" if errors else ("WARN" if warnings else "OK")

    # Tabella "controlli eseguiti" (anche con 0 issue)
    cr = list(check_results or summary.get("check_results") or [])
    if not cr:
        # fallback: costruisco da summary["checks"] (senza descrizioni)
        checks = summary.get("checks", {}) or {}
        for check_name in sorted(checks.keys()):
            cnt = checks.get(check_name, {}) or {}
            e = int(cnt.get("ERROR", 0))
            w = int(cnt.get("WARN", 0))
            i = int(cnt.get("INFO", 0))
            c_status = "ERROR" if e else ("WARN" if w else "OK")
            cr.append({
                "id": check_name,
                "title": check_name,
                "description": "",
                "status": c_status,
                "errors": e,
                "warnings": w,
                "infos": i,
            })

    checks_table = _render_check_results_table(cr)

    # Sezione dettaglio controlli fiscali (se disponibile)
    fiscal_section = ""
    fd = fiscal_details or {}
    ev_rows = fd.get("events") or []
    ord_rows = fd.get("orders") or []
    if ev_rows or ord_rows:
        ev_cols = [
            ("CodiceLocale", "Locale", "text"),
            ("DataEvento", "Data", "text"),
            ("OraEvento", "Ora", "text"),
            ("TipoTassazione", "Tass.", "text"),
            ("Incidenza", "Incidenza", "int"),
            ("TipoGenere", "Genere", "text"),
            ("IVA_rate", "IVA", "pct"),
            ("ISI_rate", "ISI", "pct"),
            ("Imponibile_LOG_net", "Imp.LOG net", "money"),
            ("BaseOmaggiEcc_ISI", "Imp. omaggi ecc", "money"),
            ("Imponibile_atteso_parziale", "Imp.atteso", "money"),
            ("Imponibile_RPM", "Imp.RPM", "money"),
            ("Delta", "Delta", "money"),
            ("Note", "Note", "text"),
        ]
        ord_cols = [
            ("CodiceLocale", "Locale", "text"),
            ("DataEvento", "Data", "text"),
            ("OraEvento", "Ora", "text"),
            ("CodiceOrdine", "Ordine", "text"),
            ("Capienza", "Cap.", "int"),
            ("Omaggi_net", "Omaggi net", "int"),
            ("Limite_omaggi", "Limite", "int"),
            ("Eccedenza_omaggi", "Ecc.", "int"),
            ("Titolo_rif", "Titolo rif", "text"),
            ("Corrispettivo_rif_unit", "Corr. rif (unit)", "money"),
            ("Imponibile_rif_unit", "Imp. rif (unit)", "money"),
            ("IVACorrispettivo_rif_unit", "IVA corr (unit)", "money"),
            ("IVAEccedenteOmaggi_attesa", "IVA ecc attesa", "money"),
            ("IVAEccedenteOmaggi_rpm", "IVA ecc RPM", "money"),
            ("Note", "Note", "text"),
        ]
        ev_table = _render_rows_table(ev_rows, ev_cols)
        ord_table = _render_rows_table(ord_rows, ord_cols)

        fiscal_section = f"""
        <div class="section">
          <h2>Dettaglio controlli fiscali</h2>
          <details>
            <summary>Mostra/Nascondi</summary>
            <h3>ImponibileIntrattenimenti (RPM) per evento</h3>
            {ev_table}
            <h3>Omaggi eccedenti e IVAEccedenteOmaggi (RPM) per ordine</h3>
            {ord_table}
          </details>
        </div>
        """


    html_doc = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Report consistenza biglietteria</title>
<style>
    body {{
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
        margin: 0;
        padding: 0;
        background: #f6f7fb;
        color: #111827;
    }}
    header {{
        background: #111827;
        color: white;
        padding: 18px 22px;
    }}
    header h1 {{
        margin: 0;
        font-size: 18px;
        letter-spacing: .2px;
    }}
    header .sub {{
        margin-top: 6px;
        opacity: .85;
        font-size: 13px;
    }}
    .wrap {{
        padding: 18px 22px 40px 22px;
    }}
    .cards {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        margin-bottom: 16px;
    }}
    .card {{
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px 14px;
        box-shadow: 0 1px 0 rgba(0,0,0,.02);
    }}
    .card .k {{
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 6px;
    }}
    .card .v {{
        font-size: 20px;
        font-weight: 700;
    }}
    .section {{
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px;
        margin-top: 12px;
    }}
    .section h2 {{
        margin: 0 0 10px 0;
        font-size: 16px;
    }}
    details {{
        margin-top: 10px;
    }}
    summary {{
        cursor: pointer;
        font-weight: 650;
    }}
    .tbl {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 13px;
    }}
    .tbl th, .tbl td {{
        border: 1px solid #e5e7eb;
        padding: 8px 8px;
        vertical-align: top;
    }}
    .tbl th {{
        background: #f3f4f6;
        text-align: left;
        font-weight: 650;
    }}
    .tbl td.num {{
        text-align: right;
        font-variant-numeric: tabular-nums;
    }}
    .tbl td.n {{
        width: 44px;
        text-align: right;
        color: #6b7280;
        font-variant-numeric: tabular-nums;
    }}
    .tbl td.ctx {{
        font-size: 12px;
        color: #111827;
        line-height: 1.25rem;
        word-break: break-word;
    }}
    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid transparent;
    }}
    .badge-red {{
        background: #fee2e2;
        color: #991b1b;
        border-color: #fecaca;
    }}
    .badge-yellow {{
        background: #fef3c7;
        color: #92400e;
        border-color: #fde68a;
    }}
    .badge-green {{
        background: #d1fae5;
        color: #065f46;
        border-color: #a7f3d0;
    }}
    .badge-blue {{
        background: #dbeafe;
        color: #1e40af;
        border-color: #bfdbfe;
    }}
    .badge-gray {{
        background: #f3f4f6;
        color: #374151;
        border-color: #e5e7eb;
    }}
    .kv {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }}
    .kv th, .kv td {{
        border: 1px solid #e5e7eb;
        padding: 6px 8px;
        vertical-align: top;
    }}
    .kv th {{
        background: #f9fafb;
        width: 260px;
        color: #374151;
        font-weight: 650;
        text-align: left;
    }}
    footer {{
        margin-top: 18px;
        color: #6b7280;
        font-size: 12px;
    }}
</style>
</head>
<body>
<header>
  <h1>Report consistenza biglietteria — {_badge(status)}</h1>
  <div class="sub">Generato: {_now_iso()}</div>
</header>
<div class="wrap">

  <div class="cards">
    <div class="card"><div class="k">Esito</div><div class="v">{html.escape(status)}</div></div>
    <div class="card"><div class="k">Errori</div><div class="v">{errors}</div></div>
    <div class="card"><div class="k">Warning</div><div class="v">{warnings}</div></div>
    <div class="card"><div class="k">Issue totali</div><div class="v">{summary.get("total_issues", 0)}</div></div>
  </div>

  <div class="section">
    <h2>Riepilogo file e volumi</h2>
    {_render_kv_table(metrics)}
  </div>

  <div class="section">
    <h2>Esito controlli (per categoria)</h2>
    {checks_table}
  </div>

{fiscal_section}

  <div class="section">
    <h2>Dettaglio anomalie</h2>
    <details open>
      <summary>Elenco issue ({len(issues)})</summary>
      {_render_issues_table(issues)}
    </details>
  </div>

  <footer>
    Nota: gli importi sono trattati come interi in centesimi (come nei file d'esempio). Se nel tuo sistema usi una scala diversa, adatta il formatter.
  </footer>
</div>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_doc)


# ---------------------------
# CLI / Main
# ---------------------------

def discover_files(directory: str) -> Dict[str, List[str]]:
    """Ritorna dict { 'LOG': [...], 'LTA': [...], 'RCA': [...], 'RPM': [...] } usando sia nome file che root tag."""
    res = {"LOG": [], "LTA": [], "RCA": [], "RPM": []}
    if not os.path.isdir(directory):
        return res

    candidates = []
    for name in os.listdir(directory):
        if not name.lower().endswith((".xml", ".xsi")):
            continue
        candidates.append(os.path.join(directory, name))

    # prima prova col nome (veloce)
    for p in candidates:
        base = os.path.basename(p).upper()
        if base.startswith("LOG_"):
            res["LOG"].append(p)
        elif base.startswith("LTA_"):
            res["LTA"].append(p)
        elif base.startswith("RCA_"):
            res["RCA"].append(p)
        elif base.startswith("RPM_"):
            res["RPM"].append(p)

    # fallback: se alcune categorie sono vuote, prova a leggere root tag
    for p in candidates:
        try:
            root = _read_xml(p)
        except Exception:
            continue
        tag = root.tag
        if tag == "LogTransazione" and p not in res["LOG"]:
            res["LOG"].append(p)
        elif tag == "LTA_Giornaliera" and p not in res["LTA"]:
            res["LTA"].append(p)
        elif tag == "RiepilogoControlloAccessi" and p not in res["RCA"]:
            res["RCA"].append(p)
        elif tag == "RiepilogoMensile" and p not in res["RPM"]:
            res["RPM"].append(p)

    # ordino per nome (stabile)
    for k in res:
        res[k] = sorted(res[k])
    return res


def choose_latest_rpm(rpm_paths: List[str]) -> List[str]:
    """Se ci sono più RPM, seleziona quello 'più recente' per DataGenerazione/OraGenerazione/ProgressivoGenerazione."""
    if len(rpm_paths) <= 1:
        return rpm_paths
    scored = []
    for p in rpm_paths:
        try:
            root = _read_xml(p)
            if root.tag != "RiepilogoMensile":
                continue
            # DataGenerazione yyyymmdd, OraGenerazione hhmmss, ProgressivoGenerazione int
            dg = root.attrib.get("DataGenerazione", "") or ""
            og = root.attrib.get("OraGenerazione", "") or ""
            pg = root.attrib.get("ProgressivoGenerazione", "") or ""
            score = (dg, og, int(pg) if str(pg).isdigit() else -1, _file_mtime(p))
            scored.append((score, p))
        except Exception:
            scored.append((( "", "", -1, _file_mtime(p)), p))
    scored.sort(reverse=True)
    # tengo il migliore
    return [scored[0][1]]


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Verifica consistenza LOG/LTA/RCA/RPM e genera report HTML.")
    ap.add_argument("--dir", default=".", help="Cartella contenente i file (default: .)")
    ap.add_argument("--log", nargs="*", help="Percorso/i file LOG_*.xsi (override)")
    ap.add_argument("--lta", nargs="*", help="Percorso/i file LTA_*.xsi (override)")
    ap.add_argument("--rca", nargs="*", help="Percorso/i file RCA_*.xsi (override)")
    ap.add_argument("--rpm", nargs="*", help="Percorso/i file RPM_*.xsi (override)")
    ap.add_argument("--out", default="report_verifica.html", help="Percorso report HTML in output")
    ap.add_argument("--keep-all-rpm", action="store_true", help="Se presente, non seleziona l'RPM più recente ma usa tutti quelli trovati.")

    ap.add_argument("--tolleranza-importi", type=int, default=0,
                    help="Tolleranza (in cent) nei confronti importi tra fonti (default: 0).")
    ap.add_argument("--aliquote-tab1", default=None,
                    help="Percorso CSV TAB.1 aliquote (default: cerca 'aliquote_tab1.csv' nella cartella --dir).")
    ap.add_argument("--omaggi-pct-capienza", type=float, default=5.0,
                    help="Percentuale capienza entro cui gli omaggi NON sono eccedenti (default: 5.0).")
    ap.add_argument("--omaggi-soglia-iva-eur", type=float, default=25.82,
                    help="Soglia valore unitario (EUR) sotto la quale l'IVA su omaggi intrattenimenti non è dovuta (default: 25.82).")


    args = ap.parse_args(argv)

    discovered = discover_files(args.dir)
    log_paths = args.log or discovered["LOG"]
    lta_paths = args.lta or discovered["LTA"]
    rca_paths = args.rca or discovered["RCA"]
    rpm_paths = args.rpm or discovered["RPM"]

    if not args.keep_all_rpm:
        rpm_paths = choose_latest_rpm(rpm_paths)

    # parse
    log_recs = parse_log(log_paths)
    lta_recs = parse_lta(lta_paths)
    rca_recs = parse_rca(rca_paths)
    rpm_recs = parse_rpm(rpm_paths)

    # run checks
    # TAB.1 aliquote (se disponibile)
    aliquote_path = args.aliquote_tab1
    if not aliquote_path:
        # prova a cercare automaticamente
        candidates = [
            os.path.join(args.dir, "aliquote_tab1.csv"),
            os.path.join(os.path.dirname(__file__), "aliquote_tab1.csv"),
            "aliquote_tab1.csv",
        ]
        for c in candidates:
            if os.path.exists(c):
                aliquote_path = c
                break

    aliquote_tab1 = load_aliquote_tab1(aliquote_path) if aliquote_path else {}

    # run checks
    soglia_cent = int(round(float(args.omaggi_soglia_iva_eur) * 100))
    summary, issues, metrics, check_results, fiscal_details = run_checks(
        log_recs, lta_recs, rca_recs, rpm_recs,
        tolleranza_importi=int(args.tolleranza_importi),
        aliquote_tab1=aliquote_tab1,
        omaggi_pct_capienza=float(args.omaggi_pct_capienza),
        omaggi_soglia_iva_cent=soglia_cent,
    )

    metrics["TAB1_aliquote_path"] = aliquote_path or ""
    metrics["TAB1_aliquote_rows"] = len(aliquote_tab1)

    # add a few file lists in a nicer format
    metrics["LOG_files"] = ", ".join(metrics.get("log_files", []))
    metrics["LTA_files"] = ", ".join(metrics.get("lta_files", []))
    metrics["RCA_files"] = ", ".join(metrics.get("rca_files", []))
    metrics["RPM_files"] = ", ".join(metrics.get("rpm_files", []))

    # remove raw lists to avoid clutter
    for k in ["log_files", "lta_files", "rca_files", "rpm_files"]:
        metrics.pop(k, None)

    build_html_report(args.out, summary, metrics, issues, check_results=check_results, fiscal_details=fiscal_details)

    # exit code: 0 ok, 2 errors
    if summary.get("errors", 0) > 0:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:
        traceback.print_exc()
        raise SystemExit(2)

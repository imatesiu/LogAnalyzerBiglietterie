#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifica_consistenza_biglietteria.py

Verifica di consistenza (tecnica + fiscale) tra file SIAE/biglietteria:
- LOG_*.xsi  : Log transazioni (emissioni/annullamenti)
- LTA_*.xsi  : Lista titoli accesso (stato titoli)
- RCA_*.xsi  : Riepilogo controllo accessi
- RPM_*.xsi  : Riepilogo mensile
- aliquote_tab1.csv (opzionale ma consigliato): mappa TipoGenere -> aliquote IVA/ISI (Tabella 1)

Controlli principali:
1) Coerenza chiavi e riferimenti (duplicati, annullamenti che puntano a un originale, ecc.)
2) Coerenza quantitativi tra LOG <-> LTA <-> RCA <-> RPM
3) Controlli fiscali:
   - Ricostruzione IVA/ISI e ImponibileIntrattenimenti in LOG (in base a Incidenza e aliquote)
   - Ricostruzione eccedenza omaggi e confronto con RPM:
       * IVAEccedenteOmaggi (per OrdineDiPosto)
       * Intrattenimento/ImponibileIntrattenimenti (per Evento) includendo l'imponibile figurativo dell’eccedenza

NOTE SUL CALCOLO "ECCEDENZA OMAGGI" (come da regola operativa descritta dall’utente):
- Si conta l’eccedenza omaggi rispetto al 5% della capienza (per OrdineDiPosto).
- Il titolo di riferimento è quello con prezzo più alto:
    * biglietto: prezzo = CorrispettivoLordo (ESCLUDE la prevendita)
    * rateo abbonamento: (se presente) prezzo = ImportoFigurativo / Quantita (RPM BigliettiAbbonamento)
- Si considera solo la quota "Intrattenimento" del titolo: Prezzo * Incidenza%
- Scorporo IVA+ISI sulla quota intrattenimento e calcolo dell’IVA (per unità, poi moltiplicata per i titoli eccedenti).
- Soglia valore unitario LORDO (default 50,00 €) applicata sulla QUOTA INTRATTENIMENTO del titolo di riferimento:
    se quota_intr_unitaria_lorda <= soglia => IVAEccedenteOmaggi = 0
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_FLOOR
from typing import Any, Dict, Iterable, List, Optional, Tuple

import xml.etree.ElementTree as ET


# -------------------------
# Helpers: parsing & money
# -------------------------

def to_int(x: Any, default: int = 0) -> int:
    try:
        if x is None:
            return default
        s = str(x).strip()
        if s == "":
            return default
        return int(s)
    except Exception:
        return default


def round_half_up_int(d: Decimal) -> int:
    """Round half-up to integer (centesimi)."""
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def round_half_up_ratio(num: int, den: int) -> int:
    """Round half-up of num/den to integer."""
    if den == 0:
        return 0
    return round_half_up_int(Decimal(num) / Decimal(den))


def floor_int(d: Decimal) -> int:
    return int(d.to_integral_value(rounding=ROUND_FLOOR))


def cents_to_eur_str(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    euros = cents // 100
    c = cents % 100
    # formato italiano: separatore decimale ","
    return f"{sign}{euros:,}".replace(",", ".") + f",{c:02d} €"


def fmt_money(cents: Optional[int]) -> str:
    if cents is None:
        return "n/d"
    return f"{cents_to_eur_str(cents)} ({cents})"


# -------------------------
# Data structures
# -------------------------

@dataclass(frozen=True)
class TicketKey:
    sistema: str
    carta: str
    progressivo: str
    sigillo: str

    def short(self) -> str:
        return f"{self.sistema}/{self.carta}/{self.progressivo}/{self.sigillo}"


@dataclass
class Issue:
    severity: str  # "ERROR" | "WARN" | "INFO"
    check: str
    message: str
    context: Dict[str, Any]


# -------------------------
# Aliquote (Tabella 1)
# -------------------------

def _parse_percent_candidates(raw: str) -> List[float]:
    raw = (raw or "").strip()
    if not raw:
        return []
    # es: "10|22" oppure "22"
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    out: List[float] = []
    for p in parts:
        try:
            out.append(float(p) / 100.0)
        except Exception:
            pass
    return out


def _extract_percent_from_text(raw: str) -> Optional[float]:
    if not raw:
        return None
    import re
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", raw)
    if not m:
        return None
    try:
        return float(m.group(1)) / 100.0
    except Exception:
        return None


def parse_aliquote_tab1_csv(path: str) -> Dict[int, Dict[str, Any]]:
    """
    Ritorna dict:
      code -> { "descrizione": str, "iva_candidates": [..], "isi": float }
    """
    out: Dict[int, Dict[str, Any]] = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            code = row.get("Codice")
            if code is None or str(code).strip() == "":
                continue
            try:
                codice = int(str(code).strip())
            except Exception:
                continue

            descr = (row.get("Descrizione") or "").strip()

            iva_candidates = _parse_percent_candidates(str(row.get("IVA_rates_%") or "").strip())
            if not iva_candidates:
                iva_raw = (row.get("IVA_raw") or "").strip()
                if "esente" in iva_raw.lower():
                    iva_candidates = [0.0]
                else:
                    p = _extract_percent_from_text(iva_raw)
                    if p is not None:
                        iva_candidates = [p]

            # default: se ancora vuoto, assumo 0 (esente / non applicabile)
            if not iva_candidates:
                iva_candidates = [0.0]

            isi_rate = 0.0
            isi_raw = row.get("ISI_raw")
            if isinstance(isi_raw, str):
                p = _extract_percent_from_text(isi_raw)
                if p is not None:
                    isi_rate = p
            else:
                isi_rates = row.get("ISI_rates_%")
                if isi_rates is not None and str(isi_rates).strip() != "":
                    try:
                        isi_rate = float(str(isi_rates).strip()) / 100.0
                    except Exception:
                        isi_rate = 0.0

            out[codice] = {
                "descrizione": descr,
                "iva_candidates": iva_candidates,
                "isi": float(isi_rate),
            }
    return out


# -------------------------
# Fiscal math (calcolo-ISI)
# -------------------------

def calc_intr_sp_from_gross(
    gross_total_cents: int,
    incidenza_pct: int,
    iva_rate: float,
    isi_rate: float,
) -> Dict[str, int]:
    """
    Implementazione coerente con i valori osservati nei LOG di esempio:
    - Quota intrattenimento = round_half_up(gross * incidenza/100)
      Quota spettacolo = residuo (per mantenere somma esatta)
    - Intrattenimento: IVA e ISI calcolate con rounding half-up sul valore in centesimi,
      imponibile = quota_intr - iva_intr - isi
    - Spettacolo: imponibile = floor(quota_sp/(1+iva)), IVA = residuo (quota_sp - imponibile)
    """
    gross_total_cents = int(gross_total_cents)
    incidenza_pct = int(incidenza_pct)

    quota_intr = round_half_up_int(Decimal(gross_total_cents) * Decimal(incidenza_pct) / Decimal(100))
    quota_sp = gross_total_cents - quota_intr

    denom_intr = Decimal(1) + Decimal(str(iva_rate)) + Decimal(str(isi_rate))
    iva_intr = 0
    isi = 0
    imponibile_intr = 0
    if quota_intr != 0:
        iva_intr = round_half_up_int(Decimal(quota_intr) * Decimal(str(iva_rate)) / denom_intr)
        isi = round_half_up_int(Decimal(quota_intr) * Decimal(str(isi_rate)) / denom_intr)
        imponibile_intr = quota_intr - iva_intr - isi

    iva_sp = 0
    imponibile_sp = 0
    if quota_sp != 0:
        den_sp = Decimal(1) + Decimal(str(iva_rate))
        imponibile_sp = floor_int(Decimal(quota_sp) / den_sp)
        iva_sp = quota_sp - imponibile_sp

    return {
        "gross": gross_total_cents,
        "quota_intr": int(quota_intr),
        "quota_sp": int(quota_sp),
        "iva_intr": int(iva_intr),
        "isi": int(isi),
        "imponibile_intr": int(imponibile_intr),
        "imponibile_sp": int(imponibile_sp),
        "iva_sp": int(iva_sp),
        "iva_tot": int(iva_intr + iva_sp),
    }


def split_iva_tot_corr_prev(
    iva_tot_cents: int,
    corr_cents: int,
    prev_cents: int,
) -> Tuple[int, int]:
    """
    Ripartizione proporzionale dell'IVA totale tra Corrispettivo e Prevendita.
    - IVA_corr = round_half_up(IVA_tot * Corr / (Corr+Prev))
    - IVA_prev = residuo
    """
    gross = corr_cents + prev_cents
    if gross <= 0:
        return (0, 0)
    iva_corr = round_half_up_int(Decimal(iva_tot_cents) * Decimal(corr_cents) / Decimal(gross))
    iva_prev = iva_tot_cents - iva_corr
    return int(iva_corr), int(iva_prev)


# -------------------------
# XML parsing
# -------------------------

def _find_text(el: Optional[ET.Element], path: str) -> str:
    if el is None:
        return ""
    found = el.find(path)
    return found.text.strip() if found is not None and found.text else ""


def parse_log(path: str) -> List[Dict[str, Any]]:
    tree = ET.parse(path)
    root = tree.getroot()
    out: List[Dict[str, Any]] = []

    for tr in root.findall(".//Transazione"):
        ta = tr.find("TitoloAccesso")
        if ta is None:
            continue

        # Nei LOG osservati (esempio): i campi chiave sono attributi della Transazione.
        # Manteniamo fallback su eventuali elementi/attributi nel TitoloAccesso per robustezza.
        sistema = (tr.get("SistemaEmissione") or _find_text(ta, "SistemaEmissione") or "").strip()
        carta = (tr.get("CartaAttivazione") or _find_text(ta, "CartaAttivazione") or "").strip()
        prog = (
            tr.get("NumeroProgressivo")
            or tr.get("ProgressivoFiscale")
            or _find_text(ta, "NumeroProgressivo")
            or _find_text(ta, "ProgressivoFiscale")
            or ""
        ).strip()
        sig = (tr.get("SigilloFiscale") or _find_text(ta, "SigilloFiscale") or "").strip()
        key = TicketKey(sistema=sistema, carta=carta, progressivo=prog, sigillo=sig)

        rec = {
            "_file": os.path.basename(path),
            "key": key,

            "CFOrganizzatore": (tr.get("CFOrganizzatore") or "").strip(),
            "CFTitolare": (tr.get("CFTitolare") or "").strip(),
            "DataEmissione": (tr.get("DataEmissione") or "").strip(),
            "OraEmissione": (tr.get("OraEmissione") or "").strip(),
            "TipoTitolo": (tr.get("TipoTitolo") or "").strip(),
            "CodiceOrdine": (tr.get("CodiceOrdine") or "").strip(),
            "Posto": (tr.get("Posto") or "").strip(),
            "ImponibileIntrattenimenti": to_int(tr.get("ImponibileIntrattenimenti"), 0),

            # Attributi fiscali possono stare su Transazione (frequente) o su TitoloAccesso
            "TipoTassazione": (tr.get("TipoTassazione") or ta.get("TipoTassazione") or "").strip(),
            "IVAPreassolta": (tr.get("IVAPreassolta") or ta.get("IVAPreassolta") or "").strip(),

            # TitoloAccesso
            "Annullamento": (ta.get("Annullamento") or "").strip(),
            "OriginaleAnnullato": (tr.get("OriginaleAnnullato") or ta.get("OriginaleAnnullato") or "").strip(),
            "CartaOriginaleAnnullato": (tr.get("CartaOriginaleAnnullato") or ta.get("CartaOriginaleAnnullato") or "").strip(),
            "CausaleAnnullamento": (tr.get("CausaleAnnullamento") or ta.get("CausaleAnnullamento") or "").strip(),

            "CodiceLocale": _find_text(ta, "CodiceLocale"),
            "DataEvento": _find_text(ta, "DataEvento"),
            "OraEvento": _find_text(ta, "OraEvento"),
            "TipoGenere": to_int(_find_text(ta, "TipoGenere"), 0),
            "TitoloEvento": _find_text(ta, "Titolo"),

            "CorrispettivoLordo": to_int(_find_text(ta, "CorrispettivoLordo"), 0),
            "Prevendita": to_int(_find_text(ta, "Prevendita"), 0),
            "IVACorrispettivo": to_int(_find_text(ta, "IVACorrispettivo"), 0),
            "IVAPrevendita": to_int(_find_text(ta, "IVAPrevendita"), 0),
        }
        out.append(rec)

    return out



def parse_lta(path: str) -> List[Dict[str, Any]]:
    """
    Parsing LTA.

    Nota importante sugli annullamenti:
    - In LTA, quando un titolo viene annullato, *rimane* il record del titolo originale
      (chiave: SistemaEmissione/CartaAttivazione/ProgressivoFiscale/SigilloFiscale) ma con:
         Annullamento="S"
         DataANN/OraANN + CartaAttivazioneANN/ProgressivoFiscaleANN/SigilloFiscaleANN
      che identificano il "titolo di annullamento" (presente nel LOG come Transazione con Annullamento="S").
    """
    tree = ET.parse(path)
    root = tree.getroot()
    out: List[Dict[str, Any]] = []

    for ev in root.findall(".//LTA_Evento"):
        cf_org = (ev.get("CFOrganizzatore") or "").strip()
        cod_loc = (ev.get("CodiceLocale") or "").strip()
        data_ev = (ev.get("DataEvento") or "").strip()
        ora_ev = (ev.get("OraEvento") or "").strip()
        tipo_gen = (ev.get("TipoGenere") or "").strip()
        titolo_ev = (ev.get("Titolo") or ev.get("TitoloEvento") or "").strip()

        for ta in ev.findall("./TitoloAccesso"):
            sistema = (ta.get("SistemaEmissione") or "").strip()
            carta = (ta.get("CartaAttivazione") or "").strip()
            prog = (ta.get("ProgressivoFiscale") or "").strip()
            sig = (ta.get("SigilloFiscale") or "").strip()
            key = TicketKey(sistema=sistema, carta=carta, progressivo=prog, sigillo=sig)

            # Stato: negli esempi reali è "Stato" (VT/VD/AT/...), ma teniamo fallback su "StatoTitolo"
            stato = (ta.get("Stato") or ta.get("StatoTitolo") or "").strip()

            out.append({
                "_file": os.path.basename(path),
                "key": key,

                "CFOrganizzatore": cf_org,
                "CodiceLocale": cod_loc,
                "DataEvento": data_ev,
                "OraEvento": ora_ev,
                "TipoGenere": tipo_gen,
                "TitoloEvento": titolo_ev,

                "StatoTitolo": stato,
                "Annullamento": (ta.get("Annullamento") or "").strip(),

                "TipoTitolo": (ta.get("TipoTitolo") or "").strip(),
                "CodiceOrdine": (ta.get("CodiceOrdine") or "").strip(),

                "CorrispettivoLordo_LTA": to_int(ta.get("CorrispettivoLordo"), 0),
                "Abbonamento": (ta.get("Abbonamento") or "").strip(),
                "CodSupporto": (ta.get("CodSupporto") or "").strip(),
                "IdSupporto": (ta.get("IdSupporto") or "").strip(),
                "DataEmissione": (ta.get("DataEmissione") or "").strip(),
                "OraEmissione": (ta.get("OraEmissione") or "").strip(),
                "DataLTA": (ta.get("DataLTA") or "").strip(),
                "OraLTA": (ta.get("OraLTA") or "").strip(),

                # Campi di annullamento (presenti sul titolo originale quando Annullamento="S")
                "DataANN": (ta.get("DataANN") or "").strip(),
                "OraANN": (ta.get("OraANN") or "").strip(),
                "CartaAttivazioneANN": (ta.get("CartaAttivazioneANN") or "").strip(),
                "ProgressivoFiscaleANN": (ta.get("ProgressivoFiscaleANN") or "").strip(),
                "SigilloFiscaleANN": (ta.get("SigilloFiscaleANN") or "").strip(),
            })

    return out



def parse_rca(path: str) -> List[Dict[str, Any]]:
    """
    Parsing RCA (RiepilogoControlloAccessi).

    Nei file RCA reali, per ciascun Evento e per ciascun Ordine di posto, sono presenti i totali
    per TipoTitolo e per "stato/uso" (NoAccesso, Automatizzati, Manuali, Annullati, Daspati, Rubati, BL),
    distinti fra Tradizionale e Digitale.

    Struttura tipica:
      RiepilogoControlloAccessi/Evento/SistemaEmissione/Titoli/TotaleTipoTitolo/...
    """
    tree = ET.parse(path)
    root = tree.getroot()
    out: List[Dict[str, Any]] = []

    for ev in root.findall(".//Evento"):
        cf_org = (_find_text(ev, "CFOrganizzatore") or "").strip()
        cod_loc = (_find_text(ev, "CodiceLocale") or "").strip()
        data_ev = (_find_text(ev, "DataEvento") or "").strip()
        ora_ev = (_find_text(ev, "OraEvento") or "").strip()
        incidenza = to_int(_find_text(ev, "IncidenzaIntrattenimento"), 0)

        for se in ev.findall("./SistemaEmissione"):
            sistema_em = (_find_text(se, "CodiceSistemaEmissione") or "").strip()

            for titoli in se.findall("./Titoli"):
                ordine = (_find_text(titoli, "CodiceOrdinePosto") or "").strip()
                capienza = to_int(_find_text(titoli, "Capienza"), 0)

                for tt in titoli.findall("./TotaleTipoTitolo"):
                    tipo = (_find_text(tt, "TipoTitolo") or "").strip()
                    rec = {
                        "_file": os.path.basename(path),
                        "CFOrganizzatore": cf_org,
                        "CodiceLocale": cod_loc,
                        "DataEvento": data_ev,
                        "OraEvento": ora_ev,
                        "SistemaEmissione": sistema_em,
                        "IncidenzaIntrattenimento": incidenza,
                        "CodiceOrdine": ordine,
                        "Capienza": capienza,
                        "TipoTitolo": tipo,

                        "TotaleTitoliLTA": to_int(_find_text(tt, "TotaleTitoliLTA"), 0),

                        "TotaleTitoliNoAccessoTradiz": to_int(_find_text(tt, "TotaleTitoliNoAccessoTradiz"), 0),
                        "TotaleTitoliNoAccessoDigitali": to_int(_find_text(tt, "TotaleTitoliNoAccessoDigitali"), 0),

                        "TotaleTitoliAutomatizzatiTradiz": to_int(_find_text(tt, "TotaleTitoliAutomatizzatiTradiz"), 0),
                        "TotaleTitoliAutomatizzatiDigitali": to_int(_find_text(tt, "TotaleTitoliAutomatizzatiDigitali"), 0),

                        "TotaleTitoliManualiTradiz": to_int(_find_text(tt, "TotaleTitoliManualiTradiz"), 0),
                        "TotaleTitoliManualiDigitali": to_int(_find_text(tt, "TotaleTitoliManualiDigitali"), 0),

                        "TotaleTitoliAnnullatiTradiz": to_int(_find_text(tt, "TotaleTitoliAnnullatiTradiz"), 0),
                        "TotaleTitoliAnnullatiDigitali": to_int(_find_text(tt, "TotaleTitoliAnnullatiDigitali"), 0),

                        "TotaleTitoliDaspatiTradiz": to_int(_find_text(tt, "TotaleTitoliDaspatiTradiz"), 0),
                        "TotaleTitoliDaspatiDigitali": to_int(_find_text(tt, "TotaleTitoliDaspatiDigitali"), 0),

                        "TotaleTitoliRubatiTradiz": to_int(_find_text(tt, "TotaleTitoliRubatiTradiz"), 0),
                        "TotaleTitoliRubatiDigitali": to_int(_find_text(tt, "TotaleTitoliRubatiDigitali"), 0),

                        "TotaleTitoliBLTradiz": to_int(_find_text(tt, "TotaleTitoliBLTradiz"), 0),
                        "TotaleTitoliBLDigitali": to_int(_find_text(tt, "TotaleTitoliBLDigitali"), 0),
                    }
                    out.append(rec)

    return out


def parse_rpm(path: str) -> List[Dict[str, Any]]:
    tree = ET.parse(path)
    root = tree.getroot()
    out: List[Dict[str, Any]] = []

    for org in root.findall(".//Organizzatore"):
        cf_org = _find_text(org, "CodiceFiscale")
        for ev in org.findall("./Evento"):
            loc = _find_text(ev, "Locale/CodiceLocale")
            denom_loc = _find_text(ev, "Locale/Denominazione")
            data = _find_text(ev, "DataEvento")
            ora = _find_text(ev, "OraEvento")

            inc = to_int(_find_text(ev, "Intrattenimento/Incidenza"), 0)
            imp_intr = _find_text(ev, "Intrattenimento/ImponibileIntrattenimenti")
            imp_intr_val = to_int(imp_intr, 0) if imp_intr != "" else None
            tipo_tass_el = ev.find("Intrattenimento/TipoTassazione")
            tipo_tass = tipo_tass_el.get("valore") if tipo_tass_el is not None else ""

            # record evento (unico)
            out.append({
                "kind": "Evento",
                "Organizzatore_CF": cf_org,
                "CodiceLocale": loc,
                "DenominazioneLocale": denom_loc,
                "DataEvento": data,
                "OraEvento": ora,
                "Incidenza": inc if inc != 0 or tipo_tass else None,
                "TipoTassazione": tipo_tass or None,
                "ImponibileIntrattenimenti": imp_intr_val,
            })

            for od in ev.findall("./OrdineDiPosto"):
                ordine = _find_text(od, "CodiceOrdine")
                capienza = to_int(_find_text(od, "Capienza"), 0)
                iva_ecc = _find_text(od, "IVAEccedenteOmaggi")
                iva_ecc_val = to_int(iva_ecc, 0) if iva_ecc != "" else 0

                # record ordine di posto
                out.append({
                    "kind": "OrdineDiPosto",
                    "Organizzatore_CF": cf_org,
                    "CodiceLocale": loc,
                "DenominazioneLocale": denom_loc,
                    "DataEvento": data,
                    "OraEvento": ora,
                    "CodiceOrdine": ordine,
                    "Capienza": capienza if capienza != 0 else None,
                    "IVAEccedenteOmaggi": iva_ecc_val,
                })

                def emit_titoli(kind: str) -> None:
                    for node in od.findall(f"./{kind}"):
                        out.append({
                            "kind": kind,
                            "Organizzatore_CF": cf_org,
                            "CodiceLocale": loc,
                "DenominazioneLocale": denom_loc,
                            "DataEvento": data,
                            "OraEvento": ora,
                            "CodiceOrdine": ordine,
                            "Capienza": capienza if capienza != 0 else None,
                            "IVAEccedenteOmaggi": iva_ecc_val,

                            "TipoTitolo": _find_text(node, "TipoTitolo"),
                            "Quantita": to_int(_find_text(node, "Quantita"), 0),
                            "CorrispettivoLordo": to_int(_find_text(node, "CorrispettivoLordo"), 0),
                            "Prevendita": to_int(_find_text(node, "Prevendita"), 0),
                            "IVACorrispettivo": to_int(_find_text(node, "IVACorrispettivo"), 0),
                            "IVAPrevendita": to_int(_find_text(node, "IVAPrevendita"), 0),
                            "ImportoPrestazione": to_int(_find_text(node, "ImportoPrestazione"), 0),
                        })

                for k in ("TitoliAccesso", "TitoliAnnullati", "TitoliAccessoIVAPreassolta", "TitoliIVAPreassoltaAnnullati"):
                    emit_titoli(k)

                # BigliettiAbbonamento (ratei figurativi)
                for node in od.findall("./BigliettiAbbonamento"):
                    out.append({
                        "kind": "BigliettiAbbonamento",
                        "Organizzatore_CF": cf_org,
                        "CodiceLocale": loc,
                "DenominazioneLocale": denom_loc,
                        "DataEvento": data,
                        "OraEvento": ora,
                        "CodiceOrdine": ordine,
                        "Capienza": capienza if capienza != 0 else None,
                        "IVAEccedenteOmaggi": iva_ecc_val,

                        "TipoTitolo": _find_text(node, "TipoTitolo"),
                        "Quantita": to_int(_find_text(node, "Quantita"), 0),
                        "ImportoFigurativo": to_int(_find_text(node, "ImportoFigurativo"), 0),
                        "IVAFigurativa": to_int(_find_text(node, "IVAFigurativa"), 0),
                    })

    return out


# -------------------------
# File discovery
# -------------------------

def discover_files(directory: str) -> Dict[str, List[str]]:
    """
    Ritorna dict con chiavi: LOG, LTA, RCA, RPM, ALIQUOTE
    """
    out = {"LOG": [], "LTA": [], "RCA": [], "RPM": [], "ALIQ": []}
    for fn in os.listdir(directory):
        path = os.path.join(directory, fn)
        if not os.path.isfile(path):
            continue
        low = fn.lower()
        if low.endswith(".xsi") or low.endswith(".xml"):
            if low.startswith("log_"):
                out["LOG"].append(path)
            elif low.startswith("lta_"):
                out["LTA"].append(path)
            elif low.startswith("rca_"):
                out["RCA"].append(path)
            elif low.startswith("rpm_"):
                out["RPM"].append(path)
        elif low.endswith(".csv") and "aliquote" in low and "tab1" in low:
            out["ALIQ"].append(path)
    # ordina per stabilità
    for k in out:
        out[k] = sorted(out[k])
    return out


# -------------------------
# Checks (definitions)
# -------------------------

CHECK_DEFS: Dict[str, str] = {
    "LOG_duplicates": "LOG: verifica duplicati chiave titolo (emissioni)",
    "LOG_cancellations_ref": "LOG: annullamenti puntano a un titolo originale esistente",
    "LOG_vs_LTA": "LOG↔LTA: emissioni presenti in LTA; annullamenti verificati su LTA tramite campi *ANN* del titolo originale",
    "LTA_vs_RCA": "LTA↔RCA: confronto totali per TipoTitolo (NoAccesso/Automatizzati/Manuali/Annullati/Daspati/Rubati/BL) Tradiz/Digitali",
    "RCA_internal": "RCA: TotaleTitoliLTA coerente con la somma delle categorie per TipoTitolo",
    "LOG_vs_RPM": "LOG↔RPM: coerenza aggregati titoli (accesso/annullati) per evento/ordine/tipo",
    "LTA_vs_RPM": "LTA↔RPM: coerenza quantità titoli (accesso/annullati)",
    "FIS_LOG_IVA_ISI": "Fiscale (LOG): ricostruzione IVA/ISI & ImponibileIntrattenimenti (calcolo-ISI)",
    "FIS_RPM_OMAGGI": "Fiscale (RPM): eccedenza omaggi (IVAEccedenteOmaggi) su prezzo massimo (corrispettivo, no prevendita)",
    "FIS_RPM_IMP_INTR": "Fiscale (RPM): ImponibileIntrattenimenti evento = LOG netto + imponibile figurativo eccedenza omaggi",
}


# -------------------------
# Core checks runner
# -------------------------

def run_checks(
    log_recs: List[Dict[str, Any]],
    lta_recs: List[Dict[str, Any]],
    rca_recs: List[Dict[str, Any]],
    rpm_recs: List[Dict[str, Any]],
    aliquote: Optional[Dict[int, Dict[str, Any]]],
    omaggi_pct: float,
    soglia_omaggi_eur: float,
) -> Tuple[Dict[str, Any], List[Issue], Dict[str, Any], Dict[str, Any]]:

    issues: List[Issue] = []

    # metrics
    metrics: Dict[str, Any] = {
        "LOG_records": len(log_recs),
        "LTA_records": len(lta_recs),
        "RCA_records": len(rca_recs),
        "RPM_records": len(rpm_recs),
    }

    details: Dict[str, Any] = {
        "fiscale_omaggi": [],  # filled later
        "fiscale_evento_titoli": [],  # riepilogo fiscale per evento/tipologia (netto annulli)
    }

    # -------------------------
    # Indexes
    # -------------------------
    log_emis = [r for r in log_recs if r.get("Annullamento") == "N"]
    log_ann = [r for r in log_recs if r.get("Annullamento") == "S"]

    lta_by_key: Dict[TicketKey, Dict[str, Any]] = {r["key"]: r for r in lta_recs}

    # Index original lookup for annullamenti: (sistema, carta, progressivo) -> rec
    log_by_triplet: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for r in log_emis:
        k: TicketKey = r["key"]
        trip = (k.sistema, k.carta, k.progressivo)
        # se duplicati li segnaleremo sotto; qui manteniamo il primo
        log_by_triplet.setdefault(trip, r)

    # RPM indexes
    rpm_event_info: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}
    rpm_order_info: Dict[Tuple[str, str, str, str, str], Dict[str, Any]] = {}
    rpm_by_key: Dict[Tuple[str, str, str, str, str, str], Dict[str, Any]] = {}

    for rr in rpm_recs:
        kind = rr.get("kind")
        if kind == "Evento":
            key = (rr.get("Organizzatore_CF") or "", rr.get("CodiceLocale") or "", rr.get("DataEvento") or "", rr.get("OraEvento") or "")
            # keep first
            rpm_event_info.setdefault(key, rr)
        elif kind == "OrdineDiPosto":
            key = (rr.get("Organizzatore_CF") or "", rr.get("CodiceLocale") or "", rr.get("DataEvento") or "", rr.get("OraEvento") or "", rr.get("CodiceOrdine") or "")
            rpm_order_info[key] = rr
        elif kind in ("TitoliAccesso", "TitoliAnnullati", "TitoliAccessoIVAPreassolta", "TitoliIVAPreassoltaAnnullati"):
            key = (
                kind,
                rr.get("Organizzatore_CF") or "",
                rr.get("CodiceLocale") or "",
                rr.get("DataEvento") or "",
                rr.get("OraEvento") or "",
                rr.get("CodiceOrdine") or "",
                rr.get("TipoTitolo") or "",
            )
            rpm_by_key[key] = rr

    # -------------------------

    # Incidenza per evento (da RPM) - usata nei calcoli fiscali e nelle tabelle di riepilogo
    inc_map: Dict[Tuple[str, str, str, str], int] = {}
    for k, ev in rpm_event_info.items():
        inc = ev.get("Incidenza")
        if inc is not None:
            inc_map[k] = int(inc)

    # 1) LOG duplicates (emissioni)
    # -------------------------
    seen: Dict[TicketKey, int] = Counter()
    for r in log_emis:
        seen[r["key"]] += 1
    dup_keys = [k for k, c in seen.items() if c > 1]
    for k in dup_keys:
        issues.append(Issue(
            severity="ERROR",
            check="LOG_duplicates",
            message="Chiave titolo duplicata tra le emissioni LOG",
            context={"key": k.short(), "count": seen[k]},
        ))

    # -------------------------
    # 2) LOG cancellations reference original
    # -------------------------
    for r in log_ann:
        k: TicketKey = r["key"]
        orig_prog = r.get("OriginaleAnnullato") or ""
        orig_card = r.get("CartaOriginaleAnnullato") or ""
        trip = (k.sistema, orig_card, orig_prog)
        if not orig_prog or not orig_card:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_cancellations_ref",
                message="Annullamento senza riferimenti all'originale (OriginaleAnnullato/CartaOriginaleAnnullato mancanti)",
                context={"ann_key": k.short(), "file": r.get("_file")},
            ))
            continue
        if trip not in log_by_triplet:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_cancellations_ref",
                message="Annullamento che non trova il titolo originale nel LOG (per tripla sistema/carta/progressivo)",
                context={"ann_key": k.short(), "orig_triplet": f"{trip[0]}/{trip[1]}/{trip[2]}", "file": r.get("_file")},
            ))

    # -------------------------
    
    # -------------------------
    # 3) LOG ↔ LTA (presenza emissioni + gestione annullamenti via campi ANN in LTA)
    # -------------------------
    # In LTA, il titolo annullato è il titolo originale marcato Annullamento="S" e contiene:
    #   DataANN, OraANN, CartaAttivazioneANN, ProgressivoFiscaleANN, SigilloFiscaleANN
    # che identificano la transazione di annullamento presente nel LOG.

    # Indice LTA per tripla (SistemaEmissione, CartaAttivazione, ProgressivoFiscale) per trovare il titolo originale
    lta_by_triplet: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    lta_triplet_counts: Counter = Counter()
    for rr in lta_recs:
        kk: TicketKey = rr["key"]
        trip = (kk.sistema, kk.carta, kk.progressivo)
        lta_triplet_counts[trip] += 1
        lta_by_triplet.setdefault(trip, rr)

    for trip, c in lta_triplet_counts.items():
        if c > 1:
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="LTA: più titoli condividono la stessa tripla (SistemaEmissione/CartaAttivazione/ProgressivoFiscale) -> match annullamenti non univoco",
                context={"triplet": f"{trip[0]}/{trip[1]}/{trip[2]}", "count": c},
            ))

    # Indice LOG per chiave completa (utile per reverse-check annullamenti)
    log_by_key: Dict[TicketKey, Dict[str, Any]] = {}
    for rr in log_recs:
        log_by_key.setdefault(rr["key"], rr)

    # 3.a) Emissioni: la chiave completa del titolo deve essere presente in LTA
    for r in log_emis:
        k: TicketKey = r["key"]
        if k not in lta_by_key:
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="Emissione presente nel LOG ma assente in LTA",
                context={"key": k.short(), "file": r.get("_file")},
            ))

    # 3.b) Annullamenti: NON si cerca la chiave di annullamento in LTA come titolo autonomo.
    #      Si cerca invece il titolo originale in LTA e si verifica che i campi *ANN* combacino con il LOG.
    for r in log_ann:
        k_ann: TicketKey = r["key"]
        orig_prog = (r.get("OriginaleAnnullato") or "").strip()
        orig_card = (r.get("CartaOriginaleAnnullato") or "").strip()
        if not orig_prog or not orig_card:
            # già gestito in LOG_cancellations_ref
            continue

        orig_trip = (k_ann.sistema, orig_card, orig_prog)
        lta_orig = lta_by_triplet.get(orig_trip)
        if not lta_orig:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_LTA",
                message="Annullamento LOG: titolo originale non trovato in LTA (match su Sistema/CartaOriginale/ProgressivoOriginale)",
                context={"ann_key": k_ann.short(), "orig_triplet": f"{orig_trip[0]}/{orig_trip[1]}/{orig_trip[2]}"},
            ))
            continue

        if (lta_orig.get("Annullamento") or "").upper() != "S":
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_LTA",
                message="Annullamento LOG: il titolo originale in LTA non è marcato Annullamento='S'",
                context={"orig_key": lta_orig["key"].short(), "ann_key": k_ann.short()},
            ))

        # Verifica campi ANN sul titolo originale
        expected = {
            "DataANN": (r.get("DataEmissione") or "").strip(),
            "OraANN": (r.get("OraEmissione") or "").strip(),
            "CartaAttivazioneANN": k_ann.carta,
            "ProgressivoFiscaleANN": k_ann.progressivo,
            "SigilloFiscaleANN": k_ann.sigillo,
        }
        for fld, exp in expected.items():
            act = (lta_orig.get(fld) or "").strip()
            if act != exp:
                issues.append(Issue(
                    severity="ERROR",
                    check="LOG_vs_LTA",
                    message=f"Mismatch campo {fld} tra LOG annullamento e LTA (sul titolo originale)",
                    context={
                        "orig_key": lta_orig["key"].short(),
                        "ann_key": k_ann.short(),
                        "expected": exp,
                        "actual": act,
                    },
                ))

        # Se nel LOG esiste l'emissione originale, controlliamo anche il sigillo originale (coerenza forte)
        orig_log = log_by_triplet.get((k_ann.sistema, orig_card, orig_prog))
        if orig_log is not None:
            sig_log = orig_log["key"].sigillo
            sig_lta = lta_orig["key"].sigillo
            if sig_log and sig_lta and sig_log != sig_lta:
                issues.append(Issue(
                    severity="WARN",
                    check="LOG_vs_LTA",
                    message="SigilloFiscale del titolo originale differente tra LOG e LTA (possibile incongruenza di anagrafica titolo)",
                    context={"orig_triplet": f"{orig_trip[0]}/{orig_trip[1]}/{orig_trip[2]}", "sigillo_log": sig_log, "sigillo_lta": sig_lta},
                ))

    # 3.c) Reverse-check: ogni titolo LTA con Annullamento='S' deve avere un annullamento LOG corrispondente
    for rr in lta_recs:
        if (rr.get("Annullamento") or "").upper() != "S":
            continue
        kk: TicketKey = rr["key"]
        carta_ann = (rr.get("CartaAttivazioneANN") or "").strip()
        prog_ann = (rr.get("ProgressivoFiscaleANN") or "").strip()
        sig_ann = (rr.get("SigilloFiscaleANN") or "").strip()
        data_ann = (rr.get("DataANN") or "").strip()
        ora_ann = (rr.get("OraANN") or "").strip()

        if not (carta_ann and prog_ann and sig_ann):
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="LTA: titolo marcato Annullamento='S' ma campi ANN incompleti (Carta/Progressivo/Sigillo)",
                context={"orig_key": kk.short(), "cartaANN": carta_ann, "progANN": prog_ann, "sigANN": sig_ann},
            ))
            continue

        ann_key = TicketKey(sistema=kk.sistema, carta=carta_ann, progressivo=prog_ann, sigillo=sig_ann)
        log_ann_rec = log_by_key.get(ann_key)
        if log_ann_rec is None:
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="LTA: annullamento indicato nei campi ANN ma transazione di annullamento non trovata nel LOG",
                context={"orig_key": kk.short(), "ann_key": ann_key.short(), "dataANN": data_ann, "oraANN": ora_ann},
            ))
            continue

        if (log_ann_rec.get("Annullamento") or "").upper() != "S":
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_LTA",
                message="LTA: i campi ANN puntano a un titolo nel LOG che NON è un annullamento (Annullamento!='S')",
                context={"orig_key": kk.short(), "ann_key": ann_key.short(), "log_ann_flag": log_ann_rec.get("Annullamento")},
            ))

        # Coerenza riferimenti originale nel LOG annullamento
        if (log_ann_rec.get("CartaOriginaleAnnullato") or "").strip() != kk.carta or (log_ann_rec.get("OriginaleAnnullato") or "").strip() != kk.progressivo:
            issues.append(Issue(
                severity="ERROR",
                check="LOG_vs_LTA",
                message="LOG annullamento: riferimenti all'originale diversi da quelli del titolo originale in LTA",
                context={
                    "orig_key_lta": kk.short(),
                    "ann_key_log": ann_key.short(),
                    "log_CartaOriginaleAnnullato": (log_ann_rec.get("CartaOriginaleAnnullato") or "").strip(),
                    "log_OriginaleAnnullato": (log_ann_rec.get("OriginaleAnnullato") or "").strip(),
                },
            ))

        # Coerenza data/ora annullamento
        if data_ann and (log_ann_rec.get("DataEmissione") or "").strip() != data_ann:
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="DataANN in LTA diversa da DataEmissione della transazione di annullamento nel LOG",
                context={"orig_key": kk.short(), "ann_key": ann_key.short(), "lta_DataANN": data_ann, "log_DataEmissione": (log_ann_rec.get("DataEmissione") or "").strip()},
            ))
        if ora_ann and (log_ann_rec.get("OraEmissione") or "").strip() != ora_ann:
            issues.append(Issue(
                severity="WARN",
                check="LOG_vs_LTA",
                message="OraANN in LTA diversa da OraEmissione della transazione di annullamento nel LOG",
                context={"orig_key": kk.short(), "ann_key": ann_key.short(), "lta_OraANN": ora_ann, "log_OraEmissione": (log_ann_rec.get("OraEmissione") or "").strip()},
            ))


    # -------------------------
    # 4) LTA vs RCA (totali per TipoTitolo e categoria)
    # -------------------------
    # Mappatura StatoTitolo (2 lettere) -> categorie RCA.
    # Convenzione tipica osservata negli esempi:
    #   V? = NoAccesso, Z? = Automatizzati, M? = Manuali, A? = Annullati, D? = Daspati, R? = Rubati, B? = BlackList
    #   ?T = Tradizionale, ?D = Digitale
    rca_fields = [
        "TotaleTitoliLTA",
        "TotaleTitoliNoAccessoTradiz", "TotaleTitoliNoAccessoDigitali",
        "TotaleTitoliAutomatizzatiTradiz", "TotaleTitoliAutomatizzatiDigitali",
        "TotaleTitoliManualiTradiz", "TotaleTitoliManualiDigitali",
        "TotaleTitoliAnnullatiTradiz", "TotaleTitoliAnnullatiDigitali",
        "TotaleTitoliDaspatiTradiz", "TotaleTitoliDaspatiDigitali",
        "TotaleTitoliRubatiTradiz", "TotaleTitoliRubatiDigitali",
        "TotaleTitoliBLTradiz", "TotaleTitoliBLDigitali",
    ]

    def _empty_rca_bucket() -> Dict[str, int]:
        return {f: 0 for f in rca_fields}

    # Aggregazione LTA
    lta_rca: Dict[Tuple[str, str, str, str, str, str, str], Dict[str, int]] = defaultdict(_empty_rca_bucket)
    unknown_lta_states: Counter = Counter()

    for r in lta_recs:
        kkey: TicketKey = r["key"]
        key_rca = (
            kkey.sistema,
            (r.get("CFOrganizzatore") or "").strip(),
            (r.get("CodiceLocale") or "").strip(),
            (r.get("DataEvento") or "").strip(),
            (r.get("OraEvento") or "").strip(),
            (r.get("CodiceOrdine") or "").strip(),
            (r.get("TipoTitolo") or "").strip(),
        )
        b = lta_rca[key_rca]
        b["TotaleTitoliLTA"] += 1

        stato = (r.get("StatoTitolo") or "").strip().upper()
        if len(stato) < 2:
            if stato:
                unknown_lta_states[stato] += 1
            continue

        prefix = stato[0]
        suffix = stato[1]
        trad_dig = "Tradiz" if suffix == "T" else ("Digitali" if suffix == "D" else None)
        if trad_dig is None:
            unknown_lta_states[stato] += 1
            continue

        cat = None
        if prefix == "V":
            cat = "NoAccesso"
        elif prefix == "Z":
            cat = "Automatizzati"
        elif prefix == "M":
            cat = "Manuali"
        elif prefix == "A":
            cat = "Annullati"
        elif prefix == "D":
            cat = "Daspati"
        elif prefix == "R":
            cat = "Rubati"
        elif prefix == "B":
            cat = "BL"
        else:
            unknown_lta_states[stato] += 1
            continue

        fld = f"TotaleTitoli{cat}{trad_dig}"
        if fld in b:
            b[fld] += 1
        else:
            unknown_lta_states[stato] += 1

    if unknown_lta_states:
        issues.append(Issue(
            severity="INFO",
            check="LTA_vs_RCA",
            message="LTA contiene codici StatoTitolo non mappati sulle categorie RCA (controllo parziale su queste righe)",
            context={"unknown_states": dict(unknown_lta_states)},
        ))

    # Mappa RCA per chiave comparabile
    rca_map: Dict[Tuple[str, str, str, str, str, str, str], Dict[str, Any]] = {}
    dup_rca = 0
    for rr in rca_recs:
        key_rca = (
            (rr.get("SistemaEmissione") or "").strip(),
            (rr.get("CFOrganizzatore") or "").strip(),
            (rr.get("CodiceLocale") or "").strip(),
            (rr.get("DataEvento") or "").strip(),
            (rr.get("OraEvento") or "").strip(),
            (rr.get("CodiceOrdine") or "").strip(),
            (rr.get("TipoTitolo") or "").strip(),
        )
        if key_rca in rca_map:
            dup_rca += 1
        rca_map.setdefault(key_rca, rr)

    if dup_rca:
        issues.append(Issue(
            severity="WARN",
            check="RCA_internal",
            message="RCA contiene chiavi duplicate (stesso evento/ordine/tipo) - viene usata la prima occorrenza",
            context={"duplicate_keys": dup_rca},
        ))

    # Confronto
    all_keys = set(lta_rca.keys()) | set(rca_map.keys())
    for key_rca in sorted(all_keys):
        lta_bucket = lta_rca.get(key_rca)
        rca_rec = rca_map.get(key_rca)

        if lta_bucket is None:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RCA",
                message="Chiave presente in RCA ma assente in LTA",
                context={"key": "/".join(key_rca)},
            ))
            continue
        if rca_rec is None:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RCA",
                message="Chiave presente in LTA ma assente in RCA",
                context={"key": "/".join(key_rca)},
            ))
            continue

        for fld in rca_fields:
            lta_v = int(lta_bucket.get(fld, 0))
            rca_v = int(rca_rec.get(fld, 0) or 0)
            if lta_v != rca_v:
                issues.append(Issue(
                    severity="WARN",
                    check="LTA_vs_RCA",
                    message=f"Differenza conteggio {fld} tra LTA e RCA",
                    context={
                        "key": "/".join(key_rca),
                        "lta": lta_v,
                        "rca": rca_v,
                    },
                ))

    # -------------------------
    # 4.b) RCA internal: TotaleTitoliLTA = somma categorie
    # -------------------------
    for rr in rca_recs:
        tot = int(rr.get("TotaleTitoliLTA", 0) or 0)
        sum_cats = 0
        for fld in rca_fields:
            if fld == "TotaleTitoliLTA":
                continue
            sum_cats += int(rr.get(fld, 0) or 0)
        if tot != sum_cats:
            issues.append(Issue(
                severity="WARN",
                check="RCA_internal",
                message="RCA: TotaleTitoliLTA diverso dalla somma delle categorie",
                context={
                    "evento": f"{rr.get('DataEvento')} {rr.get('OraEvento')} {rr.get('CodiceLocale')} Ord={rr.get('CodiceOrdine')} Tipo={rr.get('TipoTitolo')}",
                    "totale": tot,
                    "somma_categorie": sum_cats,
                },
            ))

# 5) LOG vs RPM aggregations
    # -------------------------
    def agg_log(kind: str) -> Dict[Tuple[str, str, str, str, str, str], Dict[str, int]]:
        """
        kind: "TitoliAccesso" (emissioni) oppure "TitoliAnnullati" (annullamenti)
        chiave: (CFOrg, CodLocale, Data, Ora, Ordine, TipoTitolo)
        """
        out: Dict[Tuple[str, str, str, str, str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        rows = log_emis if kind == "TitoliAccesso" else log_ann
        for r in rows:
            key = (
                r.get("CFOrganizzatore") or "",
                r.get("CodiceLocale") or "",
                r.get("DataEvento") or "",
                r.get("OraEvento") or "",
                r.get("CodiceOrdine") or "",
                r.get("TipoTitolo") or "",
            )
            out[key]["Quantita"] += 1
            out[key]["CorrispettivoLordo"] += int(r.get("CorrispettivoLordo") or 0)
            out[key]["Prevendita"] += int(r.get("Prevendita") or 0)
            out[key]["IVACorrispettivo"] += int(r.get("IVACorrispettivo") or 0)
            out[key]["IVAPrevendita"] += int(r.get("IVAPrevendita") or 0)
        return out

    log_acc = agg_log("TitoliAccesso")
    log_can = agg_log("TitoliAnnullati")

    def compare_agg(log_map: Dict[Tuple[str, str, str, str, str, str], Dict[str, int]], rpm_kind: str) -> None:
        # build comparable rpm map for this kind
        rpm_map: Dict[Tuple[str, str, str, str, str, str], Dict[str, int]] = {}
        for (k_kind, cf, loc, data, ora, ordine, tipo), rr in rpm_by_key.items():
            if k_kind != rpm_kind:
                continue
            k2 = (cf, loc, data, ora, ordine, tipo)
            rpm_map[k2] = {
                "Quantita": int(rr.get("Quantita") or 0),
                "CorrispettivoLordo": int(rr.get("CorrispettivoLordo") or 0),
                "Prevendita": int(rr.get("Prevendita") or 0),
                "IVACorrispettivo": int(rr.get("IVACorrispettivo") or 0),
                "IVAPrevendita": int(rr.get("IVAPrevendita") or 0),
            }

        allk = set(log_map.keys())
        # Nota: RPM può contenere altri eventi non presenti nei LOG analizzati (es. mese completo).
        # Per evitare falsi positivi, qui confrontiamo solo le chiavi presenti nei LOG.
        for k2 in sorted(allk):
            lvals = log_map.get(k2, {"Quantita": 0, "CorrispettivoLordo": 0, "Prevendita": 0, "IVACorrispettivo": 0, "IVAPrevendita": 0})
            rvals = rpm_map.get(k2, {"Quantita": 0, "CorrispettivoLordo": 0, "Prevendita": 0, "IVACorrispettivo": 0, "IVAPrevendita": 0})
            for field in ("Quantita", "CorrispettivoLordo", "Prevendita", "IVACorrispettivo", "IVAPrevendita"):
                if int(lvals.get(field, 0)) != int(rvals.get(field, 0)):
                    issues.append(Issue(
                        severity="ERROR",
                        check="LOG_vs_RPM",
                        message=f"Mismatch {rpm_kind}.{field} tra LOG e RPM",
                        context={
                            "key": f"CF={k2[0]} Loc={k2[1]} Data={k2[2]} Ora={k2[3]} Ord={k2[4]} Tipo={k2[5]}",
                            "log": int(lvals.get(field, 0)),
                            "rpm": int(rvals.get(field, 0)),
                        },
                    ))

    compare_agg(log_acc, "TitoliAccesso")
    compare_agg(log_can, "TitoliAnnullati")

    # -------------------------
    
    # -------------------------
    # 6) LTA vs RPM (quantità per evento/ordine/tipo) - confronto "a parità di evento"
    # -------------------------
    # Nota: LTA è giornaliero, RPM è mensile. Per evitare falsi mismatch, confrontiamo solo
    # le chiavi evento/ordine/tipo presenti in LTA (quindi, gli eventi "in scope" per il giorno analizzato).

    # Aggregazione LTA
    lta_qty_accesso: Dict[Tuple[str, str, str, str, str, str], int] = Counter()
    lta_qty_ann: Dict[Tuple[str, str, str, str, str, str], int] = Counter()

    for r in lta_recs:
        key6 = (
            (r.get("CFOrganizzatore") or "").strip(),
            (r.get("CodiceLocale") or "").strip(),
            (r.get("DataEvento") or "").strip(),
            (r.get("OraEvento") or "").strip(),
            (r.get("CodiceOrdine") or "").strip(),
            (r.get("TipoTitolo") or "").strip(),
        )
        lta_qty_accesso[key6] += 1  # include anche titoli poi annullati (sono comunque titoli emessi)
        if (r.get("Annullamento") or "").upper() == "S":
            lta_qty_ann[key6] += 1

    # Aggregazione RPM
    rpm_qty_accesso: Dict[Tuple[str, str, str, str, str, str], int] = Counter()
    rpm_qty_ann: Dict[Tuple[str, str, str, str, str, str], int] = Counter()

    for rr in rpm_recs:
        kind = rr.get("kind") or ""
        key6 = (
            (rr.get("Organizzatore_CF") or "").strip(),
            (rr.get("CodiceLocale") or "").strip(),
            (rr.get("DataEvento") or "").strip(),
            (rr.get("OraEvento") or "").strip(),
            (rr.get("CodiceOrdine") or "").strip(),
            (rr.get("TipoTitolo") or "").strip(),
        )
        q = int(rr.get("Quantita", 0) or 0)
        if kind in ("TitoliAccesso", "TitoliAccessoIVAPreassolta"):
            rpm_qty_accesso[key6] += q
        elif kind in ("TitoliAnnullati", "TitoliIVAPreassoltaAnnullati"):
            rpm_qty_ann[key6] += q

    # Confronto per chiavi presenti in LTA
    for key6 in sorted(lta_qty_accesso.keys()):
        lta_acc = int(lta_qty_accesso.get(key6, 0))
        lta_ann = int(lta_qty_ann.get(key6, 0))

        rpm_acc = rpm_qty_accesso.get(key6, None)
        rpm_an = rpm_qty_ann.get(key6, None)

        if rpm_acc is None:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RPM",
                message="RPM: chiave (evento/ordine/tipo) presente in LTA ma assente in RPM (TitoliAccesso)",
                context={"key": "/".join(key6), "lta_TitoliAccesso": lta_acc},
            ))
        elif int(rpm_acc) != lta_acc:
            issues.append(Issue(
                severity="WARN",
                check="LTA_vs_RPM",
                message="Differenza TitoliAccesso tra LTA e RPM per evento/ordine/tipo",
                context={"key": "/".join(key6), "lta": lta_acc, "rpm": int(rpm_acc)},
            ))

        if rpm_an is None:
            # se in LTA non ci sono annullati per questa chiave, possiamo tollerare assenza (0 implicito)
            if lta_ann != 0:
                issues.append(Issue(
                    severity="WARN",
                    check="LTA_vs_RPM",
                    message="RPM: chiave presente in LTA ma assente in RPM (TitoliAnnullati)",
                    context={"key": "/".join(key6), "lta_TitoliAnnullati": lta_ann},
                ))
        else:
            if int(rpm_an) != lta_ann:
                issues.append(Issue(
                    severity="WARN",
                    check="LTA_vs_RPM",
                    message="Differenza TitoliAnnullati tra LTA e RPM per evento/ordine/tipo",
                    context={"key": "/".join(key6), "lta": lta_ann, "rpm": int(rpm_an)},
                ))

# 7) Fiscal checks - LOG IVA/ISI & ImponibileIntrattenimenti
    # -------------------------
    soglia_omaggi_cents = int(round(soglia_omaggi_eur * 100))

    # Prepare aliquote resolution
    resolved_rates: Dict[int, Tuple[float, float]] = {}  # TipoGenere -> (iva_rate, isi_rate)
    rate_notes: Dict[int, str] = {}

    if aliquote is None:
        issues.append(Issue(
            severity="WARN",
            check="FIS_LOG_IVA_ISI",
            message="File aliquote_tab1.csv non disponibile: i controlli fiscali possono essere incompleti",
            context={},
        ))
    else:
        # Resolve IVA rate for codes with multiple candidates by matching LOG values
        # Build event incidenza map from RPM
        inc_map: Dict[Tuple[str, str, str, str], int] = {}
        for k, ev in rpm_event_info.items():
            inc = ev.get("Incidenza")
            if inc is not None:
                inc_map[k] = int(inc)

        # group log by TipoGenere
        by_code: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        for r in log_recs:
            code = int(r.get("TipoGenere") or 0)
            if code:
                by_code[code].append(r)

        for code, rows in by_code.items():
            if code not in aliquote:
                resolved_rates[code] = (0.0, 0.0)
                rate_notes[code] = "Aliquota mancante in tab1 -> IVA=0, ISI=0 (fallback)"
                continue
            cand = aliquote[code].get("iva_candidates", [0.0]) or [0.0]
            isi_rate = float(aliquote[code].get("isi", 0.0))
            # se un solo candidato: scelgo quello
            if len(cand) == 1:
                resolved_rates[code] = (float(cand[0]), isi_rate)
                rate_notes[code] = "Aliquota IVA univoca"
                continue

            # prova ciascun candidato e conta mismatch su IVA_corr/prev e imponibile
            best = None
            best_mis = None
            for iva_rate in cand:
                mism = 0
                checked = 0
                for r in rows:
                    ev_key = (r.get("CFOrganizzatore") or "", r.get("CodiceLocale") or "", r.get("DataEvento") or "", r.get("OraEvento") or "")
                    inc = inc_map.get(ev_key)
                    if inc is None:
                        continue
                    checked += 1
                    corr = int(r.get("CorrispettivoLordo") or 0)
                    prev = int(r.get("Prevendita") or 0)
                    calc = calc_intr_sp_from_gross(corr + prev, inc, float(iva_rate), isi_rate)
                    iva_corr_exp, iva_prev_exp = split_iva_tot_corr_prev(calc["iva_tot"], corr, prev)
                    if iva_corr_exp != int(r.get("IVACorrispettivo") or 0):
                        mism += 1
                    if iva_prev_exp != int(r.get("IVAPrevendita") or 0):
                        mism += 1
                    if calc["imponibile_intr"] != int(r.get("ImponibileIntrattenimenti") or 0):
                        mism += 1
                if checked == 0:
                    continue
                if best_mis is None or mism < best_mis:
                    best_mis = mism
                    best = float(iva_rate)

            if best is None:
                resolved_rates[code] = (float(cand[0]), isi_rate)
                rate_notes[code] = f"Aliquota IVA variabile, scelta default {cand[0]*100:.0f}% (nessun record verificabile)"
            else:
                resolved_rates[code] = (best, isi_rate)
                rate_notes[code] = f"Aliquota IVA variabile, scelta {best*100:.0f}% (mismatch {best_mis})"

        metrics["Aliquote_resolved_codes"] = len(resolved_rates)

        # Now check each LOG record
        checked = 0
        skipped = 0
        mism = 0
        for r in log_recs:
            code = int(r.get("TipoGenere") or 0)
            ev_key = (r.get("CFOrganizzatore") or "", r.get("CodiceLocale") or "", r.get("DataEvento") or "", r.get("OraEvento") or "")
            ev_info = rpm_event_info.get(ev_key)
            inc = ev_info.get("Incidenza") if ev_info else None
            if inc is None:
                skipped += 1
                continue
            iva_rate, isi_rate = resolved_rates.get(code, (0.0, 0.0))
            corr = int(r.get("CorrispettivoLordo") or 0)
            prev = int(r.get("Prevendita") or 0)

            calc = calc_intr_sp_from_gross(corr + prev, int(inc), iva_rate, isi_rate)
            iva_corr_exp, iva_prev_exp = split_iva_tot_corr_prev(calc["iva_tot"], corr, prev)

            checked += 1

            if calc["imponibile_intr"] != int(r.get("ImponibileIntrattenimenti") or 0):
                mism += 1
                issues.append(Issue(
                    severity="ERROR",
                    check="FIS_LOG_IVA_ISI",
                    message="LOG: ImponibileIntrattenimenti non coerente con calcolo IVA/ISI",
                    context={
                        "titolo": r.get("key").short(),
                        "evento": f"{r.get('DataEvento')} {r.get('OraEvento')} {r.get('CodiceLocale')} Ord={r.get('CodiceOrdine')}",
                        "tipo_genere": code,
                        "incidenza": int(inc),
                        "expected": calc["imponibile_intr"],
                        "actual": int(r.get("ImponibileIntrattenimenti") or 0),
                    },
                ))

            if iva_corr_exp != int(r.get("IVACorrispettivo") or 0):
                mism += 1
                issues.append(Issue(
                    severity="ERROR",
                    check="FIS_LOG_IVA_ISI",
                    message="LOG: IVACorrispettivo non coerente con calcolo IVA (ripartizione proporzionale)",
                    context={
                        "titolo": r.get("key").short(),
                        "evento": f"{r.get('DataEvento')} {r.get('OraEvento')} {r.get('CodiceLocale')} Ord={r.get('CodiceOrdine')}",
                        "expected": iva_corr_exp,
                        "actual": int(r.get("IVACorrispettivo") or 0),
                    },
                ))

            if iva_prev_exp != int(r.get("IVAPrevendita") or 0):
                mism += 1
                issues.append(Issue(
                    severity="ERROR",
                    check="FIS_LOG_IVA_ISI",
                    message="LOG: IVAPrevendita non coerente con calcolo IVA (ripartizione proporzionale)",
                    context={
                        "titolo": r.get("key").short(),
                        "evento": f"{r.get('DataEvento')} {r.get('OraEvento')} {r.get('CodiceLocale')} Ord={r.get('CodiceOrdine')}",
                        "expected": iva_prev_exp,
                        "actual": int(r.get("IVAPrevendita") or 0),
                    },
                ))

        metrics["FIS_LOG_checked"] = checked
        metrics["FIS_LOG_skipped_no_incidenza"] = skipped
        metrics["FIS_LOG_mismatches"] = mism

    # -------------------------
        # -------------------------
    # 8) Fiscal checks - RPM eccedenza omaggi & imponibile intrattenimenti
    # -------------------------
    # Scope: per evitare falsi positivi quando i LOG/LTA sono parziali (es. solo un giorno),
    # in questa sezione calcoliamo e confrontiamo solo gli eventi/ordini presenti nei LOG analizzati.

    # Group LOG per evento/ordine (netto, considerando annullamenti)
    log_groups: Dict[Tuple[str, str, str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    log_events: Dict[Tuple[str, str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in log_recs:
        ok = (r.get("CFOrganizzatore") or "", r.get("CodiceLocale") or "", r.get("DataEvento") or "", r.get("OraEvento") or "", r.get("CodiceOrdine") or "")
        ek = (r.get("CFOrganizzatore") or "", r.get("CodiceLocale") or "", r.get("DataEvento") or "", r.get("OraEvento") or "")
        log_groups[ok].append(r)
        log_events[ek].append(r)

    # Net ImponibileIntrattenimenti (LOG) per evento
    net_imp_event_log: Dict[Tuple[str, str, str, str], int] = defaultdict(int)
    for ek, rows in log_events.items():
        for r in rows:
            sign = 1 if r.get("Annullamento") == "N" else -1
            net_imp_event_log[ek] += sign * int(r.get("ImponibileIntrattenimenti") or 0)

    # Helper: count omaggi net
    def count_omaggi_net(rows: List[Dict[str, Any]]) -> int:
        cnt = 0
        for r in rows:
            sign = 1 if r.get("Annullamento") == "N" else -1
            tipo = r.get("TipoTitolo") or ""
            if tipo.startswith("O") and int(r.get("CorrispettivoLordo") or 0) == 0 and int(r.get("Prevendita") or 0) == 0:
                cnt += sign
        return cnt

    # Helper: max price title (corrispettivo, no prevendita)
    def max_title_price(rows: List[Dict[str, Any]]) -> Tuple[int, Optional[int], str]:
        max_price = 0
        max_gen: Optional[int] = None
        source = "LOG"
        for r in rows:
            tipo = r.get("TipoTitolo") or ""
            corr = int(r.get("CorrispettivoLordo") or 0)
            # escludo omaggi
            if corr > 0 and not tipo.startswith("O"):
                if corr > max_price:
                    max_price = corr
                    max_gen = int(r.get("TipoGenere") or 0) or None
        if max_gen is None:
            # fallback: tipo genere più frequente nel gruppo
            c = Counter([int(r.get("TipoGenere") or 0) for r in rows if int(r.get("TipoGenere") or 0) != 0])
            if c:
                max_gen = c.most_common(1)[0][0]
        return max_price, max_gen, source

    # Build RPM omaggi counts (net: accesso - annullati) (solo per confronto)
    rpm_omaggi_net: Dict[Tuple[str, str, str, str, str], int] = defaultdict(int)
    for rr in rpm_recs:
        kind = rr.get("kind")
        if kind not in ("TitoliAccesso", "TitoliAnnullati"):
            continue
        tipo = rr.get("TipoTitolo") or ""
        if not tipo.startswith("O"):
            continue
        # consider only zero-value titles as omaggi
        if int(rr.get("CorrispettivoLordo") or 0) != 0 or int(rr.get("Prevendita") or 0) != 0:
            continue
        key = (rr.get("Organizzatore_CF") or "", rr.get("CodiceLocale") or "", rr.get("DataEvento") or "", rr.get("OraEvento") or "", rr.get("CodiceOrdine") or "")
        q = int(rr.get("Quantita") or 0)
        if kind == "TitoliAccesso":
            rpm_omaggi_net[key] += q
        else:
            rpm_omaggi_net[key] -= q

    # Accumulatori per check evento (ImponibileIntrattenimenti)
    additions_by_event: Dict[Tuple[str, str, str, str], int] = defaultdict(int)
    event_inferred: Dict[Tuple[str, str, str, str], bool] = defaultdict(bool)
    rpm_imp_by_event: Dict[Tuple[str, str, str, str], Optional[int]] = {}
    for ek, ev_rr in rpm_event_info.items():
        rpm_imp_by_event[ek] = ev_rr.get("ImponibileIntrattenimenti")

    # Iteriamo SOLO sugli ordini presenti nei LOG (scope)
    all_order_keys = set(log_groups.keys())

    for ok in sorted(all_order_keys):
        cf, loc, data, ora, ordine = ok
        rows = log_groups.get(ok, [])
        event_key = (cf, loc, data, ora)

        order_rr = rpm_order_info.get(ok)
        event_rr = rpm_event_info.get(event_key)

        capienza = order_rr.get("Capienza") if order_rr else None
        rpm_iva_ecc = int(order_rr.get("IVAEccedenteOmaggi") or 0) if order_rr else None
        inc = event_rr.get("Incidenza") if event_rr else None
        rpm_imp_intr_event = rpm_imp_by_event.get(event_key)

        om_log = count_omaggi_net(rows) if rows else 0
        om_rpm = rpm_omaggi_net.get(ok) if ok in rpm_omaggi_net else None

        if capienza is None or inc is None:
            # Senza capienza o incidenza non si può calcolare in modo affidabile
            continue

        allowed = int(math.floor((capienza * omaggi_pct) / 100.0))
        ecc = max(0, int(om_log) - allowed)

        # prezzo massimo del titolo (no prevendita)
        max_price, max_gen, price_source = max_title_price(rows)
        inferred = False

        # se manca, prova da BigliettiAbbonamento RPM
        if max_price <= 0:
            best = 0
            for rr in rpm_recs:
                if rr.get("kind") != "BigliettiAbbonamento":
                    continue
                if (rr.get("Organizzatore_CF") or "", rr.get("CodiceLocale") or "", rr.get("DataEvento") or "", rr.get("OraEvento") or "", rr.get("CodiceOrdine") or "") != ok:
                    continue
                q = int(rr.get("Quantita") or 0)
                imp = int(rr.get("ImportoFigurativo") or 0)
                if q > 0 and imp > 0:
                    unit = int(round_half_up_int(Decimal(imp) / Decimal(q)))
                    if unit > best:
                        best = unit
            if best > 0:
                max_price = best
                price_source = "RPM_BigliettiAbbonamento"
                inferred = True

        # se ancora manca e abbiamo RPM imponibile evento, inferisci un prezzo massimo (solo per spiegazione/verifica interna)
        if max_price <= 0 and ecc > 0 and rpm_imp_intr_event is not None:
            diff = int(rpm_imp_intr_event) - int(net_imp_event_log.get(event_key, 0))
            if diff > 0:
                base_unit_est = diff // ecc
                if max_gen is None:
                    c = Counter([int(r.get("TipoGenere") or 0) for r in rows if int(r.get("TipoGenere") or 0) != 0])
                    if c:
                        max_gen = c.most_common(1)[0][0]
                iva_rate, isi_rate = resolved_rates.get(max_gen or 0, (0.0, 0.0))
                denom_intr = (1.0 + iva_rate + isi_rate)
                quota_intr_est = int(round(base_unit_est * denom_intr))
                gross_est = int(round(quota_intr_est * 100 / int(inc))) if int(inc) != 0 else quota_intr_est
                cand_price = None
                for g in range(max(0, gross_est - 5000), gross_est + 5001):
                    calc = calc_intr_sp_from_gross(g, int(inc), iva_rate, isi_rate)
                    if calc["imponibile_intr"] == base_unit_est:
                        cand_price = g
                        break
                if cand_price is not None and cand_price > 0:
                    max_price = cand_price
                    price_source = "INFERITO_DA_RPM"
                    inferred = True

        if max_gen is None:
            # Senza tipo genere non posso collegare aliquote
            continue

        iva_rate, isi_rate = resolved_rates.get(max_gen, (0.0, 0.0))

        # calcolo unitario sulla sola quota intrattenimento del titolo (prezzo * incidenza)
        unit_calc = calc_intr_sp_from_gross(max_price, int(inc), iva_rate, isi_rate)
        quota_intr_unit = unit_calc["quota_intr"]
        iva_intr_unit = unit_calc["iva_intr"]
        isi_unit = unit_calc["isi"]
        imponibile_intr_unit = unit_calc["imponibile_intr"]

        # regola soglia: valore unitario LORDO della QUOTA INTRATTENIMENTO del titolo di riferimento
        # (per biglietto: CorrispettivoLordo senza prevendita * Incidenza%; per rateo: importo figurativo unitario * Incidenza%)
        if quota_intr_unit <= soglia_omaggi_cents:
            expected_iva_ecc = 0
            soglia_flag = True
        else:
            expected_iva_ecc = ecc * iva_intr_unit
            soglia_flag = False

        # contribuzione dell'ordine all'imponibile evento
        addition_imp = ecc * imponibile_intr_unit
        additions_by_event[event_key] += addition_imp
        if inferred:
            event_inferred[event_key] = True

        # details row (l'Expected_ImponibileIntr_evento verrà compilato dopo, a livello evento)
        details["fiscale_omaggi"].append({
            "CF": cf,
            "CodiceLocale": loc,
            "DataEvento": data,
            "OraEvento": ora,
            "CodiceOrdine": ordine,
            "Capienza": capienza,
            "Incidenza": int(inc),
            "Omaggi_LOG_net": om_log,
            "Omaggi_RPM_net": om_rpm,
            "Omaggi_usati": om_log,
            "Omaggi_consentiti": allowed,
            "Eccedenza": ecc,
            "PrezzoMax_Corrispettivo": max_price if max_price > 0 else None,
            "PrezzoMax_source": price_source,
            "TipoGenere": max_gen,
            "IVA_rate": iva_rate,
            "ISI_rate": isi_rate,
            "QuotaIntr_unit": quota_intr_unit,
            "ImponibileIntr_unit": imponibile_intr_unit,
            "IVAIntr_unit": iva_intr_unit,
            "ISI_unit": isi_unit,
            "Soglia_applicata": soglia_flag,
            "Expected_IVAEccedenteOmaggi": expected_iva_ecc,
            "RPM_IVAEccedenteOmaggi": rpm_iva_ecc,
            "ImponibileIntr_addition": addition_imp,
            "Net_ImponibileIntr_LOG_evento": net_imp_event_log.get(event_key, 0),
            "Expected_ImponibileIntr_evento": None,  # filled later
            "RPM_ImponibileIntr_evento": rpm_imp_intr_event,
            "Inferred_price": inferred,
        })

        # confronto omaggi LOG vs RPM (se entrambi presenti)
        if om_rpm is not None and int(om_log) != int(om_rpm):
            issues.append(Issue(
                severity="WARN",
                check="FIS_RPM_OMAGGI",
                message="Differenza conteggio omaggi net tra LOG e RPM (può indicare set di LOG incompleto)",
                context={
                    "evento": f"{data} {ora} {loc} Ord={ordine}",
                    "omaggi_log": om_log,
                    "omaggi_rpm": om_rpm,
                },
            ))

        # check IVAEccedenteOmaggi (per ordine)
        if rpm_iva_ecc is not None and int(rpm_iva_ecc) != int(expected_iva_ecc):
            sev = "WARN" if inferred else "ERROR"
            issues.append(Issue(
                severity=sev,
                check="FIS_RPM_OMAGGI",
                message="RPM: IVAEccedenteOmaggi non coerente con calcolo eccedenza omaggi (quota Intrattenimento, no prevendita)",
                context={
                    "evento": f"{data} {ora} {loc} Ord={ordine}",
                    "capienza": capienza,
                    "omaggi_net": om_log,
                    "consentiti": allowed,
                    "eccedenza": ecc,
                    "prezzo_max_corr": max_price,
                    "incidenza": int(inc),
                    "tipo_genere": max_gen,
                    "iva_unit": iva_intr_unit,
                    "imponibile_unit": imponibile_intr_unit,
                    "soglia_omaggi_cents": soglia_omaggi_cents,
                    "expected": expected_iva_ecc,
                    "rpm": int(rpm_iva_ecc),
                    "note": "prezzo inferito" if inferred else "",
                },
            ))

        if inferred:
            issues.append(Issue(
                severity="INFO",
                check="FIS_RPM_OMAGGI",
                message="Prezzo massimo non determinabile dal LOG: stimato/inferito per permettere la verifica (attenzione: controllo non indipendente al 100%)",
                context={
                    "evento": f"{data} {ora} {loc} Ord={ordine}",
                    "prezzo_max_corr_stimato": max_price,
                    "fonte": price_source,
                },
            ))

    # Check evento: ImponibileIntrattenimenti (una volta per evento)
    expected_imp_event: Dict[Tuple[str, str, str, str], int] = {}
    for ek, net_log in net_imp_event_log.items():
        expected = int(net_log) + int(additions_by_event.get(ek, 0))
        expected_imp_event[ek] = expected
        rpm_val = rpm_imp_by_event.get(ek)
        if rpm_val is None:
            continue
        if int(rpm_val) != int(expected):
            sev = "WARN" if event_inferred.get(ek, False) else "ERROR"
            issues.append(Issue(
                severity=sev,
                check="FIS_RPM_IMP_INTR",
                message="RPM: ImponibileIntrattenimenti evento non coerente con LOG netto + imponibile eccedenza omaggi (somma ordini)",
                context={
                    "evento": f"{ek[2]} {ek[3]} {ek[1]}",
                    "net_log_event": int(net_log),
                    "add_omaggi_event": int(additions_by_event.get(ek, 0)),
                    "expected": int(expected),
                    "rpm": int(rpm_val),
                    "note": "prezzo inferito in almeno un ordine" if event_inferred.get(ek, False) else "",
                },
            ))

    # Riempiamo l'expected evento dentro le righe di dettaglio (per comodità di report)
    for row in details.get("fiscale_omaggi", []):
        ek = (row.get("CF") or "", row.get("CodiceLocale") or "", row.get("DataEvento") or "", row.get("OraEvento") or "")
        if ek in expected_imp_event:
            row["Expected_ImponibileIntr_evento"] = expected_imp_event[ek]

    # -------------------------
    # 9) Riepilogo fiscale per evento e TipoTitolo (LOG, al netto degli annulli)
    # -------------------------
    # Questo riepilogo serve a mettere in evidenza quanto lo script ricostruisce (calcolo-ISI)
    # per ciascuna tipologia di titolo (I1, R1, O*, ...), al netto degli annullamenti.
    # Importi calcolati su Corrispettivo+Prevendita (LOG), con Incidenza da RPM e aliquote Tab.1.
    event_type_acc: Dict[Tuple[str, str, str, str], Dict[str, Dict[str, int]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    event_meta: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}

    for r in log_recs:
        ek = (
            (r.get("CFOrganizzatore") or "").strip(),
            (r.get("CodiceLocale") or "").strip(),
            (r.get("DataEvento") or "").strip(),
            (r.get("OraEvento") or "").strip(),
        )
        tipo = (r.get("TipoTitolo") or "").strip() or "(n/d)"
        inc = inc_map.get(ek)
        if inc is None:
            # senza incidenza non possiamo applicare il calcolo-ISI in modo coerente
            continue

        code = int(r.get("TipoGenere") or 0)
        iva_rate, isi_rate = resolved_rates.get(code, (0.0, 0.0))

        corr = int(r.get("CorrispettivoLordo") or 0)
        prev = int(r.get("Prevendita") or 0)
        calc = calc_intr_sp_from_gross(corr + prev, int(inc), float(iva_rate), float(isi_rate))

        sign = 1 if (r.get("Annullamento") or "").upper() == "N" else -1
        acc = event_type_acc[ek][tipo]
        acc["TitoliNetti"] += sign
        if (r.get("Annullamento") or "").upper() == "S":
            acc["TitoliAnnullati"] += 1

        # Imponibile imposta: esposto solo quando ISI > 0 ("dove previsto")
        acc["ImponibileImposta"] += sign * (calc["imponibile_intr"] if float(isi_rate) > 0.0 else 0)
        acc["ImpostaIntrattenimento"] += sign * int(calc["isi"])
        acc["ImponibileIVA"] += sign * int(calc["imponibile_intr"] + calc["imponibile_sp"])
        acc["IVALorda"] += sign * int(calc["iva_tot"])

        if ek not in event_meta:
            ev_rr = rpm_event_info.get(ek)
            event_meta[ek] = {
                "CF": ek[0],
                "CodiceLocale": ek[1],
                "DenominazioneLocale": (ev_rr.get("DenominazioneLocale") if ev_rr else "") or "",
                "DataEvento": ek[2],
                "OraEvento": ek[3],
                "Incidenza": int(inc),
                "TipoTassazione": (ev_rr.get("TipoTassazione") if ev_rr else "") or "",
                "TitoloEvento": (r.get("TitoloEvento") or ""),
            }

    fisc_ev_tables: List[Dict[str, Any]] = []
    for ek in sorted(event_type_acc.keys(), key=lambda x: (x[2], x[3], x[1], x[0])):
        meta = event_meta.get(ek, {
            "CF": ek[0],
            "CodiceLocale": ek[1],
            "DenominazioneLocale": "",
            "DataEvento": ek[2],
            "OraEvento": ek[3],
            "Incidenza": inc_map.get(ek),
            "TipoTassazione": "",
            "TitoloEvento": "",
        })
        rows: List[Dict[str, Any]] = []
        totals = {"TitoliNetti": 0, "TitoliAnnullati": 0, "ImponibileImposta": 0, "ImpostaIntrattenimento": 0, "ImponibileIVA": 0, "IVALorda": 0}
        for tipo in sorted(event_type_acc[ek].keys()):
            v = event_type_acc[ek][tipo]
            row = {
                "TipoTitolo": tipo,
                "TitoliNetti": int(v.get("TitoliNetti", 0)),
                "TitoliAnnullati": int(v.get("TitoliAnnullati", 0)),
                "ImponibileImposta": int(v.get("ImponibileImposta", 0)),
                "ImpostaIntrattenimento": int(v.get("ImpostaIntrattenimento", 0)),
                "ImponibileIVA": int(v.get("ImponibileIVA", 0)),
                "IVALorda": int(v.get("IVALorda", 0)),
            }
            rows.append(row)
            for kf in totals.keys():
                totals[kf] += int(row.get(kf, 0))
        fisc_ev_tables.append({**meta, "rows": rows, "totals": totals})

    details["fiscale_evento_titoli"] = fisc_ev_tables
    metrics["FIS_event_tables"] = len(fisc_ev_tables)

# -------------------------
    # Build summary per check
    # -------------------------
    checks_summary: Dict[str, Dict[str, int]] = {}
    # init all checks
    for ck in CHECK_DEFS.keys():
        checks_summary[ck] = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for iss in issues:
        if iss.check not in checks_summary:
            checks_summary[iss.check] = {"ERROR": 0, "WARN": 0, "INFO": 0}
        checks_summary[iss.check][iss.severity] += 1

    # overall
    total_errors = sum(v["ERROR"] for v in checks_summary.values())
    total_warns = sum(v["WARN"] for v in checks_summary.values())
    total_infos = sum(v["INFO"] for v in checks_summary.values())

    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totals": {"ERROR": total_errors, "WARN": total_warns, "INFO": total_infos},
        "checks": checks_summary,
        "check_descriptions": CHECK_DEFS,
        "params": {
            "omaggi_pct_capienza": omaggi_pct,
            "soglia_omaggi_eur": soglia_omaggi_eur,
        },
    }

    return summary, issues, metrics, details


# -------------------------
# HTML report
# -------------------------

def _status_from_counts(c: Dict[str, int]) -> str:
    if c.get("ERROR", 0) > 0:
        return "ERROR"
    if c.get("WARN", 0) > 0:
        return "WARN"
    return "OK"


def build_html_report(summary: Dict[str, Any], issues: List[Issue], metrics: Dict[str, Any], details: Dict[str, Any]) -> str:
    totals = summary["totals"]
    checks = summary["checks"]
    descs = summary.get("check_descriptions", {})
    params = summary.get("params", {})

    # Cards
    cards = [
        ("Errori", totals["ERROR"]),
        ("Avvisi", totals["WARN"]),
        ("Info", totals["INFO"]),
        ("LOG", metrics.get("LOG_records", 0)),
        ("LTA", metrics.get("LTA_records", 0)),
        ("RCA", metrics.get("RCA_records", 0)),
        ("RPM", metrics.get("RPM_records", 0)),
    ]

    def badge(status: str) -> str:
        cls = {"OK": "b-ok", "WARN": "b-warn", "ERROR": "b-err"}.get(status, "b-ok")
        return f'<span class="badge {cls}">{html.escape(status)}</span>'

    # Checks table rows
    check_rows_html = []
    for ck in sorted(checks.keys()):
        c = checks[ck]
        st = _status_from_counts(c)
        check_rows_html.append(
            "<tr>"
            f"<td><code>{html.escape(ck)}</code><div class='muted'>{html.escape(descs.get(ck,''))}</div></td>"
            f"<td>{badge(st)}</td>"
            f"<td class='num'>{c.get('ERROR',0)}</td>"
            f"<td class='num'>{c.get('WARN',0)}</td>"
            f"<td class='num'>{c.get('INFO',0)}</td>"
            "</tr>"
        )

    # Issues grouped
    issues_sorted = sorted(issues, key=lambda x: ({"ERROR":0,"WARN":1,"INFO":2}.get(x.severity,9), x.check, x.message))
    issue_blocks = []
    for iss in issues_sorted:
        ctx = "<br/>".join(f"<b>{html.escape(str(k))}</b>: {html.escape(str(v))}" for k, v in iss.context.items())
        issue_blocks.append(
            f"<div class='issue {iss.severity.lower()}'>"
            f"<div class='issue-head'><span class='sev'>{html.escape(iss.severity)}</span> "
            f"<code>{html.escape(iss.check)}</code> — {html.escape(iss.message)}</div>"
            f"<div class='issue-ctx'>{ctx}</div>"
            f"</div>"
        )

    # Fiscale omaggi table
    fisc_rows = details.get("fiscale_omaggi", [])
    fisc_table_html = ""
    if fisc_rows:
        # keep deterministic order
        fisc_rows_sorted = sorted(fisc_rows, key=lambda r: (r.get("DataEvento",""), r.get("OraEvento",""), r.get("CodiceLocale",""), r.get("CodiceOrdine","")))
        rows_html = []
        for r in fisc_rows_sorted:
            rows_html.append(
                "<tr>"
                f"<td>{html.escape(r.get('DataEvento',''))}</td>"
                f"<td>{html.escape(r.get('OraEvento',''))}</td>"
                f"<td>{html.escape(r.get('CodiceLocale',''))}</td>"
                f"<td>{html.escape(r.get('CodiceOrdine',''))}</td>"
                f"<td class='num'>{r.get('Capienza','')}</td>"
                f"<td class='num'>{'' if r.get('Omaggi_LOG_net') is None else r.get('Omaggi_LOG_net')}</td>"
                f"<td class='num'>{'' if r.get('Omaggi_RPM_net') is None else r.get('Omaggi_RPM_net')}</td>"
                f"<td class='num'>{r.get('Omaggi_consentiti','')}</td>"
                f"<td class='num'>{r.get('Eccedenza','')}</td>"
                f"<td class='num'>{cents_to_eur_str(int(r.get('PrezzoMax_Corrispettivo') or 0)) if r.get('PrezzoMax_Corrispettivo') else 'n/d'}</td>"
                f"<td>{html.escape(str(r.get('PrezzoMax_source','')))}</td>"
                f"<td class='num'>{r.get('Incidenza','')}</td>"
                f"<td class='num'>{int(round((r.get('IVA_rate') or 0)*100))}%</td>"
                f"<td class='num'>{int(round((r.get('ISI_rate') or 0)*100))}%</td>"
                f"<td class='num'>{cents_to_eur_str(int(r.get('ImponibileIntr_unit') or 0))}</td>"
                f"<td class='num'>{cents_to_eur_str(int(r.get('IVAIntr_unit') or 0))}</td>"
                f"<td>{'Sì' if r.get('Soglia_applicata') else 'No'}</td>"
                f"<td class='num'>{cents_to_eur_str(int(r.get('Expected_IVAEccedenteOmaggi') or 0))}</td>"
                f"<td class='num'>{('n/d' if r.get('RPM_IVAEccedenteOmaggi') is None else cents_to_eur_str(int(r.get('RPM_IVAEccedenteOmaggi') or 0)))}</td>"
                f"<td class='num'>{'n/d' if r.get('Expected_ImponibileIntr_evento') is None else cents_to_eur_str(int(r.get('Expected_ImponibileIntr_evento') or 0))}</td>"
                f"<td class='num'>{'n/d' if r.get('RPM_ImponibileIntr_evento') is None else cents_to_eur_str(int(r.get('RPM_ImponibileIntr_evento') or 0))}</td>"
                "</tr>"
            )

        fisc_table_html = f"""
        <details open>
          <summary><b>Dettaglio calcolo eccedenza omaggi</b> (righe: {len(fisc_rows_sorted)})</summary>
          <div class="hint">
            Regola: eccedenza = omaggi_net - floor(capienza * {params.get('omaggi_pct_capienza',5)}%). 
            Prezzo max = CorrispettivoLordo più alto (esclude prevendita), o rateo abbonamento se maggiore.
            Soglia lordo unitario (quota Intrattenimento): {params.get('soglia_omaggi_eur',50.00):.2f} €.
            Nota arrotondamenti: calcolo IVA/ISI per singolo titolo (round half-up) e poi moltiplica sull’eccedenza; un calcolo 'sul totale' può differire di 1 cent.
          </div>
          <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Data</th><th>Ora</th><th>Locale</th><th>Ordine</th>
                <th class='num'>Capienza</th>
                <th class='num'>Omaggi LOG net</th>
                <th class='num'>Omaggi RPM net</th>
                <th class='num'>Omaggi ammessi</th>
                <th class='num'>Eccedenza</th>
                <th class='num'>Prezzo max</th>
                <th>Fonte</th>
                <th class='num'>Inc%</th>
                <th class='num'>IVA%</th>
                <th class='num'>ISI%</th>
                <th class='num'>Imp. unit</th>
                <th class='num'>IVA unit</th>
                <th>Soglia</th>
                <th class='num'>IVA ecc attesa</th>
                <th class='num'>IVA ecc RPM</th>
                <th class='num'>Imp. evento atteso</th><th class='num'>Imp. evento RPM</th>
              </tr>
            </thead>
            <tbody>
              {''.join(rows_html)}
            </tbody>
          </table>
          </div>
        </details>
        """


    # Riepilogo fiscale per evento/tipologia (LOG, netto annulli)
    ev_tables = details.get("fiscale_evento_titoli", [])
    ev_tables_html = ""
    if ev_tables:
        ev_tables_sorted = sorted(ev_tables, key=lambda e: (e.get("DataEvento", ""), e.get("OraEvento", ""), e.get("CodiceLocale", ""), e.get("CF", "")))
        blocks: List[str] = []
        for e in ev_tables_sorted:
            rows = e.get("rows", []) or []
            totals = e.get("totals", {}) or {}
            row_html: List[str] = []
            for r in rows:
                row_html.append(
                    "<tr>"
                    f"<td><code>{html.escape(str(r.get('TipoTitolo','')))}</code></td>"
                    f"<td class='num'>{html.escape(str(r.get('TitoliNetti',0)))}</td>"
                    f"<td class='num'>{html.escape(str(r.get('TitoliAnnullati',0)))}</td>"
                    f"<td class='num'>{cents_to_eur_str(int(r.get('ImponibileImposta',0) or 0))}</td>"
                    f"<td class='num'>{cents_to_eur_str(int(r.get('ImpostaIntrattenimento',0) or 0))}</td>"
                    f"<td class='num'>{cents_to_eur_str(int(r.get('ImponibileIVA',0) or 0))}</td>"
                    f"<td class='num'>{cents_to_eur_str(int(r.get('IVALorda',0) or 0))}</td>"
                    "</tr>"
                )

            # Totali evento
            row_html.append(
                "<tr class='tot'>"
                "<td><b>Totale</b></td>"
                f"<td class='num'><b>{html.escape(str(totals.get('TitoliNetti',0)))}</b></td>"
                f"<td class='num'><b>{html.escape(str(totals.get('TitoliAnnullati',0)))}</b></td>"
                f"<td class='num'><b>{cents_to_eur_str(int(totals.get('ImponibileImposta',0) or 0))}</b></td>"
                f"<td class='num'><b>{cents_to_eur_str(int(totals.get('ImpostaIntrattenimento',0) or 0))}</b></td>"
                f"<td class='num'><b>{cents_to_eur_str(int(totals.get('ImponibileIVA',0) or 0))}</b></td>"
                f"<td class='num'><b>{cents_to_eur_str(int(totals.get('IVALorda',0) or 0))}</b></td>"
                "</tr>"
            )

            denom = (e.get("DenominazioneLocale") or "").strip()
            loc = (e.get("CodiceLocale") or "").strip()
            titolo_ev = (e.get("TitoloEvento") or "").strip()
            inc = e.get("Incidenza")
            tipotass = (e.get("TipoTassazione") or "").strip()

            header_txt = f"{e.get('DataEvento','')} {e.get('OraEvento','')} — "
            if denom:
                header_txt += f"{denom} "
            header_txt += f"({loc})"
            if titolo_ev:
                header_txt += f" — {titolo_ev}"

            extra_parts = []
            if inc is not None and str(inc) != "":
                extra_parts.append(f"Incidenza {inc}%")
            if tipotass:
                extra_parts.append(f"Tassazione {tipotass}")
            extra_txt = (" — " + ", ".join(extra_parts)) if extra_parts else ""

            blocks.append(
                f"""
                <details open>
                  <summary><b>{html.escape(header_txt)}</b>{html.escape(extra_txt)}</summary>
                  <div class=\"table-wrap\">
                    <table>
                      <thead>
                        <tr>
                          <th>TipoTitolo</th>
                          <th class='num'>Titoli netti</th>
                          <th class='num'>Annullati</th>
                          <th class='num'>Imponibile imposta</th>
                          <th class='num'>Imposta intratt.</th>
                          <th class='num'>Imponibile IVA</th>
                          <th class='num'>IVA lorda</th>
                        </tr>
                      </thead>
                      <tbody>
                        {''.join(row_html)}
                      </tbody>
                    </table>
                  </div>
                </details>
                """
            )

        ev_tables_html = f"""
        <details open>
          <summary><b>Riepilogo fiscale per evento e tipologia titolo (LOG, netto annulli)</b> (eventi: {len(ev_tables_sorted)})</summary>
          <div class=\"hint\">
            Valori calcolati dallo script sui LOG (Corrispettivo+Prevendita), usando Incidenza da RPM e aliquote da TAB.1.
            La colonna “Imponibile imposta” è valorizzata solo dove l’ISI è prevista.
          </div>
          {''.join(blocks)}
        </details>
        """
    # Metrics KV
    kv_rows = []
    for k in sorted(metrics.keys()):
        kv_rows.append(f"<tr><td>{html.escape(str(k))}</td><td class='num'>{html.escape(str(metrics[k]))}</td></tr>")

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
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 0 1px 0 rgba(17,24,39,0.03);
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
    h2 {{
        font-size: 15px;
        margin: 18px 0 10px;
    }}
    .table-wrap {{
        overflow: auto;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        font-size: 13px;
    }}
    th, td {{
        padding: 10px 10px;
        border-bottom: 1px solid #eef2f7;
        vertical-align: top;
    }}
    th {{
        text-align: left;
        position: sticky;
        top: 0;
        background: #f9fafb;
        z-index: 1;
        font-weight: 700;
        color: #374151;
    }}
    td.num {{
        text-align: right;
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }}
    code {{
        background: #f3f4f6;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 12px;
    }}
    .muted {{
        color: #6b7280;
        font-size: 12px;
        margin-top: 2px;
    }}
    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        color: white;
        line-height: 18px;
    }}
    .b-ok {{ background: #059669; }}
    .b-warn {{ background: #d97706; }}
    .b-err {{ background: #dc2626; }}

    .issues {{
        display: grid;
        gap: 10px;
        margin-top: 10px;
    }}
    .issue {{
        background: white;
        border: 1px solid #e5e7eb;
        border-left-width: 6px;
        border-radius: 12px;
        padding: 10px 12px;
    }}
    .issue.error {{ border-left-color: #dc2626; }}
    .issue.warn {{ border-left-color: #d97706; }}
    .issue.info {{ border-left-color: #2563eb; }}
    .issue-head {{
        font-size: 13px;
        margin-bottom: 6px;
        display: flex;
        gap: 8px;
        align-items: baseline;
        flex-wrap: wrap;
    }}
    .issue-head .sev {{
        font-weight: 900;
    }}
    .issue-ctx {{
        font-size: 12px;
        color: #374151;
        line-height: 1.35;
    }}
    details summary {{
        cursor: pointer;
        margin: 10px 0;
    }}
    .hint {{
        font-size: 12px;
        color: #6b7280;
        margin: 8px 0 10px;
    }}
    tr.tot td {{
        font-weight: 800;
        background: #f9fafb;
    }}

</style>
</head>
<body>
<header>
  <h1>Report consistenza biglietteria</h1>
  <div class="sub">Generato: {html.escape(summary.get('generated_at',''))}</div>
</header>
<div class="wrap">
  <div class="cards">
    {''.join([f"<div class='card'><div class='k'>{html.escape(k)}</div><div class='v'>{html.escape(str(v))}</div></div>" for k,v in cards])}
  </div>

  <h2>Controlli eseguiti</h2>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Controllo</th><th>Esito</th><th class="num">Errori</th><th class="num">Avvisi</th><th class="num">Info</th></tr></thead>
      <tbody>
        {''.join(check_rows_html)}
      </tbody>
    </table>
  </div>

  {ev_tables_html}
  {fisc_table_html}

  <h2>Metriche</h2>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Voce</th><th class="num">Valore</th></tr></thead>
      <tbody>{''.join(kv_rows)}</tbody>
    </table>
  </div>

  <h2>Dettaglio anomalie</h2>
  <div class="issues">
    {''.join(issue_blocks) if issue_blocks else "<div class='muted'>Nessuna anomalia rilevata.</div>"}
  </div>

  <div class="hint" style="margin-top:16px;">
    Parametri: omaggi_pct_capienza={params.get('omaggi_pct_capienza',5)}, soglia_omaggi_lordo={params.get('soglia_omaggi_eur',50.00)} €.
  </div>
</div>
</body>
</html>
"""
    return html_doc


# -------------------------
# Main CLI
# -------------------------

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Verifica consistenza biglietteria (LOG/LTA/RCA/RPM) con controlli fiscali.")
    ap.add_argument("directory", nargs="?", default=".", help="Cartella contenente i file .xsi/.xml/.csv")
    ap.add_argument("--out", default=None, help="Percorso report HTML di output (default: report_verifica.html nella cartella)")
    ap.add_argument("--aliquote-tab1", default=None, help="Percorso aliquote_tab1.csv (se omesso: ricerca automatica)")
    ap.add_argument("--rpm", default=None, help="Percorso RPM_*.xsi da usare (se omesso: usa l’ultimo trovato nella cartella)")
    ap.add_argument("--omaggi-pct", type=float, default=5.0, help="Percentuale omaggi ammessi rispetto alla capienza (default 5.0)")
    ap.add_argument("--soglia-omaggi", type=float, default=50.00, help="Soglia valore unitario LORDO (EUR) per IVAEccedenteOmaggi=0 (default 50.00). Valutata sulla quota Intrattenimento lorda unitaria (prezzo * Incidenza%, escludendo la prevendita)")
    args = ap.parse_args(argv)

    directory = os.path.abspath(args.directory)
    files = discover_files(directory)

    # Aliquote
    aliquote = None
    aliquote_path = args.aliquote_tab1
    if aliquote_path is None:
        if files["ALIQ"]:
            aliquote_path = files["ALIQ"][0]
    if aliquote_path is not None and os.path.exists(aliquote_path):
        aliquote = parse_aliquote_tab1_csv(aliquote_path)

    # Parse all sources
    log_recs: List[Dict[str, Any]] = []
    for p in files["LOG"]:
        log_recs.extend(parse_log(p))

    lta_recs: List[Dict[str, Any]] = []
    for p in files["LTA"]:
        lta_recs.extend(parse_lta(p))

    rca_recs: List[Dict[str, Any]] = []
    for p in files["RCA"]:
        rca_recs.extend(parse_rca(p))

    rpm_recs: List[Dict[str, Any]] = []

    rpm_paths: List[str] = []
    if args.rpm:
        rpm_paths = [args.rpm]
    else:
        # Se nella cartella ci sono più RPM (revisioni/prove), per default usiamo l’ultima (ordine alfabetico)
        rpm_paths = files["RPM"][-1:] if files["RPM"] else []

    for p in rpm_paths:
        if os.path.exists(p):
            rpm_recs.extend(parse_rpm(p))

    # Nota: se ci sono più RPM trovati ma ne usiamo solo uno, lo segnaliamo in output (poi verrà riportato anche in report)
    ignored_rpm = [os.path.basename(x) for x in files["RPM"] if x not in rpm_paths]

    summary, issues, metrics, details = run_checks(
        log_recs=log_recs,
        lta_recs=lta_recs,
        rca_recs=rca_recs,
        rpm_recs=rpm_recs,
        aliquote=aliquote,
        omaggi_pct=args.omaggi_pct,
        soglia_omaggi_eur=args.soglia_omaggi,
    )

    # Metriche: quali file RPM sono stati usati
    metrics["RPM_files_found"] = len(files["RPM"])
    metrics["RPM_files_used"] = ", ".join([os.path.basename(p) for p in rpm_paths]) if rpm_paths else "Nessuno"
    metrics["RPM_files_ignored"] = ", ".join(ignored_rpm) if ignored_rpm else ""

    html_report = build_html_report(summary, issues, metrics, details)

    out_path = args.out or os.path.join(directory, "report_verifica.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_report)

    # stampa breve riassunto su stdout
    print(f"Report scritto in: {out_path}")
    print(f"ERROR={summary['totals']['ERROR']} WARN={summary['totals']['WARN']} INFO={summary['totals']['INFO']}")
    return 0 if summary["totals"]["ERROR"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())


from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from lxml import etree

VALUTA_DEFAULT = "EUR"

def dt_now() -> datetime:
    return datetime.now().replace(microsecond=0)

def yyyymmdd_from_iso(date_iso: str) -> str:
    return date_iso.replace("-", "")

def iso_from_yyyymmdd(d: str) -> str:
    d = (d or "").strip()
    if len(d) != 8 or not d.isdigit():
        return ""
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"

def hhmm_from_iso_ts(ts: str) -> str:
    if "T" in ts:
        t = ts.split("T", 1)[1]
        return t[:5].replace(":", "")
    return ts[:5].replace(":", "")

def sanitize_id(s: str) -> str:
    import re
    s = (s or "").strip()
    s = re.sub(r"[^A-Za-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:80] or "EVT"

def money(x: Any) -> Decimal:
    d = Decimal(str(x))
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def eur_to_cents(eur: Any) -> int:
    d = money(eur)
    return int((d * Decimal("100")).to_integral_value(rounding=ROUND_HALF_UP))

def vat_iva_cents(lordo_cents: int, aliquota_percent: Decimal) -> int:
    if aliquota_percent <= 0:
        return 0
    lordo = Decimal(lordo_cents) / Decimal(100)
    imponibile = (lordo / (Decimal("1") + aliquota_percent/Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    iva = (lordo - imponibile).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return eur_to_cents(iva)

def sigillo16(seed: str) -> str:
    import hashlib
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16].upper()

def id_supporto20(seed: str) -> str:
    import hashlib
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    n = int(h[:20], 16)
    s = str(n)
    return (s + "0"*20)[:20]

# -----------------------
# Persistence
# -----------------------
def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

def default_config() -> Dict[str, Any]:
    return {
        "version": 7,
        "anagrafica": {
            "cf_organizzatore": "00000000000",
            "cf_titolare": "00000000000",
            "sistema_emissione": "P0000000",
            "codice_richiedente_emissione_sigillo": "CL000000",
            "denominazione_titolare": "",
            "denominazione_organizzatore": "",
            "tipo_organizzatore": "G",
        },
        "defaults": {
            "valuta": VALUTA_DEFAULT,
            "ivapreassolta_biglietto": "N",
            "ivapreassolta_abbonamenti": "B",
            "imponibile_intrattenimenti": "0",
        },
        "carte": [],
        "eventi": [],
        "abbonamenti_prodotti": [],
    }

@dataclass
class Paths:
    base_dir: Path
    data_dir: Path
    journal_dir: Path
    templates_dir: Path
    reference_dir: Path
    config_path: Path
    templ_log: Path
    templ_lta: Path
    templ_rca: Path
    templ_rpm: Path

def make_paths(base_dir: Path) -> Paths:
    data_dir = base_dir / "data"
    journal_dir = data_dir / "journal"
    templates_dir = base_dir / "templates"
    reference_dir = base_dir / "reference"
    return Paths(
        base_dir=base_dir,
        data_dir=data_dir,
        journal_dir=journal_dir,
        templates_dir=templates_dir,
        reference_dir=reference_dir,
        config_path=data_dir / "config.yml",
        templ_log=templates_dir / "LOG_template.xml",
        templ_lta=templates_dir / "LTA_template.xml",
        templ_rca=templates_dir / "RCA_template.xml",
        templ_rpm=templates_dir / "RPM_template.xml",
    )

def ensure_config(paths: Paths) -> Dict[str, Any]:
    cfg = load_yaml(paths.config_path)
    if not cfg:
        cfg = default_config()
        save_yaml(paths.config_path, cfg)
    # minimal migration
    base = default_config()
    cfg.setdefault("anagrafica", base["anagrafica"])
    cfg["anagrafica"].setdefault("denominazione_titolare", "")
    cfg["anagrafica"].setdefault("denominazione_organizzatore", "")
    cfg["anagrafica"].setdefault("tipo_organizzatore", "G")
    cfg.setdefault("defaults", base["defaults"])
    cfg.setdefault("carte", [])
    cfg.setdefault("eventi", [])
    cfg.setdefault("abbonamenti_prodotti", [])
    return cfg

def save_config(paths: Paths, cfg: Dict[str, Any]) -> None:
    save_yaml(paths.config_path, cfg)

def journal_path(paths: Paths, date_iso: str) -> Path:
    paths.journal_dir.mkdir(parents=True, exist_ok=True)
    return paths.journal_dir / f"{date_iso}.yml"

def ensure_day(paths: Paths, date_iso: str) -> Dict[str, Any]:
    p = journal_path(paths, date_iso)
    if not p.exists():
        save_yaml(p, {"data": date_iso, "titoli": [], "transazioni": []})
    return load_yaml(p)

def save_day(paths: Paths, date_iso: str, day: Dict[str, Any]) -> None:
    save_yaml(journal_path(paths, date_iso), day)

def reset_config(paths: Paths) -> Dict[str, Any]:
    cfg = default_config()
    save_yaml(paths.config_path, cfg)
    return cfg

def reset_section(cfg: Dict[str, Any], section: str) -> None:
    base = default_config()
    if section == "anagrafica":
        cfg["anagrafica"] = base["anagrafica"]
        cfg["defaults"] = base["defaults"]
    elif section in ("carte","eventi","abbonamenti_prodotti"):
        cfg[section] = []

def reset_day(paths: Paths, date_iso: str) -> Dict[str, Any]:
    day = {"data": date_iso, "titoli": [], "transazioni": []}
    save_yaml(journal_path(paths, date_iso), day)
    return day

# -----------------------
# Lookups / merge
# -----------------------
def make_event_id(codice_locale: str, data_evento: str, ora_evento: str, titolo: str) -> str:
    return sanitize_id(f"{codice_locale}_{data_evento}_{ora_evento}_{titolo}")

def find_card(cfg: Dict[str, Any], carta: str) -> Dict[str, Any]:
    for c in cfg.get("carte", []):
        if c.get("carta_attivazione") == carta:
            return c
    raise KeyError(f"Carta non trovata: {carta}")

def ensure_card(cfg: Dict[str, Any], carta: str, next_prog: int) -> None:
    if not carta:
        return
    for c in cfg.get("carte", []):
        if c.get("carta_attivazione") == carta:
            c["progressivo_next"] = max(int(c.get("progressivo_next", 1)), int(next_prog))
            return
    cfg.setdefault("carte", []).append({"carta_attivazione": carta, "progressivo_next": int(next_prog)})

def find_event(cfg: Dict[str, Any], event_id: str) -> Dict[str, Any]:
    for e in cfg.get("eventi", []):
        if e.get("id") == event_id:
            return e
    raise KeyError(f"Evento non trovato: {event_id}")

def find_event_by_key(cfg: Dict[str, Any], codice_locale: str, data_evento: str, ora_evento: str) -> Optional[Dict[str, Any]]:
    for e in cfg.get("eventi", []):
        if e.get("codice_locale")==codice_locale and e.get("data_evento")==data_evento and e.get("ora_evento")==ora_evento:
            return e
    return None

def ensure_sector(event: Dict[str, Any], codice_ordine: str) -> Dict[str, Any]:
    event.setdefault("settori", [])
    for s in event["settori"]:
        if str(s.get("codice_ordine")) == str(codice_ordine):
            s.setdefault("prezzi", {})
            return s
    sec = {"codice_ordine": str(codice_ordine), "capienza": 0, "prezzi": {}}
    event["settori"].append(sec)
    return sec

def merge_event(cfg: Dict[str, Any], ev: Dict[str, Any]) -> None:
    eid = ev["id"]
    for existing in cfg.get("eventi", []):
        if existing.get("id") == eid:
            existing.setdefault("settori", [])
            for s in (ev.get("settori") or []):
                ex_s = None
                for t in existing["settori"]:
                    if str(t.get("codice_ordine")) == str(s.get("codice_ordine")):
                        ex_s = t
                        break
                if ex_s is None:
                    s.setdefault("prezzi", {})
                    existing["settori"].append(s)
                else:
                    if "capienza" in s and int(s.get("capienza") or 0):
                        ex_s["capienza"] = int(s["capienza"])
                    ex_s.setdefault("prezzi", {})
                    if s.get("prezzi"):
                        ex_s["prezzi"].update(s["prezzi"])
            for k,v in ev.items():
                if k == "settori": 
                    continue
                if v not in (None,"") and existing.get(k) in (None,""):
                    existing[k] = v
            return
    cfg.setdefault("eventi", []).append(ev)

# -----------------------
# Capienza parsers
# -----------------------
def parse_capienza_from_rca(rca_xml: bytes) -> Dict[Tuple[str,str,str], Dict[str,int]]:
    root = etree.fromstring(rca_xml)
    out: Dict[Tuple[str,str,str], Dict[str,int]] = {}
    for ev in root.findall("Evento"):
        codice_locale = (ev.findtext("CodiceLocale") or "").strip()
        data_evento = (ev.findtext("DataEvento") or "").strip()
        ora_evento = (ev.findtext("OraEvento") or "").strip()
        key = (codice_locale, data_evento, ora_evento)
        for titoli in ev.findall("SistemaEmissione/Titoli"):
            cod_ord = (titoli.findtext("CodiceOrdinePosto") or "").strip()
            cap = int((titoli.findtext("Capienza") or "0").strip() or 0)
            if cod_ord:
                out.setdefault(key, {})[cod_ord] = cap
    return out

def parse_capienza_from_rpm(rpm_xml: bytes) -> Dict[Tuple[str,str,str], Dict[str,int]]:
    root = etree.fromstring(rpm_xml)
    out: Dict[Tuple[str,str,str], Dict[str,int]] = {}
    org = root.find("Organizzatore")
    if org is None:
        return out
    for ev in org.findall("Evento"):
        codice_locale = ""
        loc = ev.find("Locale")
        if loc is not None:
            codice_locale = (loc.findtext("CodiceLocale") or "").strip()
        data_evento = (ev.findtext("DataEvento") or "").strip()
        ora_evento = (ev.findtext("OraEvento") or "").strip()
        key = (codice_locale, data_evento, ora_evento)
        for odp in ev.findall("OrdineDiPosto"):
            cod_ord = (odp.findtext("CodiceOrdine") or "").strip()
            cap = int((odp.findtext("Capienza") or "0").strip() or 0)
            if cod_ord:
                out.setdefault(key, {})[cod_ord] = cap
    return out

def apply_capienza_to_cfg(cfg: Dict[str, Any], cap_map: Dict[Tuple[str,str,str], Dict[str,int]]) -> int:
    updated = 0
    for (codice_locale, data_evento, ora_evento), sectors in cap_map.items():
        ev = find_event_by_key(cfg, codice_locale, data_evento, ora_evento)
        if ev is None:
            eid = make_event_id(codice_locale, data_evento, ora_evento, "")
            ev = {
                "id": eid,
                "codice_locale": codice_locale,
                "titolo_evento": "",
                "tipo_genere": "",
                "data_evento": data_evento,
                "ora_evento": ora_evento,
                "data_apertura": data_evento,
                "ora_apertura": ora_evento,
                "tipo_tassazione": "S",
                "iva_percent": 0,
                "isi_percent": 0,
                "settori": [],
            }
            cfg.setdefault("eventi", []).append(ev)

        for cod_ord, cap in sectors.items():
            sec = ensure_sector(ev, cod_ord)
            if int(sec.get("capienza",0) or 0) != int(cap):
                sec["capienza"] = int(cap)
                updated += 1
    return updated



# -----------------------
# Import LOG / LTA (popola dataset)
# -----------------------
# -----------------------
# Import LOG / LTA (popola dataset)
# -----------------------
def import_log(cfg: Dict[str, Any], log_xml: bytes, target_date_iso: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    root = etree.fromstring(log_xml)
    trans = root.findall("Transazione")

    if target_date_iso is None:
        dates = [tr.attrib.get("DataEmissione", "") for tr in trans if tr.attrib.get("DataEmissione")]
        if dates:
            from collections import Counter
            most = Counter(dates).most_common(1)[0][0]
            target_date_iso = iso_from_yyyymmdd(most) or dt_now().date().isoformat()
        else:
            target_date_iso = dt_now().date().isoformat()

    day = {"data": target_date_iso, "titoli": [], "transazioni": []}

    if trans:
        t0 = trans[0].attrib
        cfg["anagrafica"]["cf_organizzatore"] = t0.get("CFOrganizzatore", cfg["anagrafica"]["cf_organizzatore"])
        cfg["anagrafica"]["cf_titolare"] = t0.get("CFTitolare", cfg["anagrafica"]["cf_titolare"])
        cfg["anagrafica"]["sistema_emissione"] = t0.get("SistemaEmissione", cfg["anagrafica"]["sistema_emissione"])
        cfg["anagrafica"]["codice_richiedente_emissione_sigillo"] = t0.get(
            "CodiceRichiedenteEmissioneSigillo", cfg["anagrafica"]["codice_richiedente_emissione_sigillo"]
        )
        cfg["defaults"]["valuta"] = t0.get("Valuta", cfg["defaults"]["valuta"])

    title_by_key: Dict[str, Dict[str, Any]] = {}

    for tr in trans:
        ta = tr.find("TitoloAccesso")
        ba = tr.find("BigliettoAbbonamento")
        ab = tr.find("Abbonamento")

        if ta is not None:
            kind = "annullamento_ticket" if ("OriginaleAnnullato" in tr.attrib or ta.attrib.get("Annullamento") == "S") else "ticket"
        elif ba is not None:
            kind = "biglietto_abbonamento"
        elif ab is not None:
            kind = "abbonamento"
        else:
            continue

        carta = tr.attrib.get("CartaAttivazione", "")
        prog = int(tr.attrib.get("NumeroProgressivo", "0") or 0)
        sig = tr.attrib.get("SigilloFiscale", "")
        ensure_card(cfg, carta, prog + 1)

        tipo_titolo = tr.attrib.get("TipoTitolo", "")
        cod_ord = tr.attrib.get("CodiceOrdine", "")
        data_em = tr.attrib.get("DataEmissione", "") or yyyymmdd_from_iso(target_date_iso)
        ora_em = tr.attrib.get("OraEmissione", "0000")
        tipo_tass = tr.attrib.get("TipoTassazione", "S")
        causale = tr.attrib.get("Causale", "")

        if ta is not None:
            codice_locale = (ta.findtext("CodiceLocale") or "").strip()
            data_evento = (ta.findtext("DataEvento") or "").strip()
            ora_evento = (ta.findtext("OraEvento") or "").strip()
            tipo_genere = (ta.findtext("TipoGenere") or "").strip()
            titolo_evento = (ta.findtext("Titolo") or "").strip()

            corr = int((ta.findtext("CorrispettivoLordo") or "0").strip() or 0)
            prev = int((ta.findtext("Prevendita") or "0").strip() or 0)
            ivac = int((ta.findtext("IVACorrispettivo") or "0").strip() or 0)
            ivap = int((ta.findtext("IVAPrevendita") or "0").strip() or 0)

            evento_id = make_event_id(codice_locale, data_evento, ora_evento, titolo_evento)
            merge_event(
                cfg,
                {
                    "id": evento_id,
                    "codice_locale": codice_locale,
                    "titolo_evento": titolo_evento,
                    "tipo_genere": tipo_genere,
                    "data_evento": data_evento,
                    "ora_evento": ora_evento,
                    "data_apertura": data_evento,
                    "ora_apertura": ora_evento,
                    "tipo_tassazione": tipo_tass,
                    "iva_percent": 0,
                    "settori": [{"codice_ordine": cod_ord, "capienza": 0, "prezzi": {}}],
                },
            )

            tx = {
                "kind": kind,
                "evento_id": evento_id,
                "carta_attivazione": carta,
                "numero_progressivo": prog,
                "sigillo_fiscale": sig,
                "data_emissione": data_em,
                "ora_emissione": ora_em,
                "tipo_titolo": tipo_titolo,
                "codice_ordine": cod_ord,
                "causale": causale,
                "tipo_tassazione": tipo_tass,
                "codice_locale": codice_locale,
                "data_evento": data_evento,
                "ora_evento": ora_evento,
                "tipo_genere": tipo_genere,
                "titolo_evento": titolo_evento,
                "corrispettivo_lordo_cents": corr,
                "prevendita_cents": prev,
                "iva_corrispettivo_cents": ivac,
                "iva_prevendita_cents": ivap,
            }
            if kind == "annullamento_ticket":
                tx["originale_numero_progressivo"] = int(tr.attrib.get("OriginaleAnnullato", "0") or 0)
                tx["carta_originale"] = tr.attrib.get("CartaOriginaleAnnullato", "")
                tx["causale_annullamento"] = tr.attrib.get("CausaleAnnullamento", "001")
            day["transazioni"].append(tx)

            if kind == "ticket":
                key = f"{carta}:{prog}"
                title = {
                    "key": key,
                    "evento_id": evento_id,
                    "carta_attivazione": carta,
                    "numero_progressivo": prog,
                    "sigillo_fiscale": sig,
                    "data_emissione": data_em,
                    "ora_emissione": ora_em,
                    "ora_lta": ora_em,
                    "tipo_titolo": tipo_titolo,
                    "codice_ordine": cod_ord,
                    "corrispettivo_lordo_cents": corr,
                    "prevendita_cents": prev,
                    "cod_supporto": "BT",
                    "id_supporto": id_supporto20(key),
                    "abbonamento": False,
                    "annullato": False,
                    "stato": "VT",
                }
                day["titoli"].append(title)
                title_by_key[key] = title
            else:
                okey = f"{tx.get('carta_originale','')}:{tx.get('originale_numero_progressivo',0)}"
                if okey in title_by_key:
                    title_by_key[okey]["annullato"] = True
                    title_by_key[okey]["stato"] = "AT"

        # (BA/AB: import minimo; wizard crea record completi)
        elif ba is not None:
            day["transazioni"].append({"kind": "biglietto_abbonamento"})
        elif ab is not None:
            day["transazioni"].append({"kind": "abbonamento"})

    return cfg, day

def import_lta(cfg: Dict[str, Any], lta_xml: bytes, target_date_iso: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    root = etree.fromstring(lta_xml)

    if target_date_iso is None:
        target_date_iso = iso_from_yyyymmdd(root.attrib.get("DataLTA", "")) or dt_now().date().isoformat()

    cfg["anagrafica"]["sistema_emissione"] = root.attrib.get("SistemaCA", cfg["anagrafica"]["sistema_emissione"])
    cfg["anagrafica"]["cf_titolare"] = root.attrib.get("CFTitolareCA", cfg["anagrafica"]["cf_titolare"])

    day = {"data": target_date_iso, "titoli": [], "transazioni": []}

    for evt in root.findall("LTA_Evento"):
        codice_locale = evt.attrib.get("CodiceLocale","")
        data_evento = evt.attrib.get("DataEvento","")
        ora_evento = evt.attrib.get("OraEvento","")
        titolo_evento = evt.attrib.get("Titolo","")
        tipo_genere = evt.attrib.get("TipoGenere","")

        evento_id = make_event_id(codice_locale, data_evento, ora_evento, titolo_evento)
        merge_event(cfg, {
            "id": evento_id,
            "codice_locale": codice_locale,
            "titolo_evento": titolo_evento,
            "tipo_genere": tipo_genere,
            "data_evento": data_evento,
            "ora_evento": ora_evento,
            "data_apertura": evt.attrib.get("DataApertura", data_evento),
            "ora_apertura": evt.attrib.get("OraApertura", ora_evento),
            "tipo_tassazione": "S",
            "iva_percent": 0,
            "settori": [],
        })

        for ta in evt.findall("TitoloAccesso"):
            carta = ta.attrib.get("CartaAttivazione","")
            prog = int(ta.attrib.get("ProgressivoFiscale","0") or 0)
            sig = ta.attrib.get("SigilloFiscale","")
            ensure_card(cfg, carta, prog+1)

            cod_ord = ta.attrib.get("CodiceOrdine","")
            ensure_sector(find_event(cfg, evento_id), cod_ord)

            key = f"{carta}:{prog}"
            title = {
                "key": key,
                "evento_id": evento_id,
                "carta_attivazione": carta,
                "numero_progressivo": prog,
                "sigillo_fiscale": sig,
                "data_emissione": ta.attrib.get("DataEmissione", yyyymmdd_from_iso(target_date_iso)),
                "ora_emissione": ta.attrib.get("OraEmissione","0000"),
                "ora_lta": ta.attrib.get("OraLTA", ta.attrib.get("OraEmissione","0000")),
                "tipo_titolo": ta.attrib.get("TipoTitolo",""),
                "codice_ordine": cod_ord,
                "corrispettivo_lordo_cents": int(ta.attrib.get("CorrispettivoLordo","0") or 0),
                "prevendita_cents": 0,
                "cod_supporto": ta.attrib.get("CodSupporto","BT"),
                "id_supporto": ta.attrib.get("IdSupporto", id_supporto20(key)),
                "abbonamento": ta.attrib.get("Abbonamento","N") == "S",
                "annullato": ta.attrib.get("Annullamento","N") == "S",
                "stato": ta.attrib.get("Stato","VT"),
            }
            # optional passthrough attributes
            for k in ["CFAbbonamento","CodiceAbbonamento","ProgressivoAbbonamento","QEventiAbilitati",
                      "DataIngresso","OraIngresso","DataANN","OraANN","CartaAttivazioneANN","ProgressivoFiscaleANN","SigilloFiscaleANN"]:
                if k in ta.attrib:
                    title[k] = ta.attrib.get(k)
            day["titoli"].append(title)

    return cfg, day

# -----------------------
# Wizard actions
# -----------------------
def add_or_update_price(cfg: Dict[str, Any], event_id: str, codice_ordine: str, price_key: str, price: Dict[str, Any]) -> None:
    ev = find_event(cfg, event_id)
    sec = ensure_sector(ev, codice_ordine)
    sec.setdefault("prezzi", {})
    sec["prezzi"][price_key] = price

def add_or_update_abbonamento(cfg: Dict[str, Any], item: Dict[str, Any]) -> None:
    code = item.get("codice_abbonamento")
    if not code:
        raise ValueError("codice_abbonamento richiesto")
    for a in cfg.get("abbonamenti_prodotti", []):
        if a.get("codice_abbonamento") == code:
            a.update(item)
            return
    cfg.setdefault("abbonamenti_prodotti", []).append(item)

def issue_ticket(cfg: Dict[str, Any], day: Dict[str, Any], date_iso: str,
                event_id: str, codice_ordine: str, price_key: str,
                carta: str, quantita: int, cod_supporto: str, ora_em: str) -> None:
    ev = find_event(cfg, event_id)
    sec = ensure_sector(ev, codice_ordine)
    prezzi = sec.get("prezzi", {}) or {}
    if price_key not in prezzi:
        raise KeyError("Prezzo non trovato nel settore.")
    pz = prezzi[price_key]
    card = find_card(cfg, carta)

    iva_pct = Decimal(str(pz.get("iva_percent", ev.get("iva_percent", 0)) or 0))
    corr_lordo_c = eur_to_cents(pz.get("corrispettivo_eur", "0.00"))
    prev_c = eur_to_cents(pz.get("prevendita_eur", "0.00"))
    iva_corr_c = vat_iva_cents(corr_lordo_c, iva_pct)
    iva_prev_c = vat_iva_cents(prev_c, iva_pct)

    data_em = yyyymmdd_from_iso(date_iso)

    for _ in range(int(quantita)):
        prog = int(card.get("progressivo_next", 1))
        key = f"{carta}:{prog}"
        sig = sigillo16(f"{key}|{event_id}|{data_em}|T")

        day.setdefault("titoli", []).append({
            "key": key,
            "evento_id": event_id,
            "carta_attivazione": carta,
            "numero_progressivo": prog,
            "sigillo_fiscale": sig,
            "data_emissione": data_em,
            "ora_emissione": ora_em,
            "ora_lta": ora_em,
            "tipo_titolo": str(pz.get("tipo_titolo", "")),
            "codice_ordine": str(codice_ordine),
            "corrispettivo_lordo_cents": corr_lordo_c,
            "prevendita_cents": prev_c,
            "cod_supporto": cod_supporto,
            "id_supporto": id_supporto20(key),
            "abbonamento": False,
            "annullato": False,
            "stato": "VT" if cod_supporto == "BT" else "VD",
        })

        day.setdefault("transazioni", []).append({
            "kind": "ticket",
            "evento_id": event_id,
            "carta_attivazione": carta,
            "numero_progressivo": prog,
            "sigillo_fiscale": sig,
            "data_emissione": data_em,
            "ora_emissione": ora_em,
            "tipo_titolo": str(pz.get("tipo_titolo", "")),
            "codice_ordine": str(codice_ordine),
            "causale": str(pz.get("causale","") or ""),
            "tipo_tassazione": ev.get("tipo_tassazione","S"),
            "codice_locale": ev.get("codice_locale",""),
            "data_evento": ev.get("data_evento",""),
            "ora_evento": ev.get("ora_evento",""),
            "tipo_genere": ev.get("tipo_genere",""),
            "titolo_evento": ev.get("titolo_evento",""),
            "corrispettivo_lordo_cents": corr_lordo_c,
            "prevendita_cents": prev_c,
            "iva_corrispettivo_cents": iva_corr_c,
            "iva_prevendita_cents": iva_prev_c,
        })

        card["progressivo_next"] = prog + 1

def sell_abbonamento(cfg: Dict[str, Any], day: Dict[str, Any], date_iso: str,
                   codice_abbonamento: str, turno: str,
                   carta: str, quantita: int, ora_em: str) -> None:
    """
    Vende/Emette Abbonamenti (LOG transazioni Abbonamento).
    Il ProgressivoAbbonamento viene incrementato (prod.progressivo_next).
    """
    prod = None
    for a in cfg.get("abbonamenti_prodotti", []):
        if a.get("codice_abbonamento") == codice_abbonamento and str(a.get("turno","")).upper() == str(turno).upper():
            prod = a
            break
    if prod is None:
        raise KeyError("Prodotto abbonamento non trovato per codice+turno selezionati.")
    card = find_card(cfg, carta)

    iva_pct = Decimal(str(prod.get("iva_percent", 0) or 0))
    corr_c = eur_to_cents(prod.get("corrispettivo_eur","0.00"))
    prev_c = eur_to_cents(prod.get("prevendita_eur","0.00"))
    iva_corr = vat_iva_cents(corr_c, iva_pct)
    iva_prev = vat_iva_cents(prev_c, iva_pct)

    qev = int(prod.get("q_eventi_abilitati", 1) or 1)
    total = corr_c + prev_c
    rateo = int(Decimal(total) / Decimal(max(qev,1)))
    rateo_iva = vat_iva_cents(rateo, iva_pct)

    data_em = yyyymmdd_from_iso(date_iso)

    for _ in range(int(quantita)):
        prog_tx = int(card.get("progressivo_next", 1))
        prog_ab = int(prod.get("progressivo_next", 1))
        sig = sigillo16(f"{carta}:{prog_tx}|AB|{codice_abbonamento}|{prog_ab}")

        day.setdefault("transazioni", []).append({
            "kind": "abbonamento",
            "carta_attivazione": carta,
            "numero_progressivo": prog_tx,
            "sigillo_fiscale": sig,
            "data_emissione": data_em,
            "ora_emissione": ora_em,
            "tipo_titolo": str(prod.get("tipo_titolo","")),
            "codice_ordine": str(prod.get("codice_ordine","")),
            "causale": "",
            "tipo_tassazione": str(prod.get("tipo_tassazione","S")),
            "codice_abbonamento": codice_abbonamento,
            "progressivo_abbonamento": prog_ab,
            "turno": str(turno).upper(),
            "q_eventi_abilitati": qev,
            "validita": str(prod.get("validita","")),
            "rateo_cents": rateo,
            "rateo_intrattenimenti_cents": 0,
            "rateo_iva_cents": rateo_iva,
            "corrispettivo_lordo_cents": corr_c,
            "prevendita_cents": prev_c,
            "iva_corrispettivo_cents": iva_corr,
            "iva_prevendita_cents": iva_prev,
        })

        card["progressivo_next"] = prog_tx + 1
        prod["progressivo_next"] = prog_ab + 1

def issue_biglietto_abbonamento(cfg: Dict[str, Any], day: Dict[str, Any], date_iso: str,
                               event_id: str, codice_ordine: str, tipo_titolo: str,
                               carta: str, quantita: int, cod_supporto: str, ora_em: str,
                               codice_abbonamento: str, cf_abbonamento: str,
                               progressivo_abbonamento: Optional[int] = None) -> None:
    """
    Emette BigliettoAbbonamento (LOG) + TitoloAccesso Abbonamento=S (LTA dataset).
    Se progressivo_abbonamento è fornito, NON modifica progressivo_next del prodotto abbonamento.
    """
    ev = find_event(cfg, event_id)
    card = find_card(cfg, carta)

    prod = None
    for a in cfg.get("abbonamenti_prodotti", []):
        if a.get("codice_abbonamento") == codice_abbonamento:
            prod = a
            break

    # Vincolo: solo turno libero (L)
    if prod is not None and str(prod.get("turno","")).upper() not in ("L",""):
        raise ValueError("Biglietto abbonamento consentito solo per abbonamenti a TURNO LIBERO (L).")

    iva_pct = Decimal(str((prod or {}).get("iva_percent", 0) or 0))
    qev = int((prod or {}).get("q_eventi_abilitati", 1) or 1)
    total = eur_to_cents((prod or {}).get("corrispettivo_eur","0.00")) + eur_to_cents((prod or {}).get("prevendita_eur","0.00"))
    importo_fig = int(Decimal(total) / Decimal(max(qev,1))) if prod else 0
    iva_fig = vat_iva_cents(importo_fig, iva_pct) if prod else 0

    data_em = yyyymmdd_from_iso(date_iso)

    for _ in range(int(quantita)):
        prog = int(card.get("progressivo_next", 1))
        key = f"{carta}:{prog}"
        sig = sigillo16(f"{key}|{event_id}|{data_em}|BA")

        if progressivo_abbonamento is not None:
            progabb = int(progressivo_abbonamento)
        else:
            progabb = int((prod or {}).get("progressivo_next", 1) or 1)
            if prod:
                prod["progressivo_next"] = progabb + 1

        # TitoloAccesso in LTA dataset (Abbonamento=S)
        day.setdefault("titoli", []).append({
            "key": key,
            "evento_id": event_id,
            "carta_attivazione": carta,
            "numero_progressivo": prog,
            "sigillo_fiscale": sig,
            "data_emissione": data_em,
            "ora_emissione": ora_em,
            "ora_lta": ora_em,
            "tipo_titolo": tipo_titolo,
            "codice_ordine": codice_ordine,
            "corrispettivo_lordo_cents": 0,
            "prevendita_cents": 0,
            "cod_supporto": cod_supporto,
            "id_supporto": id_supporto20(key),
            "abbonamento": True,
            "CFAbbonamento": cf_abbonamento,
            "CodiceAbbonamento": codice_abbonamento,
            "ProgressivoAbbonamento": progabb,
            "QEventiAbilitati": qev,
            "annullato": False,
            "stato": "VT" if cod_supporto == "BT" else "VD",
        })

        # LOG transazione BigliettoAbbonamento
        day.setdefault("transazioni", []).append({
            "kind": "biglietto_abbonamento",
            "evento_id": event_id,
            "carta_attivazione": carta,
            "numero_progressivo": prog,
            "sigillo_fiscale": sig,
            "data_emissione": data_em,
            "ora_emissione": ora_em,
            "tipo_titolo": tipo_titolo,
            "codice_ordine": codice_ordine,
            "causale": "",
            "tipo_tassazione": ev.get("tipo_tassazione","S"),
            "codice_locale": ev.get("codice_locale",""),
            "data_evento": ev.get("data_evento",""),
            "ora_evento": ev.get("ora_evento",""),
            "tipo_genere": ev.get("tipo_genere",""),
            "titolo_evento": ev.get("titolo_evento",""),
            "codice_abbonamento": codice_abbonamento,
            "progressivo_abbonamento": progabb,
            "cf_abbonamento": cf_abbonamento,
            "importo_figurativo_cents": importo_fig,
            "iva_figurativa_cents": iva_fig,
        })

        card["progressivo_next"] = prog + 1

def cancel_ticket(cfg: Dict[str, Any], day: Dict[str, Any], date_iso: str, titolo_key: str, causale_annullamento: str, carta_ann: str) -> None:
    # find title
    t = None
    for x in day.get("titoli", []):
        if x.get("key") == titolo_key:
            t = x; break
    if t is None:
        raise KeyError("Titolo non trovato nel giorno.")
    ev = find_event(cfg, t["evento_id"])
    card = find_card(cfg, carta_ann)
    prog = int(card.get("progressivo_next",1))
    sig = sigillo16(f"{carta_ann}:{prog}|ANN|{titolo_key}")
    data_em = yyyymmdd_from_iso(date_iso)
    ora_em = hhmm_from_iso_ts(dt_now().isoformat())

    # get original ticket tx for iva if present
    orig = None
    for tx in day.get("transazioni", []):
        if tx.get("kind")=="ticket" and tx.get("carta_attivazione")==t.get("carta_attivazione") and int(tx.get("numero_progressivo",0))==int(t.get("numero_progressivo",0)):
            orig = tx; break

    day.setdefault("transazioni", []).append({
        "kind": "annullamento_ticket",
        "evento_id": t["evento_id"],
        "carta_attivazione": carta_ann,
        "numero_progressivo": prog,
        "sigillo_fiscale": sig,
        "data_emissione": data_em,
        "ora_emissione": ora_em,
        "tipo_titolo": t.get("tipo_titolo",""),
        "codice_ordine": t.get("codice_ordine",""),
        "causale": "",
        "tipo_tassazione": ev.get("tipo_tassazione","S"),
        "codice_locale": ev.get("codice_locale",""),
        "data_evento": ev.get("data_evento",""),
        "ora_evento": ev.get("ora_evento",""),
        "tipo_genere": ev.get("tipo_genere",""),
        "titolo_evento": ev.get("titolo_evento",""),
        "corrispettivo_lordo_cents": int((orig or {}).get("corrispettivo_lordo_cents", t.get("corrispettivo_lordo_cents",0))),
        "prevendita_cents": int((orig or {}).get("prevendita_cents", t.get("prevendita_cents",0))),
        "iva_corrispettivo_cents": int((orig or {}).get("iva_corrispettivo_cents", 0)),
        "iva_prevendita_cents": int((orig or {}).get("iva_prevendita_cents", 0)),
        "originale_numero_progressivo": int(t.get("numero_progressivo",0)),
        "carta_originale": str(t.get("carta_attivazione","")),
        "causale_annullamento": str(causale_annullamento).zfill(3),
    })
    card["progressivo_next"] = prog + 1

    # mark title
    t["annullato"] = True
    t["stato"] = "AT" if t.get("cod_supporto","BT")=="BT" else "AD"
    t["DataANN"] = data_em
    t["OraANN"] = ora_em
    t["CartaAttivazioneANN"] = carta_ann
    t["ProgressivoFiscaleANN"] = str(prog)
    t["SigilloFiscaleANN"] = sig

def record_access(day: Dict[str, Any], titolo_key: str, timestamp_iso: str, mode: str) -> None:
    t = None
    for x in day.get("titoli", []):
        if x.get("key") == titolo_key:
            t = x; break
    if t is None:
        raise KeyError("Titolo non trovato.")
    support = t.get("cod_supporto","BT")
    t["stato"] = ("MT" if support=="BT" else "MD") if mode=="MAN" else ("ZT" if support=="BT" else "ZD")
    t["DataIngresso"] = yyyymmdd_from_iso(timestamp_iso[:10])
    t["OraIngresso"] = hhmm_from_iso_ts(timestamp_iso)

def set_block_status(day: Dict[str, Any], titolo_key: str, kind: str) -> None:
    t = None
    for x in day.get("titoli", []):
        if x.get("key") == titolo_key:
            t = x; break
    if t is None:
        raise KeyError("Titolo non trovato.")
    support = t.get("cod_supporto","BT")
    if kind == "DASPO":
        t["stato"] = "DT" if support=="BT" else "DD"
    elif kind == "RUBATO":
        t["stato"] = "FT" if support=="BT" else "FD"
    else:
        t["stato"] = "BT" if support=="BT" else "BD"

# -----------------------
# Exporters (LOG/LTA) - require prototypes in template
# -----------------------
def set_text(el: etree._Element, xpath: str, text: str) -> None:
    n = el.find(xpath)
    if n is None:
        parts = xpath.split("/")
        cur = el
        for p in parts:
            if not p: continue
            nxt = cur.find(p)
            if nxt is None:
                nxt = etree.SubElement(cur, p)
            cur = nxt
        n = cur
    n.text = text

def set_attrib_ordered(el: etree._Element, attrib: Dict[str, str], order: List[str]) -> None:
    for k in list(el.attrib.keys()):
        del el.attrib[k]
    for k in order:
        if k in attrib:
            el.set(k, attrib[k])
    for k,v in attrib.items():
        if k not in order:
            el.set(k,v)

@dataclass
class LogTemplates:
    base_ticket: etree._Element
    base_ann: etree._Element
    base_ba: etree._Element
    base_ab: etree._Element
    attr_order: List[str]
    ann_order: List[str]

def load_log_templates(paths: Paths) -> LogTemplates:
    root = etree.parse(str(paths.templ_log)).getroot()
    base_ticket = base_ann = base_ba = base_ab = None
    for tr in root.findall("Transazione"):
        if base_ticket is None and tr.find("TitoloAccesso") is not None and "OriginaleAnnullato" not in tr.attrib:
            base_ticket = tr
        if base_ann is None and "OriginaleAnnullato" in tr.attrib:
            base_ann = tr
        if base_ba is None and tr.find("BigliettoAbbonamento") is not None:
            base_ba = tr
        if base_ab is None and tr.find("Abbonamento") is not None:
            base_ab = tr
    if not all([base_ticket, base_ann, base_ba, base_ab]):
        raise ValueError("LOG_template.xml deve contenere esempi per ticket + annullamento + BigliettoAbbonamento + Abbonamento.")
    return LogTemplates(deepcopy(base_ticket), deepcopy(base_ann), deepcopy(base_ba), deepcopy(base_ab),
                        list(base_ticket.attrib.keys()), list(base_ann.attrib.keys()))

def build_common(cfg: Dict[str, Any], tx: Dict[str, Any], ivap: str) -> Dict[str,str]:
    return {
        "CFOrganizzatore": cfg["anagrafica"]["cf_organizzatore"],
        "CFTitolare": cfg["anagrafica"]["cf_titolare"],
        "IVAPreassolta": ivap,
        "TipoTassazione": tx.get("tipo_tassazione","S"),
        "Valuta": cfg["defaults"].get("valuta", VALUTA_DEFAULT),
        "SistemaEmissione": cfg["anagrafica"]["sistema_emissione"],
        "CartaAttivazione": tx.get("carta_attivazione",""),
        "SigilloFiscale": tx.get("sigillo_fiscale",""),
        "DataEmissione": tx.get("data_emissione",""),
        "OraEmissione": tx.get("ora_emissione",""),
        "NumeroProgressivo": str(tx.get("numero_progressivo","")),
        "TipoTitolo": tx.get("tipo_titolo",""),
        "CodiceOrdine": tx.get("codice_ordine",""),
        "Causale": tx.get("causale",""),
        "CodiceRichiedenteEmissioneSigillo": cfg["anagrafica"]["codice_richiedente_emissione_sigillo"],
        "ImponibileIntrattenimenti": cfg["defaults"].get("imponibile_intrattenimenti","0"),
    }

def export_log(paths: Paths, cfg: Dict[str, Any], day: Dict[str, Any]) -> bytes:
    doc = etree.parse(str(paths.templ_log))
    root = doc.getroot()
    for tr in list(root.findall("Transazione")):
        root.remove(tr)
    tpls = load_log_templates(paths)

    for tx in day.get("transazioni", []):
        kind = tx.get("kind")

        if kind == "ticket":
            tr = deepcopy(tpls.base_ticket)
            attrs = build_common(cfg, tx, cfg["defaults"].get("ivapreassolta_biglietto","N"))
            set_attrib_ordered(tr, attrs, tpls.attr_order)
            ta = tr.find("TitoloAccesso")
            ta.attrib["Annullamento"] = "N"
            set_text(ta, "CorrispettivoLordo", str(tx.get("corrispettivo_lordo_cents",0)))
            set_text(ta, "Prevendita", str(tx.get("prevendita_cents",0)))
            set_text(ta, "IVACorrispettivo", str(tx.get("iva_corrispettivo_cents",0)))
            set_text(ta, "IVAPrevendita", str(tx.get("iva_prevendita_cents",0)))
            for tag, key in [("CodiceLocale","codice_locale"),("DataEvento","data_evento"),("OraEvento","ora_evento"),("TipoGenere","tipo_genere"),("Titolo","titolo_evento")]:
                set_text(ta, tag, str(tx.get(key,"")))
            root.append(tr)

        elif kind == "annullamento_ticket":
            tr = deepcopy(tpls.base_ann)
            attrs = build_common(cfg, tx, cfg["defaults"].get("ivapreassolta_biglietto","N"))
            attrs["OriginaleAnnullato"] = str(tx.get("originale_numero_progressivo",0))
            attrs["CartaOriginaleAnnullato"] = tx.get("carta_originale","")
            attrs["CausaleAnnullamento"] = str(tx.get("causale_annullamento","001")).zfill(3)
            set_attrib_ordered(tr, attrs, tpls.ann_order)
            ta = tr.find("TitoloAccesso")
            ta.attrib["Annullamento"] = "S"
            set_text(ta, "CorrispettivoLordo", str(tx.get("corrispettivo_lordo_cents",0)))
            set_text(ta, "Prevendita", str(tx.get("prevendita_cents",0)))
            set_text(ta, "IVACorrispettivo", str(tx.get("iva_corrispettivo_cents",0)))
            set_text(ta, "IVAPrevendita", str(tx.get("iva_prevendita_cents",0)))
            for tag, key in [("CodiceLocale","codice_locale"),("DataEvento","data_evento"),("OraEvento","ora_evento"),("TipoGenere","tipo_genere"),("Titolo","titolo_evento")]:
                set_text(ta, tag, str(tx.get(key,"")))
            root.append(tr)

        elif kind == "biglietto_abbonamento":
            tr = deepcopy(tpls.base_ba)
            attrs = build_common(cfg, tx, cfg["defaults"].get("ivapreassolta_abbonamenti","B"))
            set_attrib_ordered(tr, attrs, tpls.attr_order)
            ba = tr.find("BigliettoAbbonamento")
            ba.attrib["Annullamento"] = "N"
            for tag, key in [
                ("CodiceLocale","codice_locale"),("DataEvento","data_evento"),("OraEvento","ora_evento"),
                ("TipoGenere","tipo_genere"),("Titolo","titolo_evento"),
                ("CodiceAbbonamento","codice_abbonamento"),
                ("ProgressivoAbbonamento","progressivo_abbonamento"),
                ("CodiceFiscale","cf_abbonamento"),
                ("ImportoFigurativo","importo_figurativo_cents"),
                ("IVAFigurativa","iva_figurativa_cents"),
            ]:
                set_text(ba, tag, str(tx.get(key,"")))
            root.append(tr)

        elif kind == "abbonamento":
            tr = deepcopy(tpls.base_ab)
            attrs = build_common(cfg, tx, cfg["defaults"].get("ivapreassolta_abbonamenti","B"))
            set_attrib_ordered(tr, attrs, tpls.attr_order)
            ab = tr.find("Abbonamento")
            ab.attrib["Annullamento"] = "N"
            set_text(ab, "CodiceAbbonamento", tx.get("codice_abbonamento",""))
            set_text(ab, "ProgressivoAbbonamento", str(tx.get("progressivo_abbonamento","")))
            turno = ab.find("Turno")
            if turno is None:
                turno = etree.SubElement(ab, "Turno")
            turno.attrib["valore"] = str(tx.get("turno","L"))
            for tag, key in [
                ("QuantitaEventiAbilitati","q_eventi_abilitati"),
                ("Validita","validita"),
                ("Rateo","rateo_cents"),
                ("RateoIntrattenimenti","rateo_intrattenimenti_cents"),
                ("RateoIVA","rateo_iva_cents"),
                ("CorrispettivoLordo","corrispettivo_lordo_cents"),
                ("Prevendita","prevendita_cents"),
                ("IVACorrispettivo","iva_corrispettivo_cents"),
                ("IVAPrevendita","iva_prevendita_cents"),
            ]:
                set_text(ab, tag, str(tx.get(key,0) if "iva" in key or "cents" in key else tx.get(key,"")))
            root.append(tr)

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def export_lta(paths: Paths, cfg: Dict[str, Any], day: Dict[str, Any]) -> bytes:
    doc = etree.parse(str(paths.templ_lta))
    root = doc.getroot()
    root.attrib["SistemaCA"] = cfg["anagrafica"]["sistema_emissione"]
    root.attrib["CFTitolareCA"] = cfg["anagrafica"]["cf_titolare"]
    root.attrib["DataLTA"] = yyyymmdd_from_iso(day["data"])

    for e in list(root.findall("LTA_Evento")):
        root.remove(e)

    base_evt = etree.parse(str(paths.templ_lta)).getroot().find("LTA_Evento")
    if base_evt is None:
        raise ValueError("LTA_template.xml deve contenere almeno 1 LTA_Evento di esempio.")
    base_ta = base_evt.find("TitoloAccesso")
    if base_ta is None:
        raise ValueError("LTA_template.xml deve contenere almeno 1 TitoloAccesso di esempio.")

    by_event: Dict[str, List[Dict[str, Any]]] = {}
    for t in day.get("titoli", []):
        by_event.setdefault(t.get("evento_id","EVT"), []).append(t)

    for event_id, titoli in by_event.items():
        ev = None
        try:
            ev = find_event(cfg, event_id)
        except Exception:
            ev = None

        evt = deepcopy(base_evt)
        for c in list(evt):
            if c.tag == "TitoloAccesso":
                evt.remove(c)

        evt.attrib["CFOrganizzatore"] = cfg["anagrafica"]["cf_organizzatore"]
        if ev:
            evt.attrib["CodiceLocale"] = ev.get("codice_locale","")
            evt.attrib["DataEvento"] = ev.get("data_evento","")
            evt.attrib["OraEvento"] = ev.get("ora_evento","")
            evt.attrib["Titolo"] = ev.get("titolo_evento","")
            evt.attrib["TipoGenere"] = ev.get("tipo_genere","")
            evt.attrib["DataApertura"] = ev.get("data_apertura", ev.get("data_evento",""))
            evt.attrib["OraApertura"] = ev.get("ora_apertura", ev.get("ora_evento",""))

        for t in titoli:
            ta = deepcopy(base_ta)
            for cc in list(ta):
                ta.remove(cc)

            ta.attrib["SistemaEmissione"] = cfg["anagrafica"]["sistema_emissione"]
            ta.attrib["CartaAttivazione"] = str(t.get("carta_attivazione",""))
            ta.attrib["ProgressivoFiscale"] = str(t.get("numero_progressivo",""))
            ta.attrib["SigilloFiscale"] = str(t.get("sigillo_fiscale",""))
            ta.attrib["DataEmissione"] = str(t.get("data_emissione", yyyymmdd_from_iso(day["data"])))
            ta.attrib["OraEmissione"] = str(t.get("ora_emissione","0000"))
            ta.attrib["DataLTA"] = yyyymmdd_from_iso(day["data"])
            ta.attrib["OraLTA"] = str(t.get("ora_lta", t.get("ora_emissione","0000")))
            ta.attrib["TipoTitolo"] = str(t.get("tipo_titolo",""))
            ta.attrib["CodiceOrdine"] = str(t.get("codice_ordine",""))
            ta.attrib["CorrispettivoLordo"] = str(t.get("corrispettivo_lordo_cents",0))
            ta.attrib["Abbonamento"] = "S" if t.get("abbonamento") else "N"
            ta.attrib["Annullamento"] = "S" if t.get("annullato") else "N"
            ta.attrib["CodSupporto"] = str(t.get("cod_supporto","BT"))
            ta.attrib["IdSupporto"] = str(t.get("id_supporto", id_supporto20(str(t.get("key","")))))
            ta.attrib["Stato"] = str(t.get("stato","VT"))

            # pass-through optional
            passthrough = ["CFAbbonamento","CodiceAbbonamento","ProgressivoAbbonamento","QEventiAbilitati",
                           "DataIngresso","OraIngresso","DataANN","OraANN","CartaAttivazioneANN","ProgressivoFiscaleANN","SigilloFiscaleANN"]
            for k in passthrough:
                if k in t and t[k] not in (None,""):
                    ta.attrib[k] = str(t[k])

            evt.append(ta)

        root.append(evt)

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")



# -----------------------
# RPM export (Riepilogo Mensile)
# -----------------------
def _read_doctype(xml_bytes: bytes) -> str:
    import re
    txt = xml_bytes.decode("utf-8", errors="ignore")
    m = re.search(r"<!DOCTYPE\s+[^>]+>", txt)
    return m.group(0) if m else ""

def _month_from_date_iso(date_iso: str) -> str:
    # YYYY-MM-DD -> YYYYMM
    return date_iso.replace("-", "")[:6]

def load_month_days(paths: Paths, month_yyyymm: str) -> List[Dict[str, Any]]:
    days: List[Dict[str, Any]] = []
    if not paths.journal_dir.exists():
        return days
    for p in sorted(paths.journal_dir.glob("*.yml")):
        stem = p.stem  # YYYY-MM-DD
        if len(stem) >= 7 and stem[0:4].isdigit():
            yyyymm = stem.replace("-", "")[:6]
            if yyyymm == month_yyyymm:
                try:
                    days.append(load_yaml(p))
                except Exception:
                    pass
    return days

def _get_event_meta(cfg: Dict[str, Any], event_id: str, fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    for e in cfg.get("eventi", []):
        if e.get("id") == event_id:
            return e
    return fallback or {}

def export_rpm(paths: Paths, cfg: Dict[str, Any], month_yyyymm: str,
              progressivo_generazione: int = 1, sostituzione: str = "S") -> bytes:
    """
    Genera RPM (RiepilogoMensile) per mese YYYYMM aggregando tutti i journal in data/journal.
    Richiede templates/RPM_template.xml.
    """
    import re
    if not paths.templ_rpm.exists():
        raise FileNotFoundError("RPM_template.xml mancante in templates/")

    tpl_bytes = paths.templ_rpm.read_bytes()
    doctype = _read_doctype(tpl_bytes)

    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.fromstring(tpl_bytes, parser=parser)
    root = doc  # already root element

    # Set root attrs
    root.attrib["Mese"] = str(month_yyyymm)
    root.attrib["DataGenerazione"] = yyyymmdd_from_iso(dt_now().date().isoformat())
    root.attrib["OraGenerazione"] = dt_now().strftime("%H%M%S")
    root.attrib["ProgressivoGenerazione"] = str(int(progressivo_generazione))
    root.attrib["Sostituzione"] = str(sostituzione)

    # Update anagrafica in XML
    tit = root.find("Titolare")
    org = root.find("Organizzatore")
    if tit is None or org is None:
        raise ValueError("RPM_template.xml non valido: mancano Titolare/Organizzatore")

    def _set_text(parent, tag, val):
        n = parent.find(tag)
        if n is None:
            n = etree.SubElement(parent, tag)
        n.text = str(val)

    _set_text(tit, "Denominazione", cfg["anagrafica"].get("denominazione_titolare","") or cfg["anagrafica"].get("cf_titolare",""))
    _set_text(tit, "CodiceFiscale", cfg["anagrafica"].get("cf_titolare",""))
    _set_text(tit, "SistemaEmissione", cfg["anagrafica"].get("sistema_emissione",""))

    _set_text(org, "Denominazione", cfg["anagrafica"].get("denominazione_organizzatore","") or cfg["anagrafica"].get("cf_organizzatore",""))
    _set_text(org, "CodiceFiscale", cfg["anagrafica"].get("cf_organizzatore",""))
    tipo_org = org.find("TipoOrganizzatore")
    if tipo_org is None:
        tipo_org = etree.SubElement(org, "TipoOrganizzatore")
    tipo_org.attrib["valore"] = str(cfg["anagrafica"].get("tipo_organizzatore","G"))

    # Prototipi (presi dal template) per mantenere struttura/ordine
    proto_event = org.find("Evento")
    proto_abbonamenti = org.find("Abbonamenti")
    proto_event = deepcopy(proto_event) if proto_event is not None else etree.Element("Evento")
    proto_abbonamenti = deepcopy(proto_abbonamenti) if proto_abbonamenti is not None else etree.Element("Abbonamenti")

    # Clear existing Evento and Abbonamenti under Organizzatore
    for ch in list(org):
        if ch.tag in ("Evento", "Abbonamenti"):
            org.remove(ch)

    # Load month data
    days = load_month_days(paths, month_yyyymm)

    # Aggregations
    # event_id -> order -> aggregates
    ev_aggr: Dict[str, Dict[str, Any]] = {}
    # subscription products
    ab_prod_aggr: Dict[Tuple[str,str,str,str,str,str,int], Dict[str,int]] = {}

    def ensure_ev(eid: str) -> Dict[str, Any]:
        if eid not in ev_aggr:
            meta = _get_event_meta(cfg, eid, {})
            ev_aggr[eid] = {
                "meta": meta,
                "orders": {},  # cod_ord -> dict
            }
        return ev_aggr[eid]

    def ensure_order(eid: str, cod_ord: str) -> Dict[str, Any]:
        evd = ensure_ev(eid)
        orders = evd["orders"]
        if cod_ord not in orders:
            # capienza from cfg
            cap = 0
            meta = evd["meta"] or {}
            for s in meta.get("settori", []) or []:
                if str(s.get("codice_ordine")) == str(cod_ord):
                    cap = int(s.get("capienza",0) or 0)
                    break
            orders[cod_ord] = {
                "capienza": cap,
                "iva_ecc_omaggi": 0,
                "titoli": {},       # tipo -> sums
                "annullati": {},    # tipo -> sums
                "biglietti_abbonamento": {},  # (cf,codabb,tipo) -> sums
                "abbonamenti_fissi": {},      # (cf,codabb,tipo) -> sums
            }
        return orders[cod_ord]

    def add_sum(bucket: Dict, key, qty: int, corr: int, prev: int, ivac: int, ivap: int):
        d = bucket.setdefault(key, {"qty":0, "corr":0, "prev":0, "ivac":0, "ivap":0})
        d["qty"] += qty
        d["corr"] += corr
        d["prev"] += prev
        d["ivac"] += ivac
        d["ivap"] += ivap

    # from transazioni
    for day in days:
        for tx in (day.get("transazioni") or []):
            kind = tx.get("kind")
            if kind == "ticket":
                eid = tx.get("evento_id","")
                cod_ord = str(tx.get("codice_ordine",""))
                tipo = str(tx.get("tipo_titolo",""))
                o = ensure_order(eid, cod_ord)
                add_sum(o["titoli"], tipo, 1,
                        int(tx.get("corrispettivo_lordo_cents",0) or 0),
                        int(tx.get("prevendita_cents",0) or 0),
                        int(tx.get("iva_corrispettivo_cents",0) or 0),
                        int(tx.get("iva_prevendita_cents",0) or 0))
                # IVA eccedenza omaggi (semplice): corrispettivo=0 ma IVA>0
                if int(tx.get("corrispettivo_lordo_cents",0) or 0) == 0 and int(tx.get("iva_corrispettivo_cents",0) or 0) > 0:
                    o["iva_ecc_omaggi"] += int(tx.get("iva_corrispettivo_cents",0) or 0)

            elif kind == "annullamento_ticket":
                eid = tx.get("evento_id","")
                cod_ord = str(tx.get("codice_ordine",""))
                tipo = str(tx.get("tipo_titolo",""))
                o = ensure_order(eid, cod_ord)
                add_sum(o["annullati"], tipo, 1,
                        int(tx.get("corrispettivo_lordo_cents",0) or 0),
                        int(tx.get("prevendita_cents",0) or 0),
                        int(tx.get("iva_corrispettivo_cents",0) or 0),
                        int(tx.get("iva_prevendita_cents",0) or 0))

            elif kind == "biglietto_abbonamento":
                eid = tx.get("evento_id","")
                cod_ord = str(tx.get("codice_ordine",""))
                cf = str(tx.get("cf_abbonamento","") or cfg["anagrafica"].get("cf_titolare",""))
                codabb = str(tx.get("codice_abbonamento",""))
                tipo = str(tx.get("tipo_titolo",""))
                key = (cf, codabb, tipo)
                o = ensure_order(eid, cod_ord)
                d = o["biglietti_abbonamento"].setdefault(key, {"qty":0,"imp":0,"iva":0})
                d["qty"] += 1
                d["imp"] += int(tx.get("importo_figurativo_cents",0) or 0)
                d["iva"] += int(tx.get("iva_figurativa_cents",0) or 0)

            elif kind == "abbonamento":
                # product sales aggregation
                code = str(tx.get("codice_abbonamento",""))
                turno = str(tx.get("turno","")).upper()
                validita = str(tx.get("validita",""))
                tipo_tass = str(tx.get("tipo_tassazione","S"))
                cod_ord = str(tx.get("codice_ordine",""))
                tipo_tit = str(tx.get("tipo_titolo",""))
                qev = int(tx.get("q_eventi_abilitati",0) or 0)
                k = (code, turno, validita, tipo_tass, cod_ord, tipo_tit, qev)
                d = ab_prod_aggr.setdefault(k, {"qty":0,"corr":0,"prev":0,"ivac":0,"ivap":0})
                d["qty"] += 1
                d["corr"] += int(tx.get("corrispettivo_lordo_cents",0) or 0)
                d["prev"] += int(tx.get("prevendita_cents",0) or 0)
                d["ivac"] += int(tx.get("iva_corrispettivo_cents",0) or 0)
                d["ivap"] += int(tx.get("iva_prevendita_cents",0) or 0)

    # infer AbbonamentiFissi from titles (if turno=F)
    # look up product map
    prod_map: Dict[str, Dict[str, Any]] = {str(a.get("codice_abbonamento")): a for a in cfg.get("abbonamenti_prodotti", []) if a.get("codice_abbonamento")}
    for day in days:
        for t in (day.get("titoli") or []):
            if not t.get("abbonamento"):
                continue
            codabb = str(t.get("CodiceAbbonamento","") or "")
            if not codabb:
                continue
            prod = prod_map.get(codabb)
            if not prod:
                continue
            if str(prod.get("turno","")).upper() != "F":
                continue
            eid = str(t.get("evento_id",""))
            cod_ord = str(t.get("codice_ordine",""))
            cf = str(t.get("CFAbbonamento","") or cfg["anagrafica"].get("cf_titolare",""))
            tipo = str(t.get("tipo_titolo",""))
            key = (cf, codabb, tipo)
            o = ensure_order(eid, cod_ord)
            d = o["abbonamenti_fissi"].setdefault(key, {"qty":0,"imp":0,"iva":0})
            d["qty"] += 1
            # compute rateo from product
            try:
                iva_pct = Decimal(str(prod.get("iva_percent",0) or 0))
            except Exception:
                iva_pct = Decimal("0")
            total = eur_to_cents(prod.get("corrispettivo_eur","0.00")) + eur_to_cents(prod.get("prevendita_eur","0.00"))
            qev = int(prod.get("q_eventi_abilitati",1) or 1)
            rateo = int(Decimal(total) / Decimal(max(qev,1)))
            d["imp"] += rateo
            d["iva"] += vat_iva_cents(rateo, iva_pct)

    # Build XML with prototypes (best effort)
    base_event = deepcopy(proto_event)
    base_ab = deepcopy(proto_abbonamenti)

    # helper create event node
    def build_event_node(meta: Dict[str, Any], orders: Dict[str, Any]) -> etree._Element:
        evn = deepcopy(base_event)
        # remove existing OrdineDiPosto from prototype
        for ch in list(evn):
            if ch.tag == "OrdineDiPosto":
                evn.remove(ch)

        # Intrattenimento
        intr = evn.find("Intrattenimento")
        if intr is None:
            intr = etree.SubElement(evn, "Intrattenimento")
        tipo_t = intr.find("TipoTassazione")
        if tipo_t is None:
            tipo_t = etree.SubElement(intr, "TipoTassazione")
        tipo_t.attrib["valore"] = str(meta.get("tipo_tassazione","S"))
        inc = intr.find("Incidenza")
        if inc is None:
            inc = etree.SubElement(intr, "Incidenza")
        inc.text = str(int(meta.get("intrattenimento_incidenza", 0) or 0))

        # Locale
        loc = evn.find("Locale")
        if loc is None:
            loc = etree.SubElement(evn, "Locale")
        dn = loc.find("Denominazione")
        if dn is None:
            dn = etree.SubElement(loc, "Denominazione")
        if not (dn.text and dn.text.strip()):
            dn.text = str(meta.get("denominazione_locale","") or "")
        cl = loc.find("CodiceLocale")
        if cl is None:
            cl = etree.SubElement(loc, "CodiceLocale")
        cl.text = str(meta.get("codice_locale",""))

        # Data/Ora
        _set_text(evn, "DataEvento", str(meta.get("data_evento","")))
        _set_text(evn, "OraEvento", str(meta.get("ora_evento","")))

        # MultiGenere
        mg = evn.find("MultiGenere")
        if mg is None:
            mg = etree.SubElement(evn, "MultiGenere")
        _set_text(mg, "TipoGenere", str(meta.get("tipo_genere","")))
        _set_text(mg, "IncidenzaGenere", str(int(meta.get("incidenza_genere", 100) or 100)))
        if mg.find("TitoliOpere") is None:
            etree.SubElement(mg, "TitoliOpere")

        # build each ordine
        # We create fresh OrdineDiPosto to ensure correct child order
        for cod_ord, od in orders.items():
            odp = etree.Element("OrdineDiPosto")
            etree.SubElement(odp, "CodiceOrdine").text = str(cod_ord)
            etree.SubElement(odp, "Capienza").text = str(int(od.get("capienza",0) or 0))
            etree.SubElement(odp, "IVAEccedenteOmaggi").text = str(int(od.get("iva_ecc_omaggi",0) or 0))

            # TitoliAccesso
            for tipo in sorted(od.get("titoli", {}).keys()):
                sums = od["titoli"][tipo]
                ta = etree.SubElement(odp, "TitoliAccesso")
                etree.SubElement(ta, "TipoTitolo").text = str(tipo)
                etree.SubElement(ta, "Quantita").text = str(int(sums["qty"]))
                etree.SubElement(ta, "CorrispettivoLordo").text = str(int(sums["corr"]))
                etree.SubElement(ta, "Prevendita").text = str(int(sums["prev"]))
                etree.SubElement(ta, "IVACorrispettivo").text = str(int(sums["ivac"]))
                etree.SubElement(ta, "IVAPrevendita").text = str(int(sums["ivap"]))
                etree.SubElement(ta, "ImportoPrestazione").text = "0"

            # TitoliAnnullati
            for tipo in sorted(od.get("annullati", {}).keys()):
                sums = od["annullati"][tipo]
                ta = etree.SubElement(odp, "TitoliAnnullati")
                etree.SubElement(ta, "TipoTitolo").text = str(tipo)
                etree.SubElement(ta, "Quantita").text = str(int(sums["qty"]))
                etree.SubElement(ta, "CorrispettivoLordo").text = str(int(sums["corr"]))
                etree.SubElement(ta, "Prevendita").text = str(int(sums["prev"]))
                etree.SubElement(ta, "IVACorrispettivo").text = str(int(sums["ivac"]))
                etree.SubElement(ta, "IVAPrevendita").text = str(int(sums["ivap"]))
                etree.SubElement(ta, "ImportoPrestazione").text = "0"

            # BigliettiAbbonamento
            for (cf,codabb,tipo), sums in sorted(od.get("biglietti_abbonamento", {}).items()):
                ba = etree.SubElement(odp, "BigliettiAbbonamento")
                etree.SubElement(ba, "CodiceFiscale").text = str(cf)
                etree.SubElement(ba, "CodiceAbbonamento").text = str(codabb)
                etree.SubElement(ba, "TipoTitolo").text = str(tipo)
                etree.SubElement(ba, "Quantita").text = str(int(sums["qty"]))
                etree.SubElement(ba, "ImportoFigurativo").text = str(int(sums["imp"]))
                etree.SubElement(ba, "IVAFigurativa").text = str(int(sums["iva"]))

            # AbbonamentiFissi
            for (cf,codabb,tipo), sums in sorted(od.get("abbonamenti_fissi", {}).items()):
                af = etree.SubElement(odp, "AbbonamentiFissi")
                etree.SubElement(af, "CodiceFiscale").text = str(cf)
                etree.SubElement(af, "CodiceAbbonamento").text = str(codabb)
                etree.SubElement(af, "TipoTitolo").text = str(tipo)
                etree.SubElement(af, "Quantita").text = str(int(sums["qty"]))
                etree.SubElement(af, "ImportoFigurativo").text = str(int(sums["imp"]))
                etree.SubElement(af, "IVAFigurativa").text = str(int(sums["iva"]))

            evn.append(odp)

        return evn

    # Add events sorted by date/time
    def ev_sort_key(item):
        eid, data = item
        meta = data["meta"] or {}
        return (str(meta.get("data_evento","")), str(meta.get("ora_evento","")), eid)

    for eid, data in sorted(ev_aggr.items(), key=ev_sort_key):
        meta = data["meta"] or {}
        # Only include events with date in month if available
        de = str(meta.get("data_evento",""))
        if de and de[:6] != month_yyyymm:
            # skip if strictly outside month
            continue
        org.append(build_event_node(meta, data["orders"]))

    # Add Abbonamenti products summaries
    for k, sums in sorted(ab_prod_aggr.items()):
        code, turno, validita, tipo_tass, cod_ord, tipo_tit, qev = k
        if sums["qty"] <= 0:
            continue
        abn = deepcopy(base_ab)
        # clear children
        for ch in list(abn):
            abn.remove(ch)

        etree.SubElement(abn, "CodiceAbbonamento").text = str(code)
        etree.SubElement(abn, "Validita").text = str(validita)
        tt = etree.SubElement(abn, "TipoTassazione")
        tt.attrib["valore"] = str(tipo_tass)
        tu = etree.SubElement(abn, "Turno")
        tu.attrib["valore"] = str(turno)
        etree.SubElement(abn, "CodiceOrdine").text = str(cod_ord)
        etree.SubElement(abn, "TipoTitolo").text = str(tipo_tit)
        etree.SubElement(abn, "QuantitaEventiAbilitati").text = str(int(qev))

        em = etree.SubElement(abn, "AbbonamentiEmessi")
        etree.SubElement(em, "Quantita").text = str(int(sums["qty"]))
        etree.SubElement(em, "CorrispettivoLordo").text = str(int(sums["corr"]))
        etree.SubElement(em, "Prevendita").text = str(int(sums["prev"]))
        etree.SubElement(em, "IVACorrispettivo").text = str(int(sums["ivac"]))
        etree.SubElement(em, "IVAPrevendita").text = str(int(sums["ivap"]))

        org.append(abn)

    # Serialize with doctype
    xml_body = etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True).decode("utf-8")
    if doctype:
        # inject doctype after xml declaration
        lines = xml_body.splitlines()
        if lines and lines[0].startswith("<?xml"):
            xml_body = "\n".join([lines[0], doctype] + lines[1:])
    return xml_body.encode("utf-8")

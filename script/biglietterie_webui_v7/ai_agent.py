from __future__ import annotations

import io
import json
import os
import re
import urllib.error
import urllib.request
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import engine


SUPPORTED_ACTIONS = [
    "update_anagrafica",
    "add_card",
    "create_event",
    "add_price",
    "add_subscription_product",
    "issue_ticket",
    "sell_subscription",
    "issue_subscription_ticket",
    "cancel_ticket",
    "record_access",
    "set_block",
]


def _allowed_actions_for_page(page_name: str) -> Optional[set]:
    p = str(page_name or "").strip()
    if not p:
        return None
    mapping = {
        "Anagrafica": {"update_anagrafica"},
        "Carte": {"add_card"},
        "Eventi (wizard)": {"create_event", "add_price"},
        "Abbonamenti (wizard)": {"add_subscription_product"},
        "Giornata (wizard)": {
            "issue_ticket",
            "sell_subscription",
            "issue_subscription_ticket",
            "cancel_ticket",
            "record_access",
            "set_block",
        },
        # Pagine non operative: nessuna azione applicabile.
        "Assistente AI (voce)": set(),
        "Template + Import": set(),
        "Dati di riferimento": set(),
        "Export": set(),
    }
    return mapping.get(p, None)


def resolve_ai_config(ai_cfg: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    cfg = ai_cfg or {}
    provider = str(cfg.get("provider") or os.getenv("AI_PROVIDER") or "localai").strip().lower()
    base_url = str(cfg.get("base_url") or os.getenv("OPENAI_BASE_URL") or "").strip()
    api_key = str(cfg.get("api_key") or os.getenv("OPENAI_API_KEY") or "").strip()
    command_model = str(cfg.get("command_model") or os.getenv("OPENAI_COMMAND_MODEL") or "llama-3.2-3b-instruct:q4_k_m").strip()
    transcribe_model = str(cfg.get("transcribe_model") or os.getenv("OPENAI_TRANSCRIBE_MODEL") or "whisper-1").strip()

    if provider in ("localai", "vllm") and not api_key:
        api_key = provider
    if provider == "localai" and not base_url:
        base_url = "http://localai:8080/v1"
    if provider == "vllm" and not base_url:
        base_url = "http://vllm:8000/v1"

    return {
        "provider": provider,
        "base_url": base_url,
        "api_key": api_key,
        "command_model": command_model,
        "transcribe_model": transcribe_model,
    }


def check_agent_ready(ai_cfg: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    try:
        from openai import OpenAI  # noqa: F401
    except Exception:
        return False, "Pacchetto 'openai' non disponibile. Installa le dipendenze aggiornate."
    cfg = resolve_ai_config(ai_cfg)
    provider = cfg["provider"]
    if provider == "openai" and not cfg["api_key"]:
        return False, "Provider OpenAI richiede api_key."
    if provider in ("localai", "vllm") and not cfg["base_url"]:
        return False, f"Provider {provider} richiede base_url."
    return True, f"Assistente AI pronto ({provider})."


def _client(ai_cfg: Optional[Dict[str, Any]] = None):
    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("Pacchetto 'openai' non installato.") from exc
    cfg = resolve_ai_config(ai_cfg)
    provider = cfg["provider"]
    if provider == "openai" and not cfg["api_key"]:
        raise RuntimeError("Provider OpenAI: api_key mancante.")
    if provider in ("localai", "vllm") and not cfg["base_url"]:
        raise RuntimeError(f"Provider {provider}: base_url mancante.")
    kwargs: Dict[str, Any] = {"api_key": cfg["api_key"] or "local"}
    if cfg["base_url"]:
        kwargs["base_url"] = cfg["base_url"]
    return OpenAI(**kwargs)


def list_models(ai_cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    client = _client(ai_cfg)
    resp = client.models.list()
    out = []
    for m in getattr(resp, "data", []) or []:
        mid = getattr(m, "id", None)
        if mid:
            out.append(str(mid))
    return sorted(out)


def _safe_list_models(ai_cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    try:
        return list_models(ai_cfg)
    except Exception:
        return []


def _is_probably_chat_model(model_id: str) -> bool:
    m = (model_id or "").lower()
    non_chat_markers = (
        "whisper",
        "embedding",
        "rerank",
        "tts",
        "stablediffusion",
        "diffusion",
        "image",
        "vision",
        "vad",
    )
    return not any(k in m for k in non_chat_markers)


def _pick_fallback_chat_model(available_models: List[str]) -> str:
    if not available_models:
        return ""
    preferred = [
        "llama-3.2-3b-instruct:q4_k_m",
        "llama-3.2-3b-instruct:q8_0",
    ]
    s = set(available_models)
    for p in preferred:
        if p in s:
            return p
    ranked: List[str] = []
    for m in available_models:
        ml = m.lower()
        if not _is_probably_chat_model(m):
            continue
        if any(x in ml for x in ("instruct", "chat", "llama", "qwen", "mistral", "gemma")):
            ranked.append(m)
    if ranked:
        return sorted(ranked)[0]
    plain = [m for m in available_models if _is_probably_chat_model(m)]
    if plain:
        return sorted(plain)[0]
    return ""


def _pick_fallback_transcribe_model(available_models: List[str]) -> str:
    if not available_models:
        return ""
    s = set(available_models)
    if "whisper-1" in s:
        return "whisper-1"
    for m in available_models:
        if "whisper" in m.lower():
            return m
    return ""


def _localai_root_url(ai_cfg: Optional[Dict[str, Any]] = None) -> str:
    cfg = resolve_ai_config(ai_cfg)
    base = cfg["base_url"].strip() or "http://localai:8080/v1"
    if base.endswith("/v1"):
        return base[:-3]
    return base.rstrip("/")


def localai_search_gallery_models(ai_cfg: Optional[Dict[str, Any]], query: str, limit: int = 20) -> List[str]:
    cfg = resolve_ai_config(ai_cfg)
    if cfg["provider"] != "localai":
        raise RuntimeError("Ricerca gallery disponibile solo con provider localai.")
    root = _localai_root_url(ai_cfg)
    url = f"{root}/models/available"
    with urllib.request.urlopen(url, timeout=45) as r:
        payload = json.loads(r.read().decode())
    if not isinstance(payload, list):
        return []
    q = (query or "").strip().lower()
    names = []
    for item in payload:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        if not q or q in name.lower():
            names.append(name)
    return sorted(list(dict.fromkeys(names)))[: max(1, int(limit))]


def localai_install_model(ai_cfg: Optional[Dict[str, Any]], model_name: str) -> Dict[str, Any]:
    cfg = resolve_ai_config(ai_cfg)
    if cfg["provider"] != "localai":
        raise RuntimeError("Installazione modello disponibile solo con provider localai.")
    model_name = str(model_name or "").strip()
    if not model_name:
        raise RuntimeError("Nome modello vuoto.")
    root = _localai_root_url(ai_cfg)
    url = f"{root}/models/apply"
    body = json.dumps({"id": model_name}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            payload = json.loads(r.read().decode())
        return payload if isinstance(payload, dict) else {"raw": payload}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        raise RuntimeError(f"Errore installazione modello '{model_name}': {detail}") from e


def localai_get_job(ai_cfg: Optional[Dict[str, Any]], job_ref: str) -> Dict[str, Any]:
    cfg = resolve_ai_config(ai_cfg)
    if cfg["provider"] != "localai":
        raise RuntimeError("Controllo job disponibile solo con provider localai.")
    root = _localai_root_url(ai_cfg)
    ref = str(job_ref or "").strip()
    if not ref:
        raise RuntimeError("job_ref vuoto.")
    if ref.startswith("http://") or ref.startswith("https://"):
        url = ref
    else:
        url = f"{root}/models/jobs/{ref}"
    with urllib.request.urlopen(url, timeout=45) as r:
        payload = json.loads(r.read().decode())
    return payload if isinstance(payload, dict) else {"raw": payload}


def transcribe_audio(audio_bytes: bytes, filename: str = "comando.wav", ai_cfg: Optional[Dict[str, Any]] = None) -> str:
    if not audio_bytes:
        return ""
    client = _client(ai_cfg)
    cfg = resolve_ai_config(ai_cfg)
    provider = cfg["provider"]
    model = cfg["transcribe_model"]
    available = _safe_list_models(ai_cfg) if provider in ("localai", "vllm") else []
    if available and model not in available:
        fallback = _pick_fallback_transcribe_model(available)
        if fallback:
            model = fallback
            if isinstance(ai_cfg, dict):
                ai_cfg["transcribe_model"] = fallback
        else:
            raise RuntimeError(
                f"Modello trascrizione '{cfg['transcribe_model']}' non disponibile. "
                f"Modelli disponibili: {', '.join(available[:20])}"
            )
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename
    try:
        tr = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language="it",
            prompt="Comando operativo per software di biglietteria."
        )
    except Exception as exc:
        raise RuntimeError(
            f"Trascrizione fallita con modello '{model}'. "
            "Controlla che il provider esponga /v1/audio/transcriptions."
        ) from exc
    text = getattr(tr, "text", None)
    if text is None and isinstance(tr, dict):
        text = tr.get("text")
    return (text or "").strip()


def build_context(cfg: Dict[str, Any], day: Dict[str, Any], date_iso: str, page_name: str = "") -> Dict[str, Any]:
    events = cfg.get("eventi", []) or []
    cards = [c.get("carta_attivazione", "") for c in (cfg.get("carte", []) or []) if c.get("carta_attivazione")]
    subs = [a.get("codice_abbonamento", "") for a in (cfg.get("abbonamenti_prodotti", []) or []) if a.get("codice_abbonamento")]
    event_map: Dict[str, Dict[str, Any]] = {}
    for e in events:
        sectors = []
        prices_by_sector: Dict[str, List[str]] = {}
        for s in (e.get("settori", []) or []):
            cod_ord = str(s.get("codice_ordine", ""))
            if not cod_ord:
                continue
            sectors.append(cod_ord)
            prices_by_sector[cod_ord] = sorted(list((s.get("prezzi", {}) or {}).keys()))
        event_map[str(e.get("id", ""))] = {
            "id": str(e.get("id", "")),
            "codice_locale": str(e.get("codice_locale", "")),
            "titolo_evento": str(e.get("titolo_evento", "")),
            "data_evento": str(e.get("data_evento", "")),
            "ora_evento": str(e.get("ora_evento", "")),
            "settori": sorted(sectors),
            "prezzi_per_settore": prices_by_sector,
        }

    titles = [t for t in (day.get("titoli", []) or []) if t.get("key")]
    title_keys = [t.get("key", "") for t in titles]
    title_keys_cancelable = [t.get("key", "") for t in titles if engine.title_can_cancel(t)]
    title_keys_transitable = [t.get("key", "") for t in titles if engine.title_can_transit(t)]
    title_keys_blockable = [t.get("key", "") for t in titles if engine.title_can_block(t)]
    anag = cfg.get("anagrafica", {}) or {}
    allowed_actions = _allowed_actions_for_page(page_name)
    return {
        "operational_date_iso": date_iso,
        "supported_actions": SUPPORTED_ACTIONS,
        "ui_current_page": str(page_name or ""),
        "allowed_actions_current_page": sorted(list(allowed_actions)) if allowed_actions is not None else [],
        "anagrafica_current": {
            "cf_organizzatore": str(anag.get("cf_organizzatore", "")),
            "cf_titolare": str(anag.get("cf_titolare", "")),
            "sistema_emissione": str(anag.get("sistema_emissione", "")),
            "codice_richiedente_emissione_sigillo": str(anag.get("codice_richiedente_emissione_sigillo", "")),
        },
        "anagrafica_fields": [
            "cf_organizzatore",
            "cf_titolare",
            "sistema_emissione",
            "codice_richiedente_emissione_sigillo",
            "denominazione_titolare",
            "denominazione_organizzatore",
            "tipo_organizzatore",
        ],
        "cards": sorted(cards),
        "subscriptions": sorted(list(set(subs))),
        "events": event_map,
        "title_keys": sorted(title_keys),
        "title_keys_cancelable": sorted(title_keys_cancelable),
        "title_keys_transitable": sorted(title_keys_transitable),
        "title_keys_blockable": sorted(title_keys_blockable),
        "defaults": {
            "supporto": "BT",
            "turno": "L",
            "quantita": 1,
            "ora_emissione_hhmm": datetime.now().strftime("%H%M"),
        },
    }


def _has_anagrafica_signal(command_text: str) -> bool:
    low = (command_text or "").lower()
    signals = (
        "anagrafica",
        "cf organizzatore",
        "cf titolare",
        "cf org",
        "cf tit",
        "sistema emissione",
        "codicerichiedenteemissionesigillo",
        "codice richiedente emissione sigillo",
        "richiedente emissione sigillo",
    )
    return any(k in low for k in signals)


def _has_explicit_card_signal(command_text: str) -> bool:
    low = (command_text or "").lower()
    card_signals = (
        " carta ",
        " carte ",
        "carta attivazione",
        "card",
    )
    padded = f" {low} "
    return any(k in padded for k in card_signals)


def _try_parse_anagrafica_command(command_text: str) -> Optional[Dict[str, Any]]:
    txt = (command_text or "").strip()
    if not txt:
        return None
    up = txt.upper()
    has_ana_signal = _has_anagrafica_signal(txt)
    if not has_ana_signal:
        return None

    params: Dict[str, Any] = {}

    same_cf = re.search(r"CF\s+ORGANIZZATORE\s+E\s+TITOLARE\s*[:=]?\s*([A-Z0-9]{11,16})", up)
    if same_cf:
        params["cf_organizzatore"] = same_cf.group(1)
        params["cf_titolare"] = same_cf.group(1)

    m_org = re.search(r"CF\s+ORGANIZZATORE\s*[:=]?\s*([A-Z0-9]{11,16})", up)
    if m_org:
        params["cf_organizzatore"] = m_org.group(1)

    m_tit = re.search(r"CF\s+TITOLARE\s*[:=]?\s*([A-Z0-9]{11,16})", up)
    if m_tit:
        params["cf_titolare"] = m_tit.group(1)

    m_sys = re.search(r"\bSISTEMA(?:\s+EMISSIONE)?\s*[:=]?\s*([A-Z0-9]{3,20})", up)
    if m_sys:
        params["sistema_emissione"] = m_sys.group(1)

    m_sig = re.search(r"CODICE\s*RICHIEDENTE\s*EMISSIONE\s*SIGILLO\s*[:=]?\s*([A-Z0-9]{2,20})", up)
    if m_sig:
        params["codice_richiedente_emissione_sigillo"] = m_sig.group(1)
    else:
        m_sig2 = re.search(r"CODICERICHIEDENTEEMISSIONESIGILLO\s*[:=]?\s*([A-Z0-9]{2,20})", up)
        if m_sig2:
            params["codice_richiedente_emissione_sigillo"] = m_sig2.group(1)

    if not params:
        return None

    return {
        "summary": "Aggiornamento anagrafica",
        "confidence": 0.98,
        "missing_fields": [],
        "actions": [
            {
                "type": "update_anagrafica",
                "params": params,
                "confidence": 0.98,
            }
        ],
    }


def _enforce_domain_guardrails(command_text: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
    if not _has_anagrafica_signal(command_text):
        return parsed
    if _has_explicit_card_signal(command_text):
        return parsed

    actions = parsed.get("actions", []) or []
    has_update_ana = any(str(a.get("type", "")).strip() == "update_anagrafica" for a in actions)
    has_add_card = any(str(a.get("type", "")).strip() == "add_card" for a in actions)

    if has_add_card and not has_update_ana:
        out = dict(parsed)
        missing = list(out.get("missing_fields", []) or [])
        missing.append(
            "Comando anagrafica rilevato: azione 'add_card' bloccata. Specifica campi anagrafica."
        )
        out["actions"] = []
        out["missing_fields"] = missing
        out["summary"] = out.get("summary") or "Richiesta anagrafica rilevata."
        out["confidence"] = min(float(out.get("confidence", 0.0) or 0.0), 0.6)
        return out
    return parsed


def _enforce_page_scope(parsed: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    page_name = str((context or {}).get("ui_current_page", "") or "")
    allowed = _allowed_actions_for_page(page_name)
    if allowed is None:
        return parsed

    actions = parsed.get("actions", []) or []
    if not actions:
        return parsed

    kept = []
    dropped = []
    for a in actions:
        a_type = str(a.get("type", "")).strip()
        if a_type in allowed:
            kept.append(a)
        else:
            dropped.append(a_type or "<vuoto>")

    if not dropped:
        return parsed

    out = dict(parsed)
    out["actions"] = kept
    missing = list(out.get("missing_fields", []) or [])
    if len(allowed) == 0:
        missing.append(
            f"La scheda corrente '{page_name}' non consente azioni operative. "
            "Spostati nella scheda corretta e ripeti il comando."
        )
    else:
        allowed_txt = ", ".join(sorted(allowed))
        dropped_txt = ", ".join(sorted(set(dropped)))
        missing.append(
            f"Comando fuori ambito per la scheda '{page_name}'. "
            f"Ammesse: {allowed_txt}. Scartate: {dropped_txt}."
        )
    out["missing_fields"] = missing
    if not kept:
        out["summary"] = out.get("summary") or "Nessuna azione applicabile nella scheda corrente."
        out["confidence"] = min(float(out.get("confidence", 0.0) or 0.0), 0.6)
    return out


def parse_actions(command_text: str, context: Dict[str, Any], ai_cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not command_text.strip():
        return {"summary": "", "actions": [], "missing_fields": ["testo comando vuoto"], "confidence": 0.0}

    fast = _try_parse_anagrafica_command(command_text)
    if fast is not None:
        return _enforce_page_scope(_enforce_domain_guardrails(command_text, fast), context)

    client = _client(ai_cfg)
    cfg = resolve_ai_config(ai_cfg)
    provider = cfg["provider"]
    model = cfg["command_model"]
    available = _safe_list_models(ai_cfg) if provider in ("localai", "vllm") else []
    if available and model not in available:
        fallback = _pick_fallback_chat_model(available)
        if fallback:
            model = fallback
            if isinstance(ai_cfg, dict):
                ai_cfg["command_model"] = fallback
        else:
            raise RuntimeError(
                f"Modello comandi '{cfg['command_model']}' non disponibile e nessun modello chat trovato. "
                f"Modelli disponibili: {', '.join(available[:20])}"
            )
    system = (
        "Converti il comando italiano in azioni JSON per un tool biglietteria.\n"
        "Rispondi SOLO con JSON valido.\n"
        "Non inventare id evento, carte, codici abbonamento o titolo_key: usa quelli presenti nel context quando disponibili.\n"
        "Se un campo essenziale manca o è ambiguo, aggiungilo in missing_fields.\n"
        "Schema:\n"
        "{"
        "\"summary\":\"...\","
        "\"confidence\":0.0,"
        "\"missing_fields\":[\"...\"],"
        "\"actions\":["
        "{\"type\":\"update_anagrafica|add_card|create_event|add_price|add_subscription_product|issue_ticket|sell_subscription|issue_subscription_ticket|cancel_ticket|record_access|set_block\","
        "\"params\":{...},\"confidence\":0.0}"
        "]"
        "}\n"
        "Disambiguazione obbligatoria:\n"
        "- Se il testo parla di 'anagrafica' o contiene campi CF/Sistema/CodiceRichiedenteEmissioneSigillo, usa 'update_anagrafica'.\n"
        "- Usa 'add_card' solo quando l'utente chiede esplicitamente carta/carte/carta attivazione.\n"
        "- Se context.ui_current_page='Anagrafica', prediligi update_anagrafica ed evita add_card salvo richiesta esplicita.\n"
        "- Usa solo action type presenti in context.allowed_actions_current_page (se la lista non e' vuota).\n"
        "Parametri principali attesi:\n"
        "- update_anagrafica: cf_organizzatore, cf_titolare, sistema_emissione, codice_richiedente_emissione_sigillo, denominazione_titolare, denominazione_organizzatore, tipo_organizzatore\n"
        "- add_card: carta_attivazione, progressivo_next\n"
        "- create_event: codice_locale, titolo_evento, data_evento(YYYYMMDD), ora_evento(HHMM), tipo_genere, tipo_tassazione, iva_percent, isi_percent, codice_ordine, capienza\n"
        "- add_price: event_id, codice_ordine, price_key, tipo_titolo, corrispettivo_eur, prevendita_eur, iva_percent, causale\n"
        "- add_subscription_product: codice_abbonamento, turno, tipo_tassazione, validita, codice_ordine, tipo_titolo, q_eventi_abilitati, corrispettivo_eur, prevendita_eur, iva_percent, progressivo_next\n"
        "- issue_ticket: event_id, codice_ordine, price_key, carta_attivazione, quantita, supporto, ora_emissione\n"
        "- sell_subscription: codice_abbonamento, turno, carta_attivazione, quantita, ora_emissione\n"
        "- issue_subscription_ticket: event_id, codice_ordine, tipo_titolo, carta_attivazione, quantita, supporto, ora_emissione, codice_abbonamento, cf_abbonamento, progressivo_abbonamento\n"
        "- cancel_ticket: titolo_key, causale_annullamento, carta_annullamento\n"
        "- record_access: titolo_key, timestamp_iso, mode\n"
        "- set_block: titolo_key, kind(BL|DASPO|RUBATO)\n"
        "Vincoli titolo_key:\n"
        "- cancel_ticket: usa preferibilmente context.title_keys_cancelable.\n"
        "- record_access: usa preferibilmente context.title_keys_transitable.\n"
        "- set_block: usa preferibilmente context.title_keys_blockable.\n"
        "Esempio vincolante:\n"
        "- 'inserisci questa anagrafica CF Organizzatore e Titolare SPGGGR81B09I119V Sistema P003003 CodiceRichiedenteEmissioneSigillo CL002'\n"
        "  => action type 'update_anagrafica' con quei campi; MAI 'add_card'.\n"
    )
    user = {
        "command_text": command_text,
        "context": context,
    }
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
        )
    except Exception as exc:
        msg = str(exc)
        if ("could not load model" in msg.lower() or "no such file or directory" in msg.lower()) and available:
            raise RuntimeError(
                f"Il modello comandi '{model}' non è caricabile. "
                f"Disponibili: {', '.join(available[:20])}. "
                "Seleziona un modello disponibile o installalo dalla sezione Tooling LocalAI."
            ) from exc
        raise RuntimeError(f"Errore modello comandi '{model}': {msg}") from exc
    content = resp.choices[0].message.content or "{}"
    try:
        parsed = json.loads(content)
    except Exception as exc:
        raise RuntimeError(f"Risposta AI non parsabile: {content}") from exc

    parsed.setdefault("summary", "")
    parsed.setdefault("actions", [])
    parsed.setdefault("missing_fields", [])
    parsed.setdefault("confidence", 0.0)
    if not isinstance(parsed["actions"], list):
        parsed["actions"] = []
    if not isinstance(parsed["missing_fields"], list):
        parsed["missing_fields"] = [str(parsed["missing_fields"])]
    out = _enforce_domain_guardrails(command_text, parsed)
    out = _enforce_page_scope(out, context)
    return out


def _to_int(v: Any, default: int = 0) -> int:
    try:
        return int(float(v))
    except Exception:
        return default


def _norm_date_yyyymmdd(v: Any, fallback_iso: str) -> str:
    s = str(v or "").strip()
    if not s:
        return engine.yyyymmdd_from_iso(fallback_iso)
    if len(s) == 8 and s.isdigit():
        return s
    if len(s) >= 10 and "-" in s:
        raw = s[0:10].replace("-", "")
        if len(raw) == 8 and raw.isdigit():
            return raw
    raise ValueError(f"Data non valida: {v}")


def _norm_hhmm(v: Any) -> str:
    s = str(v or "").strip()
    if not s:
        return datetime.now().strftime("%H%M")
    s = s.replace(":", "")
    if len(s) >= 4:
        s = s[0:4]
    if len(s) == 4 and s.isdigit():
        return s
    raise ValueError(f"Ora non valida: {v}")


def _resolve_event_id(cfg: Dict[str, Any], params: Dict[str, Any], fallback_date_iso: str) -> str:
    ev_id = str(params.get("event_id", "")).strip()
    if ev_id:
        engine.find_event(cfg, ev_id)
        return ev_id

    codice_locale = str(params.get("codice_locale", "")).strip()
    titolo = str(params.get("titolo_evento", "")).strip().lower()
    data_evento = str(params.get("data_evento", "")).strip()
    ora_evento = str(params.get("ora_evento", "")).strip()

    if codice_locale and data_evento and ora_evento:
        de = _norm_date_yyyymmdd(data_evento, fallback_date_iso)
        oe = _norm_hhmm(ora_evento)
        ev = engine.find_event_by_key(cfg, codice_locale, de, oe)
        if ev:
            return str(ev.get("id", ""))

    if titolo:
        hits = [e for e in (cfg.get("eventi", []) or []) if titolo in str(e.get("titolo_evento", "")).lower()]
        if len(hits) == 1:
            return str(hits[0].get("id", ""))
    raise ValueError("event_id non risolto (fornisci un id evento valido).")


def apply_actions(
    cfg: Dict[str, Any],
    day: Dict[str, Any],
    date_iso: str,
    actions: List[Dict[str, Any]]
) -> Tuple[List[str], bool, bool]:
    work_cfg = deepcopy(cfg)
    work_day = deepcopy(day)
    messages: List[str] = []
    changed_cfg = False
    changed_day = False

    for i, action in enumerate(actions, start=1):
        a_type = str(action.get("type", "")).strip()
        params = action.get("params", {}) or {}
        if a_type not in SUPPORTED_ACTIONS:
            raise ValueError(f"Azione non supportata: {a_type}")

        if a_type == "update_anagrafica":
            an = work_cfg.setdefault("anagrafica", {})
            updates: Dict[str, str] = {}
            field_map = {
                "cf_organizzatore": ["cf_organizzatore", "cfOrganizzatore", "CFOrganizzatore"],
                "cf_titolare": ["cf_titolare", "cfTitolare", "CFTitolare"],
                "sistema_emissione": ["sistema_emissione", "sistemaEmissione", "SistemaEmissione"],
                "codice_richiedente_emissione_sigillo": [
                    "codice_richiedente_emissione_sigillo",
                    "codiceRichiedenteEmissioneSigillo",
                    "CodiceRichiedenteEmissioneSigillo",
                ],
                "denominazione_titolare": ["denominazione_titolare", "denominazioneTitolare"],
                "denominazione_organizzatore": ["denominazione_organizzatore", "denominazioneOrganizzatore"],
                "tipo_organizzatore": ["tipo_organizzatore", "tipoOrganizzatore", "TipoOrganizzatore"],
            }
            for target, keys in field_map.items():
                for k in keys:
                    if k in params and params.get(k) not in (None, ""):
                        val = str(params.get(k)).strip()
                        if target == "tipo_organizzatore":
                            val = val.upper()
                            if val not in ("G", "S"):
                                continue
                        updates[target] = val
                        break
            if not updates:
                raise ValueError("update_anagrafica: nessun campo valido fornito.")
            an.update(updates)
            changed_cfg = True
            shown = ", ".join([f"{k}={v}" for k, v in updates.items()])
            messages.append(f"{i}) Anagrafica aggiornata: {shown}.")

        elif a_type == "add_card":
            carta = str(params.get("carta_attivazione", "")).strip()
            if not carta:
                raise ValueError("add_card: carta_attivazione mancante.")
            prog = max(1, _to_int(params.get("progressivo_next", 1), 1))
            engine.ensure_card(work_cfg, carta, prog)
            changed_cfg = True
            messages.append(f"{i}) Carta salvata: {carta} (next={prog}).")

        elif a_type == "create_event":
            codice_locale = str(params.get("codice_locale", "")).strip()
            titolo = str(params.get("titolo_evento", "")).strip()
            if not codice_locale or not titolo:
                raise ValueError("create_event: codice_locale e titolo_evento sono obbligatori.")
            data_evento = _norm_date_yyyymmdd(params.get("data_evento"), date_iso)
            ora_evento = _norm_hhmm(params.get("ora_evento"))
            event_id = engine.make_event_id(codice_locale, data_evento, ora_evento, titolo)
            ev = None
            for e in work_cfg.get("eventi", []):
                if e.get("id") == event_id:
                    ev = e
                    break
            if ev is None:
                ev = {"id": event_id, "settori": []}
                work_cfg.setdefault("eventi", []).append(ev)
            ev.update({
                "id": event_id,
                "codice_locale": codice_locale,
                "titolo_evento": titolo,
                "tipo_genere": str(params.get("tipo_genere", "1")),
                "data_evento": data_evento,
                "ora_evento": ora_evento,
                "data_apertura": data_evento,
                "ora_apertura": ora_evento,
                "tipo_tassazione": str(params.get("tipo_tassazione", "S")),
                "iva_percent": _to_int(params.get("iva_percent", 0), 0),
                "isi_percent": _to_int(params.get("isi_percent", 0), 0),
            })
            cod_ord = str(params.get("codice_ordine", "UN")).strip() or "UN"
            sec = engine.ensure_sector(ev, cod_ord)
            sec["capienza"] = max(0, _to_int(params.get("capienza", 0), 0))
            sec.setdefault("prezzi", {})
            changed_cfg = True
            messages.append(f"{i}) Evento salvato: {event_id} (settore {cod_ord}).")

        elif a_type == "add_price":
            event_id = _resolve_event_id(work_cfg, params, date_iso)
            cod_ord = str(params.get("codice_ordine", "")).strip()
            price_key = str(params.get("price_key", "")).strip()
            if not cod_ord or not price_key:
                raise ValueError("add_price: codice_ordine e price_key sono obbligatori.")
            ev = engine.find_event(work_cfg, event_id)
            iva_default = _to_int(ev.get("iva_percent", 0), 0)
            engine.add_or_update_price(work_cfg, event_id, cod_ord, price_key, {
                "tipo_titolo": str(params.get("tipo_titolo", "I1")),
                "corrispettivo_eur": str(params.get("corrispettivo_eur", "0.00")),
                "prevendita_eur": str(params.get("prevendita_eur", "0.00")),
                "iva_percent": _to_int(params.get("iva_percent", iva_default), iva_default),
                "causale": str(params.get("causale", "")),
            })
            changed_cfg = True
            messages.append(f"{i}) Prezzo salvato: {price_key} su {event_id}/{cod_ord}.")

        elif a_type == "add_subscription_product":
            codice = str(params.get("codice_abbonamento", "")).strip()
            if not codice:
                raise ValueError("add_subscription_product: codice_abbonamento mancante.")
            item = {
                "codice_abbonamento": codice,
                "turno": str(params.get("turno", "L")).upper(),
                "tipo_tassazione": str(params.get("tipo_tassazione", "S")),
                "validita": _norm_date_yyyymmdd(params.get("validita"), date_iso),
                "codice_ordine": str(params.get("codice_ordine", "UN")),
                "tipo_titolo": str(params.get("tipo_titolo", "I1")),
                "q_eventi_abilitati": max(1, _to_int(params.get("q_eventi_abilitati", 1), 1)),
                "corrispettivo_eur": str(params.get("corrispettivo_eur", "0.00")),
                "prevendita_eur": str(params.get("prevendita_eur", "0.00")),
                "iva_percent": _to_int(params.get("iva_percent", 10), 10),
                "progressivo_next": max(1, _to_int(params.get("progressivo_next", 1), 1)),
            }
            engine.add_or_update_abbonamento(work_cfg, item)
            changed_cfg = True
            messages.append(f"{i}) Prodotto abbonamento salvato: {codice}.")

        elif a_type == "issue_ticket":
            event_id = _resolve_event_id(work_cfg, params, date_iso)
            cod_ord = str(params.get("codice_ordine", "")).strip()
            price_key = str(params.get("price_key", "")).strip()
            carta = str(params.get("carta_attivazione", "")).strip()
            if not cod_ord or not price_key or not carta:
                raise ValueError("issue_ticket: codice_ordine, price_key, carta_attivazione sono obbligatori.")
            quantita = max(1, _to_int(params.get("quantita", 1), 1))
            supporto = str(params.get("supporto", "BT")).upper()
            ora_em = _norm_hhmm(params.get("ora_emissione"))
            engine.issue_ticket(work_cfg, work_day, date_iso, event_id, cod_ord, price_key, carta, quantita, supporto, ora_em)
            changed_cfg = True
            changed_day = True
            messages.append(f"{i}) Emessi {quantita} biglietti su {event_id}/{cod_ord}/{price_key}.")

        elif a_type == "sell_subscription":
            codabb = str(params.get("codice_abbonamento", "")).strip()
            carta = str(params.get("carta_attivazione", "")).strip()
            if not codabb or not carta:
                raise ValueError("sell_subscription: codice_abbonamento e carta_attivazione sono obbligatori.")
            turno = str(params.get("turno", "L")).upper()
            quantita = max(1, _to_int(params.get("quantita", 1), 1))
            ora_em = _norm_hhmm(params.get("ora_emissione"))
            engine.sell_abbonamento(work_cfg, work_day, date_iso, codabb, turno, carta, quantita, ora_em)
            changed_cfg = True
            changed_day = True
            messages.append(f"{i}) Venduti {quantita} abbonamenti {codabb} (turno {turno}).")

        elif a_type == "issue_subscription_ticket":
            event_id = _resolve_event_id(work_cfg, params, date_iso)
            cod_ord = str(params.get("codice_ordine", "")).strip()
            tipo_titolo = str(params.get("tipo_titolo", "")).strip()
            carta = str(params.get("carta_attivazione", "")).strip()
            codabb = str(params.get("codice_abbonamento", "")).strip()
            if not cod_ord or not tipo_titolo or not carta or not codabb:
                raise ValueError("issue_subscription_ticket: campi obbligatori mancanti.")
            quantita = max(1, _to_int(params.get("quantita", 1), 1))
            supporto = str(params.get("supporto", "BT")).upper()
            ora_em = _norm_hhmm(params.get("ora_emissione"))
            cfabb = str(params.get("cf_abbonamento", work_cfg["anagrafica"].get("cf_titolare", "")))
            progabb = max(1, _to_int(params.get("progressivo_abbonamento", 1), 1))
            engine.issue_biglietto_abbonamento(
                work_cfg, work_day, date_iso, event_id, cod_ord, tipo_titolo, carta,
                quantita, supporto, ora_em, codabb, cfabb, progressivo_abbonamento=progabb
            )
            changed_cfg = True
            changed_day = True
            messages.append(f"{i}) Emessi {quantita} biglietti abbonamento ({codabb}-{progabb}).")

        elif a_type == "cancel_ticket":
            titolo_key = str(params.get("titolo_key", "")).strip()
            causale = str(params.get("causale_annullamento", "001")).strip().zfill(3)
            carta_ann = str(params.get("carta_annullamento", "")).strip()
            if not titolo_key or not carta_ann:
                raise ValueError("cancel_ticket: titolo_key e carta_annullamento sono obbligatori.")
            engine.cancel_ticket(work_cfg, work_day, date_iso, titolo_key, causale, carta_ann)
            changed_cfg = True
            changed_day = True
            messages.append(f"{i}) Titolo annullato: {titolo_key}.")

        elif a_type == "record_access":
            titolo_key = str(params.get("titolo_key", "")).strip()
            if not titolo_key:
                raise ValueError("record_access: titolo_key mancante.")
            ts = str(params.get("timestamp_iso", "")).strip()
            if not ts:
                dd = str(params.get("data_ingresso", date_iso))
                hh = _norm_hhmm(params.get("ora_ingresso"))
                dd_iso = dd if "-" in dd else engine.iso_from_yyyymmdd(_norm_date_yyyymmdd(dd, date_iso))
                ts = f"{dd_iso}T{hh[0:2]}:{hh[2:4]}:00"
            mode = str(params.get("mode", "AUTO")).upper()
            engine.record_access(work_day, titolo_key, ts, mode)
            changed_day = True
            messages.append(f"{i}) Accesso registrato su {titolo_key}.")

        elif a_type == "set_block":
            titolo_key = str(params.get("titolo_key", "")).strip()
            kind = str(params.get("kind", "BL")).upper()
            if not titolo_key:
                raise ValueError("set_block: titolo_key mancante.")
            engine.set_block_status(work_day, titolo_key, kind)
            changed_day = True
            messages.append(f"{i}) Blocco {kind} applicato su {titolo_key}.")

    cfg.clear()
    cfg.update(work_cfg)
    day.clear()
    day.update(work_day)
    return messages, changed_cfg, changed_day

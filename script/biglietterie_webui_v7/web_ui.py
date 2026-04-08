
import io
import zipfile
from pathlib import Path
import streamlit as st
import yaml

import ai_agent
import engine
import refdata

BASE_DIR = Path(__file__).resolve().parent
paths = engine.make_paths(BASE_DIR)

st.set_page_config(page_title="Biglietterie Web UI v7", layout="wide")

# --- iPad / Apple Pencil friendly UI tweaks ---
st.markdown(
    """
<style>
/* Bigger base font & spacing */
html, body, [class*="css"] { font-size: 19px; }
.block-container { padding-top: 1.0rem; padding-bottom: 6rem; } /* room for iPad keyboard */
h1, h2, h3 { letter-spacing: -0.2px; }

/* Bigger input controls */
div[data-baseweb="select"] > div { min-height: 3.1rem; }
input, textarea { font-size: 1.05rem !important; }

/* Big touch-friendly buttons */
.stButton > button {
  width: 100%;
  min-height: 3.2rem;
  font-size: 1.05rem;
  border-radius: 14px;
}

/* Tabs larger */
button[role="tab"] { font-size: 1.0rem; padding: 0.8rem 1rem; }

/* Data editor */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>
    """,
    unsafe_allow_html=True,
)


cfg = engine.ensure_config(paths)

# Load reference data from bundled files (or empty fallbacks)
try:
    REF = refdata.load_all(paths.reference_dir)
except Exception:
    REF = refdata.RefData([], [], [], refdata.pd.DataFrame(), {})

ORDINI_CODES = [x["code"] for x in REF.ordini_posto] or refdata.fallback_ordini()
TIPI_CODES = [x["code"] for x in REF.tipi_titolo] or refdata.fallback_tipi()
CAUSALI_CODES = [x["code"] for x in REF.causali_ann] or refdata.fallback_causali()
def load_abbonamenti_emessi(turno_filter: str = "L"):
    """Scansiona tutti i journal e restituisce lista di abbonamenti emessi (transazioni kind='abbonamento')."""
    items = []
    if not paths.journal_dir.exists():
        return items
    for p in sorted(paths.journal_dir.glob("*.yml")):
        try:
            obj = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        for tx in obj.get("transazioni", []) or []:
            if tx.get("kind") != "abbonamento":
                continue
            if str(tx.get("turno","")).upper() != str(turno_filter).upper():
                continue
            code = str(tx.get("codice_abbonamento",""))
            prog = int(tx.get("progressivo_abbonamento", 0) or 0)
            if not code or not prog:
                continue
            items.append({
                "label": f"{code}-{prog} ({p.stem})",
                "codice_abbonamento": code,
                "progressivo_abbonamento": prog,
                "turno": str(tx.get("turno","")).upper(),
                "validita": str(tx.get("validita","")),
            })
    # unique by (code,prog)
    seen=set(); out=[]
    for it in items:
        k=(it["codice_abbonamento"], it["progressivo_abbonamento"])
        if k in seen: 
            continue
        seen.add(k); out.append(it)
    return out


def save_cfg():
    engine.save_config(paths, cfg)

def file_present(p: Path) -> bool:
    return p.exists() and p.stat().st_size > 0


def _chat_history():
    return st.session_state.setdefault("global_chat_history", [])


def _chat_add(role: str, text: str):
    text = (text or "").strip()
    if not text:
        return
    _chat_history().append({"role": role, "text": text})


def render_global_assistant(page_name: str):
    ai_cfg = cfg.setdefault("ai", {})
    with st.sidebar:
        st.markdown("## Chat Assistente")
        st.caption(f"Attiva in tutte le pagine. Pagina corrente: {page_name}")

        if st.session_state.pop("global_chat_clear_text_next_run", False):
            st.session_state["global_chat_text"] = ""

        ready, msg = ai_agent.check_agent_ready(ai_cfg)
        if ready:
            st.success(msg)
        else:
            st.warning(msg)

        chat_date_iso = st.date_input(
            "Data operativa chat",
            value=engine.dt_now().date(),
            key="global_chat_date",
        ).isoformat()
        auto_apply = st.checkbox(
            "Applica automaticamente le azioni",
            value=True,
            key="global_chat_auto_apply",
        )

        pending = st.session_state.get("global_chat_pending")
        ctop1, ctop2 = st.columns(2)
        clear_chat = ctop1.button("Pulisci chat", key="global_chat_clear")
        apply_pending = ctop2.button(
            "Applica pendente",
            key="global_chat_apply_pending",
            disabled=not pending,
        )

        if clear_chat:
            st.session_state["global_chat_history"] = []
            st.session_state["global_chat_pending"] = None
            st.rerun()

        if apply_pending and pending:
            try:
                p_date = str(pending.get("date_iso", chat_date_iso))
                p_actions = pending.get("actions", []) or []
                p_day = engine.ensure_day(paths, p_date)
                messages, changed_cfg, changed_day = ai_agent.apply_actions(cfg, p_day, p_date, p_actions)
                if changed_cfg:
                    save_cfg()
                if changed_day:
                    engine.save_day(paths, p_date, p_day)
                _chat_add("assistant", "Azioni pendenti applicate:\n" + "\n".join(messages))
                st.session_state["global_chat_pending"] = None
                st.rerun()
            except Exception as e:
                _chat_add("assistant", f"Errore applicazione azioni pendenti: {e}")
                st.rerun()

        history = _chat_history()
        for m in history[-12:]:
            who = "Tu" if m.get("role") == "user" else "Bot"
            st.markdown(f"**{who}:** {m.get('text','')}")

        audio = st.audio_input("Parla al bot", key="global_chat_audio")
        text_cmd = st.text_input(
            "Scrivi al bot",
            key="global_chat_text",
            placeholder="Es: emetti 2 biglietti per evento ...",
        )
        send = st.button("Invia", key="global_chat_send")

        if send:
            prev_cmd_model = str(ai_cfg.get("command_model", ""))
            prev_stt_model = str(ai_cfg.get("transcribe_model", ""))
            try:
                spoken = ""
                if audio is not None and not text_cmd.strip():
                    audio_bytes = audio.getvalue()
                    if audio_bytes:
                        spoken = ai_agent.transcribe_audio(
                            audio_bytes,
                            getattr(audio, "name", "chat.wav"),
                            ai_cfg=ai_cfg,
                        )
                user_text = text_cmd.strip() or spoken.strip()
                if not user_text:
                    _chat_add("assistant", "Inserisci testo o registra audio.")
                else:
                    _chat_add("user", user_text)
                    if not ready:
                        _chat_add("assistant", f"Assistente non pronto: {msg}")
                    else:
                        day = engine.ensure_day(paths, chat_date_iso)
                        context = ai_agent.build_context(cfg, day, chat_date_iso, page_name=page_name)
                        parsed = ai_agent.parse_actions(user_text, context, ai_cfg=ai_cfg)
                        st.session_state["global_chat_last_parse"] = parsed
                        actions = parsed.get("actions", []) or []
                        missing = parsed.get("missing_fields", []) or []

                        if missing:
                            _chat_add("assistant", "Mi mancano alcuni dati: " + ", ".join([str(x) for x in missing]))
                        elif actions:
                            if auto_apply:
                                messages, changed_cfg, changed_day = ai_agent.apply_actions(cfg, day, chat_date_iso, actions)
                                if changed_cfg:
                                    save_cfg()
                                if changed_day:
                                    engine.save_day(paths, chat_date_iso, day)
                                _chat_add("assistant", "Operazione eseguita:\n" + "\n".join(messages))
                            else:
                                st.session_state["global_chat_pending"] = {
                                    "date_iso": chat_date_iso,
                                    "actions": actions,
                                }
                                _chat_add("assistant", f"Ho preparato {len(actions)} azioni. Premi 'Applica pendente'.")
                        else:
                            summary = str(parsed.get("summary", "") or "").strip()
                            _chat_add(
                                "assistant",
                                summary or "Non ho trovato azioni operative. Riformula in modo più specifico.",
                            )
            except Exception as e:
                _chat_add("assistant", f"Errore: {e}")
            finally:
                changed_models = (
                    str(ai_cfg.get("command_model", "")) != prev_cmd_model
                    or str(ai_cfg.get("transcribe_model", "")) != prev_stt_model
                )
                if changed_models:
                    save_cfg()
                st.session_state["global_chat_clear_text_next_run"] = True
                st.rerun()

st.title("Biglietterie – Web UI v7")

pages = ['Sorgenti + Import', 'Dati di riferimento', 'Anagrafica', 'Carte', 'Eventi (wizard)', 'Abbonamenti (wizard)', 'Giornata (wizard)', 'Assistente AI (voce)', 'Export']
page = st.radio("Navigazione", pages, horizontal=True, label_visibility="collapsed")

with st.expander("⚙️ Impostazioni", expanded=False):
    if st.button("RESET GLOBALE (config + tutti i giornali)"):
        engine.reset_config(paths)
        if paths.journal_dir.exists():
            for p in paths.journal_dir.glob("*.yml"):
                p.unlink()
        st.success("Reset globale completato.")
        st.rerun()

render_global_assistant(page)

# ----------------------------
# Template + Import

# ----------------------------
if page == "Sorgenti + Import":
    st.markdown("### Sorgenti XML + Import dataset")
    st.info(
        "Nessun upload template richiesto: il sistema usa automaticamente i file in ../dati "
        "(con fallback in templates/)."
    )

    src_log = engine.resolve_source_path(paths, "LOG")
    src_lta = engine.resolve_source_path(paths, "LTA")
    src_rca = engine.resolve_source_path(paths, "RCA")
    src_rpm = engine.resolve_source_path(paths, "RPM")
    xsd_log = engine.resolve_xsd_path(paths, "LOG")
    xsd_lta = engine.resolve_xsd_path(paths, "LTA")
    xsd_rca = engine.resolve_xsd_path(paths, "RCA")
    xsd_rpm = engine.resolve_xsd_path(paths, "RPM")

    st.json({
        "source_LOG": str(src_log) if src_log else None,
        "source_LTA": str(src_lta) if src_lta else None,
        "source_RCA": str(src_rca) if src_rca else None,
        "source_RPM": str(src_rpm) if src_rpm else None,
        "xsd_LOG": str(xsd_log) if xsd_log else None,
        "xsd_LTA": str(xsd_lta) if xsd_lta else None,
        "xsd_RCA": str(xsd_rca) if xsd_rca else None,
        "xsd_RPM": str(xsd_rpm) if xsd_rpm else None,
    })

    st.subheader("Upload file import (opzionale)")
    st.caption("Se carichi un file qui, l'import usa quello; altrimenti usa la sorgente automatica da ../dati.")
    u1, u2, u3, u4 = st.columns(4)
    with u1:
        up_log = st.file_uploader("LOG (xml/xsi/txt)", type=["xml", "xsi", "txt"], key="src_up_log")
    with u2:
        up_lta = st.file_uploader("LTA (xml/xsi/txt)", type=["xml", "xsi", "txt"], key="src_up_lta")
    with u3:
        up_rca = st.file_uploader("RCA (xml/xsi/txt)", type=["xml", "xsi", "txt"], key="src_up_rca")
    with u4:
        up_rpm = st.file_uploader("RPM (xml/xsi/txt)", type=["xml", "xsi", "txt"], key="src_up_rpm")

    log_bytes = up_log.getvalue() if up_log is not None else (src_log.read_bytes() if src_log is not None else None)
    lta_bytes = up_lta.getvalue() if up_lta is not None else (src_lta.read_bytes() if src_lta is not None else None)
    rca_bytes = up_rca.getvalue() if up_rca is not None else (src_rca.read_bytes() if src_rca is not None else None)
    rpm_bytes = up_rpm.getvalue() if up_rpm is not None else (src_rpm.read_bytes() if src_rpm is not None else None)

    st.caption(
        "Origine attiva: "
        f"LOG={'upload' if up_log else ('auto' if src_log else 'n.d.')}, "
        f"LTA={'upload' if up_lta else ('auto' if src_lta else 'n.d.')}, "
        f"RCA={'upload' if up_rca else ('auto' if src_rca else 'n.d.')}, "
        f"RPM={'upload' if up_rpm else ('auto' if src_rpm else 'n.d.')}"
    )

    st.divider()
    st.subheader("Import")
    colA,colB,colC = st.columns(3)
    with colA:
        import_cap = st.checkbox("Importa CAPENZE", value=True)
        fonte_cap = st.selectbox("Fonte capienza (default RPM)", ["RPM","RCA"], index=0)
    with colB:
        target_date = st.date_input("Data journal target", value=engine.dt_now().date()).isoformat()
        overwrite = st.checkbox("Sovrascrivi giornata", value=True)
    with colC:
        st.caption("Import LOG/LTA (facoltativo)")
        import_log = st.checkbox("Importa LOG", value=False, disabled=log_bytes is None)
        import_lta = st.checkbox("Importa LTA", value=False, disabled=lta_bytes is None)

    if st.button("ESEGUI IMPORT"):
        cfg2 = engine.ensure_config(paths)
        day = engine.reset_day(paths, target_date) if overwrite else engine.ensure_day(paths, target_date)

        # LOG/LTA import
        if import_log and log_bytes is not None:
            cfg2, dlog = engine.import_log(cfg2, log_bytes, target_date_iso=target_date)
            day["titoli"].extend(dlog.get("titoli", []))
            day["transazioni"].extend(dlog.get("transazioni", []))
        if import_lta and lta_bytes is not None:
            cfg2, dlta = engine.import_lta(cfg2, lta_bytes, target_date_iso=target_date)
            existing = {t.get("key") for t in day.get("titoli", [])}
            for t in dlta.get("titoli", []):
                if t.get("key") not in existing:
                    day["titoli"].append(t)

        # CAPENZE import
        if import_cap:
            if fonte_cap == "RPM":
                if rpm_bytes is not None:
                    capmap = engine.parse_capienza_from_rpm(rpm_bytes)
                    updated = engine.apply_capienza_to_cfg(cfg2, capmap)
                    st.info(f"Capienze aggiornate da RPM: {updated} settori.")
                else:
                    st.warning("Sorgente RPM non trovata.")
            else:
                if rca_bytes is not None:
                    capmap = engine.parse_capienza_from_rca(rca_bytes)
                    updated = engine.apply_capienza_to_cfg(cfg2, capmap)
                    st.info(f"Capienze aggiornate da RCA: {updated} settori.")
                else:
                    st.warning("Sorgente RCA non trovata.")

        engine.save_config(paths, cfg2)
        engine.save_day(paths, target_date, day)
        st.success("Import completato e salvato.")
        st.rerun()

# ----------------------------
# Dati di riferimento
# ----------------------------
elif page == "Dati di riferimento":
    st.markdown("### Valori vincolati caricati dagli allegati")
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Tab.2 Ordini di Posto")
        st.write([f'{x["code"]} - {x["desc"]}' for x in (REF.ordini_posto[:50] if REF.ordini_posto else [{"code":c,"desc":""} for c in ORDINI_CODES])])
        st.subheader("Tab.5 Causali annullamento")
        st.write([f'{x["code"]} - {x["desc"]}' for x in (REF.causali_ann if REF.causali_ann else [{"code":c,"desc":""} for c in CAUSALI_CODES])])
    with c2:
        st.subheader("Tab.3 Tipi Titolo/Abbonamento")
        st.write([f'{x["code"]} - {x["desc"]}' for x in (REF.tipi_titolo[:80] if REF.tipi_titolo else [{"code":c,"desc":""} for c in TIPI_CODES])])
        st.subheader("Aliquote Tab.1 (TipoGenere)")
        if not REF.aliquote.empty:
            st.dataframe(REF.aliquote[["Codice","Descrizione","IVA_raw","IVA_rates_%","ISI_raw","ISI_rates_%"]], use_container_width=True, height=350)
        else:
            st.info("aliquote_tab1.csv non disponibile (usa fallback).")

# ----------------------------
# Anagrafica
# ----------------------------
elif page == "Anagrafica":
    st.markdown("### Anagrafica & default")
    if st.button("Ripulisci Anagrafica"):
        engine.reset_section(cfg, "anagrafica")
        save_cfg()
        st.rerun()

    a = cfg["anagrafica"]
    d = cfg["defaults"]
    c1,c2 = st.columns(2)
    with c1:
        a["cf_organizzatore"] = st.text_input("CF Organizzatore", value=a.get("cf_organizzatore",""))
        a["cf_titolare"] = st.text_input("CF Titolare", value=a.get("cf_titolare",""))
        a["sistema_emissione"] = st.text_input("Sistema emissione", value=a.get("sistema_emissione",""))
        a["codice_richiedente_emissione_sigillo"] = st.text_input("CodiceRichiedenteEmissioneSigillo", value=a.get("codice_richiedente_emissione_sigillo",""))

        a["denominazione_titolare"] = st.text_input("Denominazione Titolare (RPM)", value=a.get("denominazione_titolare",""))
        a["denominazione_organizzatore"] = st.text_input("Denominazione Organizzatore (RPM)", value=a.get("denominazione_organizzatore",""))
        a["tipo_organizzatore"] = st.selectbox("TipoOrganizzatore (RPM)", ["G","S"], index=0 if str(a.get("tipo_organizzatore","G"))!="S" else 1)
    with c2:
        d["valuta"] = st.text_input("Valuta", value=d.get("valuta","EUR"))
        d["ivapreassolta_biglietto"] = st.selectbox("IVAPreassolta biglietto", ["N","B","S"], index=0)
        d["ivapreassolta_abbonamenti"] = st.selectbox("IVAPreassolta abbonamenti", ["B","N","S"], index=0)
        d["imponibile_intrattenimenti"] = st.text_input("ImponibileIntrattenimenti", value=str(d.get("imponibile_intrattenimenti","0")))
    if st.button("Salva"):
        save_cfg()
        st.success("Salvato.")

# ----------------------------
# Carte
# ----------------------------
elif page == "Carte":
    st.markdown("### Carte")
    if st.button("Ripulisci Carte"):
        engine.reset_section(cfg, "carte")
        save_cfg()
        st.rerun()

    with st.form("add_card"):
        carta = st.text_input("CartaAttivazione")
        prog = st.number_input("Progressivo next", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("Aggiungi/aggiorna")
        if submitted:
            engine.ensure_card(cfg, carta, int(prog))
            save_cfg()
            st.success("Carta salvata.")
            st.rerun()

    st.data_editor(
        cfg.get("carte", []),
        num_rows="dynamic",
        use_container_width=True,
        key="cards_table_editor",
    )

# ----------------------------
# Eventi wizard (controllato)
# ----------------------------
elif page == "Eventi (wizard)":
    st.markdown("### Eventi – inserimento controllato (TipoGenere/IVA/ISI da Tab.1, settori da Tab.2, TipoTitolo da Tab.3)")
    if st.button("Ripulisci Eventi"):
        engine.reset_section(cfg, "eventi")
        save_cfg()
        st.rerun()

    # ----- event create/update -----
    st.subheader("1) Crea/Aggiorna Evento")
    aliq_codes = list(REF.aliq_map.keys()) if REF.aliq_map else []
    if aliq_codes:
        label_map = {c: f"{c} - {REF.aliq_map[c].get('Descrizione','')}" for c in aliq_codes}
        code = st.selectbox("TipoGenere (Tab.1)", aliq_codes, format_func=lambda x: label_map.get(x,x))
        row = REF.aliq_map.get(str(code), {})
        iva_choices = [int(x) for x in str(row.get("IVA_rates_%","0")).split("|") if str(x).strip().isdigit()] or [0]
        isi_choices = []
        try:
            isi_val = row.get("ISI_rates_%","")
            if isi_val and isi_val not in ("nan","NaN"):
                # could be float string
                isi_choices = [int(float(isi_val))]
        except Exception:
            isi_choices = []
        if not isi_choices:
            isi_choices = [0]
    else:
        code = st.text_input("TipoGenere (Tab.1) - fallback", value="1")
        iva_choices=[10,22,0]
        isi_choices=[0]

    with st.form("event_form"):
        codice_locale = st.text_input("CodiceLocale")
        titolo = st.text_input("Titolo evento")
        d_evento = st.date_input("Data evento", value=engine.dt_now().date())
        t_evento = st.time_input("Ora evento", value=engine.dt_now().time().replace(second=0, microsecond=0))
        data_evento = d_evento.strftime("%Y%m%d")
        ora_evento = t_evento.strftime("%H%M")
        
        tipo_tass = st.selectbox("TipoTassazione", ["S","I"], index=0)
        iva_pct = st.selectbox("IVA % (da Tab.1)", iva_choices, index=0)
        isi_pct = st.selectbox("ISI % (da Tab.1)", isi_choices, index=0)
        settore = st.selectbox("Settore/CodiceOrdine (Tab.2)", ORDINI_CODES, index=ORDINI_CODES.index("UN") if "UN" in ORDINI_CODES else 0)
        cap = st.number_input("Capienza settore", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Salva evento + settore")
        if submitted:
            eid = engine.make_event_id(codice_locale, data_evento, ora_evento, titolo)
            ev = None
            for e in cfg.get("eventi", []):
                if e.get("id")==eid:
                    ev = e; break
            if ev is None:
                ev = {"id": eid, "settori": []}
                cfg.setdefault("eventi", []).append(ev)
            ev.update({
                "id": eid,
                "codice_locale": codice_locale,
                "titolo_evento": titolo,
                "tipo_genere": str(code),
                "data_evento": data_evento,
                "ora_evento": ora_evento,
                "data_apertura": data_evento,
                "ora_apertura": ora_evento,
                "tipo_tassazione": tipo_tass,
                "iva_percent": int(iva_pct),
                "isi_percent": int(isi_pct),
            })
            sec = engine.ensure_sector(ev, settore)
            sec["capienza"] = int(cap)
            sec.setdefault("prezzi", {})
            save_cfg()
            st.success("Evento salvato.")
            st.rerun()

    # ----- price create/update -----
    st.divider()
    
    st.divider()
    st.subheader("1b) Settori evento (modificabili)")
    if cfg.get("eventi"):
        ev_id_sect = st.selectbox("Evento per settori", [e["id"] for e in cfg["eventi"]], key="sect_evt")
        ev_sect = engine.find_event(cfg, ev_id_sect)
        # table view/edit
        current = []
        for s in (ev_sect.get("settori") or []):
            current.append({"codice_ordine": str(s.get("codice_ordine","")), "capienza": int(s.get("capienza",0) or 0)})
        edited = st.data_editor(
            current,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "codice_ordine": st.column_config.SelectboxColumn("CodiceOrdine (Tab.2)", options=ORDINI_CODES),
                "capienza": st.column_config.NumberColumn("Capienza", min_value=0, step=1),
            },
            key="sect_editor_tbl",
        )
        if st.button("Salva settori", key="save_sectors_btn"):
            # preserve prezzi for existing sectors
            old_map = {str(s.get("codice_ordine")): s for s in (ev_sect.get("settori") or [])}
            new_settori = []
            for row in edited:
                code = str(row.get("codice_ordine","")).strip()
                if not code:
                    continue
                if code not in ORDINI_CODES:
                    st.warning(f"CodiceOrdine non valido (Tab.2): {code}")
                    continue
                old = old_map.get(code, {"codice_ordine": code, "prezzi": {}})
                new_settori.append({
                    "codice_ordine": code,
                    "capienza": int(row.get("capienza",0) or 0),
                    "prezzi": old.get("prezzi", {}) or {},
                })
            ev_sect["settori"] = new_settori
            save_cfg()
            st.success("Settori salvati.")
            st.rerun()
    
    st.subheader("2) Aggiungi/Aggiorna Prezzo (per settore)")
    if cfg.get("eventi"):
        ev_id = st.selectbox("Evento", [e["id"] for e in cfg["eventi"]])
        ev = engine.find_event(cfg, ev_id)
        settori = [s.get("codice_ordine") for s in (ev.get("settori") or [])] or ORDINI_CODES
        cod_ord = st.selectbox("Settore", settori)
        with st.form("price_form"):
            price_key = st.text_input("Chiave prezzo (es. intero, ridotto, omaggio)")
            tipo_titolo = st.selectbox("TipoTitolo (Tab.3)", TIPI_CODES, index=0)
            corrisp = st.text_input("Corrispettivo € (lordo)", value="0.00")
            prev = st.text_input("Prevendita € (lordo)", value="0.00")
            iva_pct = st.number_input("IVA %", min_value=0, max_value=100, value=int(ev.get("iva_percent",0) or 0), step=1)
            causale = st.text_input("Causale (Transazione) (opzionale)", value="")
            submitted = st.form_submit_button("Salva prezzo")
            if submitted:
                engine.add_or_update_price(cfg, ev_id, cod_ord, price_key, {
                    "tipo_titolo": tipo_titolo,
                    "corrispettivo_eur": corrisp,
                    "prevendita_eur": prev,
                    "iva_percent": int(iva_pct),
                    "causale": causale,
                })
                save_cfg()
                st.success("Prezzo salvato.")
                st.rerun()
    
        st.subheader("Prezzi settore (modificabili)")
        sec_tbl = engine.ensure_sector(ev, cod_ord)
        prezzi_dict = sec_tbl.get("prezzi", {}) or {}
        rows = []
        for k, v in prezzi_dict.items():
            if not isinstance(v, dict):
                continue
            rows.append({
                "key": k,
                "tipo_titolo": str(v.get("tipo_titolo","")),
                "corrispettivo_eur": str(v.get("corrispettivo_eur","0.00")),
                "prevendita_eur": str(v.get("prevendita_eur","0.00")),
                "iva_percent": int(v.get("iva_percent", ev.get("iva_percent",0)) or 0),
                "causale": str(v.get("causale","") or ""),
            })
        edited_prices = st.data_editor(
            rows,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "key": st.column_config.TextColumn("Chiave"),
                "tipo_titolo": st.column_config.SelectboxColumn("TipoTitolo (Tab.3)", options=TIPI_CODES),
                "iva_percent": st.column_config.NumberColumn("IVA %", min_value=0, max_value=100, step=1),
            },
            key="price_table_editor",
        )
        if st.button("Salva prezzi settore", key="save_prices_btn"):
            new_dict = {}
            for r in edited_prices:
                k = str(r.get("key","")).strip()
                if not k:
                    continue
                new_dict[k] = {
                    "tipo_titolo": str(r.get("tipo_titolo","")),
                    "corrispettivo_eur": str(r.get("corrispettivo_eur","0.00")),
                    "prevendita_eur": str(r.get("prevendita_eur","0.00")),
                    "iva_percent": int(r.get("iva_percent",0) or 0),
                    "causale": str(r.get("causale","") or ""),
                }
            sec_tbl["prezzi"] = new_dict
            save_cfg()
            st.success("Prezzi aggiornati.")
            st.rerun()

    else:
        st.info("Crea prima un evento.")

    st.divider()
    st.subheader("Editor tabellare eventi (avanzato)")
    st.data_editor(
        cfg.get("eventi", []),
        num_rows="dynamic",
        use_container_width=True,
        key="events_table_editor",
    )

# ----------------------------
# Abbonamenti wizard
# ----------------------------
elif page == "Abbonamenti (wizard)":
    st.markdown("### Abbonamenti (prodotti) – inserimento controllato")
    if st.button("Ripulisci Abbonamenti"):
        engine.reset_section(cfg, "abbonamenti_prodotti")
        save_cfg()
        st.rerun()

    with st.form("ab_form"):
        codice = st.text_input("CodiceAbbonamento")
        turno = st.selectbox("Turno", ["L","F"], index=0)
        tipo_tass = st.selectbox("TipoTassazione", ["S","I"], index=0)
        d_valid = st.date_input("Validità", value=engine.dt_now().date())
        validita = d_valid.strftime("%Y%m%d")
        codice_ordine = st.selectbox("CodiceOrdine (Tab.2)", ORDINI_CODES, index=ORDINI_CODES.index("UN") if "UN" in ORDINI_CODES else 0)
        tipo_titolo = st.selectbox("TipoTitolo (Tab.3)", TIPI_CODES, index=0)
        q_eventi = st.number_input("Q eventi abilitati", min_value=1, value=1, step=1)
        corr = st.text_input("Corrispettivo € (lordo)", value="0.00")
        prev = st.text_input("Prevendita € (lordo)", value="0.00")
        iva_pct = st.number_input("IVA %", min_value=0, max_value=100, value=10, step=1)
        prog_next = st.number_input("ProgressivoAbbonamento next", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("Salva prodotto")
        if submitted:
            engine.add_or_update_abbonamento(cfg, {
                "codice_abbonamento": codice,
                "turno": turno,
                "tipo_tassazione": tipo_tass,
                "validita": validita,
                "codice_ordine": codice_ordine,
                "tipo_titolo": tipo_titolo,
                "q_eventi_abilitati": int(q_eventi),
                "corrispettivo_eur": corr,
                "prevendita_eur": prev,
                "iva_percent": int(iva_pct),
                "progressivo_next": int(prog_next),
            })
            save_cfg()
            st.success("Prodotto abbonamento salvato.")
            st.rerun()

    st.divider()
    st.subheader("Editor tabellare (avanzato)")
    st.data_editor(
        cfg.get("abbonamenti_prodotti", []),
        num_rows="dynamic",
        use_container_width=True,
        key="subs_products_table_editor",
    )

# ----------------------------
# Giornata wizard
# ----------------------------
elif page == "Giornata (wizard)":
    st.markdown("### Giornata – emissione guidata con dropdown controllati")
    date_iso = st.date_input("Data", value=engine.dt_now().date()).isoformat()
    day = engine.ensure_day(paths, date_iso)

    if st.button("Ripulisci Giornata"):
        day = engine.reset_day(paths, date_iso)
        st.rerun()

    if not cfg.get("carte"):
        st.warning("Configura almeno una Carta.")
    if not cfg.get("eventi"):
        st.warning("Configura almeno un Evento.")

    tabs = st.tabs(["Emetti biglietti", "Emetti biglietti abbonamento", "Vendi abbonamenti", "Annulla / Accessi / Blocchi", "Dati (tabellare)"])

    # Ticket
    with tabs[0]:
        if cfg.get("eventi") and cfg.get("carte"):
            with st.form("wiz_ticket"):
                event_id = st.selectbox("Evento", [e["id"] for e in cfg["eventi"]])
                ev = engine.find_event(cfg, event_id)
                settori = [s.get("codice_ordine") for s in (ev.get("settori") or [])] or ORDINI_CODES
                cod_ord = st.selectbox("Settore", settori)
                sec = engine.ensure_sector(ev, cod_ord)
                prezzi = list((sec.get("prezzi") or {}).keys())
                if not prezzi:
                    st.warning("Questo settore non ha prezzi: aggiungili in Eventi (wizard).")
                    prezzi = ["(nessuno)"]
                price_key = st.selectbox("Prezzo", prezzi)
                carta = st.selectbox("CartaAttivazione", [c["carta_attivazione"] for c in cfg["carte"]])
                supporto = st.selectbox("Supporto", ["BT","PH"], index=0)
                quantita = st.number_input("Quantità", min_value=1, value=1, step=1)
                t_em = st.time_input("Ora emissione", value=engine.dt_now().time().replace(second=0, microsecond=0))
                ora_em = t_em.strftime("%H%M")
                submitted = st.form_submit_button("Emetti")
                if submitted:
                    if price_key == "(nessuno)":
                        st.error("Manca un prezzo.")
                    else:
                        engine.issue_ticket(cfg, day, date_iso, event_id, cod_ord, price_key, carta, int(quantita), supporto, ora_em)
                        engine.save_config(paths, cfg)
                        engine.save_day(paths, date_iso, day)
                        st.success("Biglietti emessi.")
                        st.rerun()

    # Biglietto Abbonamento
    with tabs[1]:
        if cfg.get("eventi") and cfg.get("carte"):
            with st.form("wiz_ba"):
                event_id = st.selectbox("Evento", [e["id"] for e in cfg["eventi"]], key="ba_evt")
                ev = engine.find_event(cfg, event_id)
                settori = [s.get("codice_ordine") for s in (ev.get("settori") or [])] or ORDINI_CODES
                cod_ord = st.selectbox("Settore", settori, key="ba_ord")
                tipo_titolo = st.selectbox("TipoTitolo (Tab.3)", TIPI_CODES, key="ba_tt")
                carta = st.selectbox("CartaAttivazione", [c["carta_attivazione"] for c in cfg["carte"]], key="ba_card")
                supporto = st.selectbox("Supporto", ["BT","PH"], index=0, key="ba_sup")
                quantita = st.number_input("Quantità", min_value=1, value=1, step=1, key="ba_q")
                t_em = st.time_input("Ora emissione", value=engine.dt_now().time().replace(second=0, microsecond=0), key="ba_ora_t")
                ora_em = t_em.strftime("%H%M")
                ab_emessi = load_abbonamenti_emessi("L")
                if not ab_emessi:
                    st.warning("Nessun abbonamento TURNO LIBERO (L) emesso nei journal: vendi prima l'abbonamento (tab 'Vendi abbonamenti').")
                scelta = st.selectbox("Abbonamento (solo turno libero)", ["(manuale)"] + [x["label"] for x in ab_emessi], key="ba_sel")
                if scelta != "(manuale)":
                    sel = next(x for x in ab_emessi if x["label"] == scelta)
                    codabb = sel["codice_abbonamento"]
                    progabb = sel["progressivo_abbonamento"]
                else:
                    codabb = st.selectbox("CodiceAbbonamento (solo prodotti turno libero)", 
                                          [a["codice_abbonamento"] for a in cfg.get("abbonamenti_prodotti", []) if str(a.get("turno","")).upper()=="L"] or [""],
                                          key="ba_cod")
                    progabb = st.number_input("ProgressivoAbbonamento (esistente)", min_value=1, value=1, step=1, key="ba_prog")
                cfabb = st.text_input("CF Abbonamento", value=cfg["anagrafica"].get("cf_titolare",""), key="ba_cf")
                submitted = st.form_submit_button("Emetti biglietti abbonamento")
                if submitted:
                    engine.issue_biglietto_abbonamento(cfg, day, date_iso, event_id, cod_ord, tipo_titolo, carta, int(quantita), supporto, ora_em, codabb, cfabb, progressivo_abbonamento=int(progabb))
                    engine.save_config(paths, cfg)
                    engine.save_day(paths, date_iso, day)
                    st.success("Biglietti abbonamento emessi.")
                    st.rerun()

    # Abbonamenti vendita
    with tabs[2]:
        if cfg.get("abbonamenti_prodotti") and cfg.get("carte"):
            with st.form("wiz_sell_ab"):
                codabb = st.selectbox("CodiceAbbonamento", sorted(list({a["codice_abbonamento"] for a in cfg["abbonamenti_prodotti"]})))
                turno_sel = st.selectbox("Turno (L=libero, F=fisso)", ["L","F"], index=0)
                carta = st.selectbox("CartaAttivazione", [c["carta_attivazione"] for c in cfg["carte"]])
                quantita = st.number_input("Quantità", min_value=1, value=1, step=1)
                t_em = st.time_input("Ora emissione", value=engine.dt_now().time().replace(second=0, microsecond=0))
                ora_em = t_em.strftime("%H%M")
                submitted = st.form_submit_button("Vendi")
                if submitted:
                    engine.sell_abbonamento(cfg, day, date_iso, codabb, turno_sel, carta, int(quantita), ora_em)
                    engine.save_config(paths, cfg)
                    engine.save_day(paths, date_iso, day)
                    st.success("Abbonamenti venduti.")
                    st.rerun()
        else:
            st.info("Configura prima prodotti abbonamento e carte.")

    # Annulla / Accessi / Blocchi
    with tabs[3]:
        titles = [t for t in (day.get("titoli", []) or []) if t.get("key")]
        if not titles:
            st.info("Nessun titolo nella giornata.")
        else:
            emessi_keys = [t["key"] for t in titles if (not engine.title_is_annulled(t)) and (not engine.title_is_transited(t))]
            transitati_keys = [t["key"] for t in titles if engine.title_is_transited(t)]
            annullati_keys = [t["key"] for t in titles if engine.title_is_annulled(t)]
            transitabili_keys = [t["key"] for t in titles if engine.title_can_transit(t)]
            annullabili_keys = [t["key"] for t in titles if engine.title_can_cancel(t)]
            bloccabili_keys = [t["key"] for t in titles if engine.title_can_block(t)]

            st.caption(
                f"Emessi attivi: {len(emessi_keys)} | Transitati: {len(transitati_keys)} | "
                f"Annullati: {len(annullati_keys)} | Transitabili: {len(transitabili_keys)}"
            )
            blacklist_keys = [t["key"] for t in titles if engine.title_is_blocked(t)]
            st.table([
                {"Stato": "Emessi", "Totale": len(emessi_keys)},
                {"Stato": "Transitati", "Totale": len(transitati_keys)},
                {"Stato": "Annullati", "Totale": len(annullati_keys)},
                {"Stato": "Blacklist", "Totale": len(blacklist_keys)},
            ])

            col1,col2 = st.columns(2)
            with col1:
                st.subheader("Annulla biglietto (Tab.5)")
                if not annullabili_keys:
                    st.info("Nessun titolo annullabile (esclusi già annullati o già transitati).")
                else:
                    with st.form("wiz_ann"):
                        titolo_key = st.selectbox("Titolo", annullabili_keys)
                        caus = st.selectbox("CausaleAnnullamento", CAUSALI_CODES, index=0)
                        carta_ann = st.selectbox("Carta per annullamento", [c["carta_attivazione"] for c in cfg.get("carte", [])])
                        submitted = st.form_submit_button("Annulla")
                        if submitted:
                            engine.cancel_ticket(cfg, day, date_iso, titolo_key, caus, carta_ann)
                            engine.save_config(paths, cfg)
                            engine.save_day(paths, date_iso, day)
                            st.success("Annullamento registrato.")
                            st.rerun()

            with col2:
                st.subheader("Accessi / Blocchi")
                if not transitabili_keys:
                    st.info("Nessun titolo transitabile (esclusi annullati, transitati o in blacklist).")
                else:
                    with st.form("wiz_access"):
                        titolo_key = st.selectbox("Titolo", transitabili_keys, key="acc_k")
                        d_acc = st.date_input("Data ingresso", value=engine.dt_now().date(), key="acc_date")
                        t_acc = st.time_input("Ora ingresso", value=engine.dt_now().time().replace(second=0, microsecond=0), key="acc_time")
                        ts = f"{d_acc.isoformat()}T{t_acc.strftime('%H:%M:%S')}"
                        mode = st.selectbox("Modalità accesso", ["AUTO","MAN"])
                        submitted = st.form_submit_button("Registra accesso")
                        if submitted:
                            engine.record_access(day, titolo_key, ts, mode)
                            engine.save_day(paths, date_iso, day)
                            st.success("Accesso registrato.")
                            st.rerun()

                if not bloccabili_keys:
                    st.info("Nessun titolo bloccabile (esclusi annullati o transitati).")
                else:
                    with st.form("wiz_block"):
                        titolo_key = st.selectbox("Titolo", bloccabili_keys, key="blk_k")
                        kind = st.selectbox("Tipo blocco", ["BL","DASPO","RUBATO"])
                        submitted = st.form_submit_button("Applica blocco")
                        if submitted:
                            engine.set_block_status(day, titolo_key, kind)
                            engine.save_day(paths, date_iso, day)
                            st.success("Blocco applicato.")
                            st.rerun()

    # Raw data
    with tabs[4]:
        st.subheader("Titoli (LTA source)")
        tit = st.data_editor(
            day.get("titoli", []),
            num_rows="dynamic",
            use_container_width=True,
            key="day_titles_table_editor",
        )
        st.subheader("Transazioni (LOG source)")
        tx = st.data_editor(
            day.get("transazioni", []),
            num_rows="dynamic",
            use_container_width=True,
            key="day_transactions_table_editor",
        )
        if st.button("Salva dati tabellari"):
            day["titoli"] = tit
            day["transazioni"] = tx
            engine.save_day(paths, date_iso, day)
            st.success("Salvato.")
            st.rerun()

# ----------------------------
# Assistente AI (voce)
# ----------------------------
elif page == "Assistente AI (voce)":
    st.markdown("### Assistente AI (voce + testo)")
    st.caption("Detta o scrivi un comando operativo: l'agente propone azioni e le applica dopo conferma.")

    date_iso = st.date_input("Data operativa", value=engine.dt_now().date(), key="ai_date").isoformat()
    day = engine.ensure_day(paths, date_iso)

    ai_cfg = cfg.setdefault("ai", {})

    st.markdown("#### Configurazione Provider")
    c0, c1, c2 = st.columns(3)
    with c0:
        if st.button("Preset LocalAI", key="ai_preset_localai"):
            ai_cfg.update({
                "provider": "localai",
                "base_url": "http://localai:8080/v1",
                "api_key": "localai",
                "command_model": "llama-3.2-3b-instruct:q4_k_m",
                "transcribe_model": "whisper-1",
            })
            save_cfg()
            st.rerun()
    with c1:
        if st.button("Preset vLLM", key="ai_preset_vllm"):
            ai_cfg.update({
                "provider": "vllm",
                "base_url": "http://vllm:8000/v1",
                "api_key": "vllm",
                "command_model": "Qwen/Qwen2.5-7B-Instruct",
                "transcribe_model": "whisper-1",
            })
            save_cfg()
            st.rerun()
    with c2:
        if st.button("Preset OpenAI", key="ai_preset_openai"):
            ai_cfg.update({
                "provider": "openai",
                "base_url": "",
                "api_key": "",
                "command_model": "gpt-4.1-mini",
                "transcribe_model": "gpt-4o-mini-transcribe",
            })
            save_cfg()
            st.rerun()

    with st.form("ai_config_form"):
        ai_cfg["provider"] = st.selectbox(
            "Provider",
            ["localai", "vllm", "openai"],
            index=["localai", "vllm", "openai"].index(str(ai_cfg.get("provider", "localai")).lower())
            if str(ai_cfg.get("provider", "localai")).lower() in ("localai", "vllm", "openai")
            else 0,
        )
        ai_cfg["base_url"] = st.text_input("Base URL API", value=str(ai_cfg.get("base_url", "")))
        ai_cfg["api_key"] = st.text_input("API Key", value=str(ai_cfg.get("api_key", "")), type="password")
        ai_cfg["command_model"] = st.text_input("Modello comandi", value=str(ai_cfg.get("command_model", "")))
        ai_cfg["transcribe_model"] = st.text_input("Modello trascrizione", value=str(ai_cfg.get("transcribe_model", "")))
        if st.form_submit_button("Salva configurazione AI"):
            save_cfg()
            st.success("Configurazione AI salvata.")
            st.rerun()

    resolved = ai_agent.resolve_ai_config(ai_cfg)
    st.code(
        f"provider={resolved['provider']}  base_url={resolved['base_url'] or '(default OpenAI)'}  "
        f"command_model={resolved['command_model']}  transcribe_model={resolved['transcribe_model']}",
        language="text",
    )

    ready, msg = ai_agent.check_agent_ready(ai_cfg)
    if ready:
        st.success(msg)
    else:
        st.warning(msg)

    col_test, _ = st.columns([1, 3])
    with col_test:
        if st.button("Test connessione AI", key="ai_test_conn", disabled=not ready):
            try:
                with st.spinner("Verifica endpoint e modelli..."):
                    models = ai_agent.list_models(ai_cfg)
                if models:
                    st.success(f"Connessione OK. Modelli: {', '.join(models[:8])}")
                else:
                    st.warning("Connessione OK ma nessun modello elencato da /models.")
            except Exception as e:
                st.error(str(e))

    if resolved["provider"] == "localai":
        st.markdown("#### Tooling LocalAI (gallery)")
        st.caption("Primo download modelli: può richiedere diversi minuti.")
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            if st.button("Installa modello comandi", key="ai_install_cmd_model"):
                try:
                    out = ai_agent.localai_install_model(ai_cfg, resolved["command_model"])
                    st.success(f"Install richiesta: {out}")
                except Exception as e:
                    st.error(str(e))
        with col_i2:
            if st.button("Installa modello trascrizione", key="ai_install_stt_model"):
                try:
                    out = ai_agent.localai_install_model(ai_cfg, resolved["transcribe_model"])
                    st.success(f"Install richiesta: {out}")
                except Exception as e:
                    st.error(str(e))

        search_q = st.text_input("Cerca modello in gallery", value="llama-3.2-3b")
        if st.button("Cerca in gallery", key="ai_search_gallery_btn"):
            try:
                with st.spinner("Ricerca in corso..."):
                    hits = ai_agent.localai_search_gallery_models(ai_cfg, search_q, limit=30)
                st.session_state["ai_gallery_hits"] = hits
            except Exception as e:
                st.error(str(e))
        hits = st.session_state.get("ai_gallery_hits", [])
        if hits:
            st.write(hits)

        job_ref = st.text_input("Job URL/ID (opzionale) per stato install", value="")
        if st.button("Controlla job install", key="ai_check_job_btn"):
            if not job_ref.strip():
                st.warning("Inserisci job URL o ID.")
            else:
                try:
                    st.json(ai_agent.localai_get_job(ai_cfg, job_ref.strip()))
                except Exception as e:
                    st.error(str(e))

    st.markdown("Esempi:")
    st.code(
        "Crea evento Teatro Roma domani alle 21:00 codice locale RM01 settore PL capienza 200 iva 10 e genere 1",
        language="text",
    )
    st.code(
        "Emetti 3 biglietti evento RM01_20260320_2100_Teatro_Roma settore PL prezzo intero carta CARD01",
        language="text",
    )
    st.code(
        "Vendi 2 abbonamenti ABB01 turno libero carta CARD01 adesso",
        language="text",
    )

    audio = st.audio_input("Comando vocale", key="ai_audio")
    text_cmd = st.text_area("Comando testuale (opzionale)", key="ai_text_cmd", height=120)

    if st.button("Analizza comando", key="ai_analyze_btn", disabled=not ready):
        prev_cmd_model = str(ai_cfg.get("command_model", ""))
        prev_stt_model = str(ai_cfg.get("transcribe_model", ""))
        try:
            spoken = ""
            if audio is not None:
                audio_bytes = audio.getvalue()
                if audio_bytes:
                    with st.spinner("Trascrizione audio in corso..."):
                        spoken = ai_agent.transcribe_audio(audio_bytes, getattr(audio, "name", "comando.wav"), ai_cfg=ai_cfg)

            command_text = text_cmd.strip() or spoken.strip()
            if not command_text:
                st.error("Nessun comando rilevato. Inserisci testo o registra audio.")
            else:
                with st.spinner("Interpretazione comando in corso..."):
                    context = ai_agent.build_context(cfg, day, date_iso, page_name=page)
                    parsed = ai_agent.parse_actions(command_text, context, ai_cfg=ai_cfg)
                st.session_state["ai_last_command_text"] = command_text
                st.session_state["ai_last_parse"] = parsed
        except Exception as e:
            st.error(str(e))
        finally:
            changed = (
                str(ai_cfg.get("command_model", "")) != prev_cmd_model
                or str(ai_cfg.get("transcribe_model", "")) != prev_stt_model
            )
            if changed:
                save_cfg()
                st.info(
                    f"Config AI aggiornata automaticamente: "
                    f"command_model={ai_cfg.get('command_model','')} "
                    f"transcribe_model={ai_cfg.get('transcribe_model','')}"
                )

    last_text = st.session_state.get("ai_last_command_text", "")
    parsed = st.session_state.get("ai_last_parse")

    if last_text:
        st.text_area("Comando interpretato", value=last_text, height=100, disabled=True, key="ai_last_text_area")
    if parsed:
        st.subheader("Piano azioni")
        st.json(parsed)
        missing = parsed.get("missing_fields", []) or []
        actions = parsed.get("actions", []) or []
        if missing:
            st.warning("Campi mancanti/ambigui: " + ", ".join([str(x) for x in missing]))
        if actions and st.button("Applica azioni", type="primary", key="ai_apply_btn"):
            try:
                messages, changed_cfg, changed_day = ai_agent.apply_actions(cfg, day, date_iso, actions)
                if changed_cfg:
                    engine.save_config(paths, cfg)
                if changed_day:
                    engine.save_day(paths, date_iso, day)
                for m in messages:
                    st.success(m)
                st.rerun()
            except Exception as e:
                st.error(str(e))

# ----------------------------
# Export
# ----------------------------
elif page == "Export":
    st.markdown("### Export file (LOG/LTA giornalieri + RPM mensile)")
    src_log = engine.resolve_source_path(paths, "LOG")
    src_lta = engine.resolve_source_path(paths, "LTA")
    src_rpm = engine.resolve_source_path(paths, "RPM")

    # --- Daily export (LOG/LTA) ---
    st.subheader("Giornaliero: LOG + LTA")
    ok_daily = (src_log is not None) and (src_lta is not None)
    if not ok_daily:
        st.warning("Sorgenti LOG/LTA non trovate (usa file in ../dati o fallback templates/).")

    date_iso = st.date_input("Data export (giornaliero)", value=engine.dt_now().date()).isoformat()
    day = engine.ensure_day(paths, date_iso)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Genera LOG", disabled=not ok_daily):
            try:
                xml = engine.export_log(paths, cfg, day)
                st.download_button(
                    "Scarica LOG",
                    data=xml,
                    file_name=f"LOG_{date_iso.replace('-','_')}_001.xml",
                    mime="application/xml",
                )
            except Exception as e:
                st.error(str(e))
    with col2:
        if st.button("Genera LTA", disabled=not ok_daily):
            try:
                xml = engine.export_lta(paths, cfg, day)
                st.download_button(
                    "Scarica LTA",
                    data=xml,
                    file_name=f"LTA_{date_iso.replace('-','_')}_001.xml",
                    mime="application/xml",
                )
            except Exception as e:
                st.error(str(e))

    if st.button("ZIP (LOG+LTA)", disabled=not ok_daily):
        try:
            logb = engine.export_log(paths, cfg, day)
            ltab = engine.export_lta(paths, cfg, day)
            stamp = date_iso.replace("-", "_")
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr(f"LOG_{stamp}_001.xml", logb)
                z.writestr(f"LTA_{stamp}_001.xml", ltab)
            buf.seek(0)
            st.download_button(
                "Scarica ZIP giornaliero",
                data=buf.getvalue(),
                file_name=f"export_giornaliero_{stamp}.zip",
                mime="application/zip",
            )
        except Exception as e:
            st.error(str(e))

    st.divider()

    # --- Monthly export (RPM) ---
    st.subheader("Mensile: RPM (RiepilogoMensile)")
    ok_rpm = src_rpm is not None
    if not ok_rpm:
        st.warning("Sorgente RPM non trovata (usa file in ../dati o fallback templates/).")

    # Scegli un giorno del mese (usato solo per selezionare il mese)
    date_month = st.date_input("Mese RPM (scegli una data del mese)", value=engine.dt_now().date(), key="rpm_month")
    month_yyyymm = date_month.strftime("%Y%m")

    colA, colB, colC = st.columns(3)
    with colA:
        sostituzione = st.selectbox("Sostituzione", ["S", "N"], index=0)
    with colB:
        progressivo = st.number_input("ProgressivoGenerazione", min_value=1, value=1, step=1)
    with colC:
        st.caption("Include tutti i journal del mese selezionato (data/journal/*.yml).")

    if st.button("Genera RPM", disabled=not ok_rpm):
        try:
            xml = engine.export_rpm(paths, cfg, month_yyyymm, int(progressivo), sostituzione)
            st.download_button(
                "Scarica RPM",
                data=xml,
                file_name=f"RPM_{month_yyyymm[:4]}_{month_yyyymm[4:6]}_00_{int(progressivo):03d}.xml",
                mime="application/xml",
            )
        except Exception as e:
            st.error(str(e))

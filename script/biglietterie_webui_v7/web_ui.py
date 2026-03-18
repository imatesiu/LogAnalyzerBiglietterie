
import io
import zipfile
from pathlib import Path
import streamlit as st
import yaml

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

st.title("Biglietterie – Web UI v7")

pages = ['Template + Import', 'Dati di riferimento', 'Anagrafica', 'Carte', 'Eventi (wizard)', 'Abbonamenti (wizard)', 'Giornata (wizard)', 'Export']
page = st.radio("Navigazione", pages, horizontal=True, label_visibility="collapsed")

with st.expander("⚙️ Impostazioni", expanded=False):
    if st.button("RESET GLOBALE (config + tutti i giornali)"):
        engine.reset_config(paths)
        if paths.journal_dir.exists():
            for p in paths.journal_dir.glob("*.yml"):
                p.unlink()
        st.success("Reset globale completato.")
        st.rerun()

# ----------------------------
# Template + Import

# ----------------------------
if page == "Template + Import":
    st.markdown("### Template XML + Import dataset")
    st.info("Carica qui LOG/LTA/RCA/RPM. Verranno salvati in templates/.")

    c1,c2,c3,c4 = st.columns(4)
    with c1: up_log = st.file_uploader("LOG_template.xml", type=["xml","xsi"])
    with c2: up_lta = st.file_uploader("LTA_template.xml", type=["xml","xsi"])
    with c3: up_rca = st.file_uploader("RCA_template.xml", type=["xml","xsi"])
    with c4: up_rpm = st.file_uploader("RPM_template.xml", type=["xml","xsi"])

    if st.button("Salva template caricati"):
        paths.templates_dir.mkdir(parents=True, exist_ok=True)
        if up_log: paths.templ_log.write_bytes(up_log.getvalue())
        if up_lta: paths.templ_lta.write_bytes(up_lta.getvalue())
        if up_rca: paths.templ_rca.write_bytes(up_rca.getvalue())
        if up_rpm: paths.templ_rpm.write_bytes(up_rpm.getvalue())
        st.success("Template salvati.")
        st.rerun()

    st.json({
        "LOG_template.xml": file_present(paths.templ_log),
        "LTA_template.xml": file_present(paths.templ_lta),
        "RCA_template.xml": file_present(paths.templ_rca),
        "RPM_template.xml": file_present(paths.templ_rpm),
    })

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
        import_log = st.checkbox("Importa LOG", value=False, disabled=not file_present(paths.templ_log))
        import_lta = st.checkbox("Importa LTA", value=False, disabled=not file_present(paths.templ_lta))

    if st.button("ESEGUI IMPORT"):
        cfg2 = engine.ensure_config(paths)
        day = engine.reset_day(paths, target_date) if overwrite else engine.ensure_day(paths, target_date)

        # LOG/LTA import
        if import_log and file_present(paths.templ_log):
            cfg2, dlog = engine.import_log(cfg2, paths.templ_log.read_bytes(), target_date_iso=target_date)
            day["titoli"].extend(dlog.get("titoli", []))
            day["transazioni"].extend(dlog.get("transazioni", []))
        if import_lta and file_present(paths.templ_lta):
            cfg2, dlta = engine.import_lta(cfg2, paths.templ_lta.read_bytes(), target_date_iso=target_date)
            existing = {t.get("key") for t in day.get("titoli", [])}
            for t in dlta.get("titoli", []):
                if t.get("key") not in existing:
                    day["titoli"].append(t)

        # CAPENZE import
        if import_cap:
            if fonte_cap == "RPM":
                if file_present(paths.templ_rpm):
                    capmap = engine.parse_capienza_from_rpm(paths.templ_rpm.read_bytes())
                    updated = engine.apply_capienza_to_cfg(cfg2, capmap)
                    st.info(f"Capienze aggiornate da RPM: {updated} settori.")
                else:
                    st.warning("RPM_template.xml mancante.")
            else:
                if file_present(paths.templ_rca):
                    capmap = engine.parse_capienza_from_rca(paths.templ_rca.read_bytes())
                    updated = engine.apply_capienza_to_cfg(cfg2, capmap)
                    st.info(f"Capienze aggiornate da RCA: {updated} settori.")
                else:
                    st.warning("RCA_template.xml mancante.")

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

    st.data_editor(cfg.get("carte", []), num_rows="dynamic", use_container_width=True)

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
    st.data_editor(cfg.get("eventi", []), num_rows="dynamic", use_container_width=True)

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
    st.data_editor(cfg.get("abbonamenti_prodotti", []), num_rows="dynamic", use_container_width=True)

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
        keys = [t.get("key") for t in day.get("titoli", []) if t.get("key")]
        if not keys:
            st.info("Nessun titolo nella giornata.")
        else:
            col1,col2 = st.columns(2)
            with col1:
                st.subheader("Annulla biglietto (Tab.5)")
                with st.form("wiz_ann"):
                    titolo_key = st.selectbox("Titolo", keys)
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
                with st.form("wiz_access"):
                    titolo_key = st.selectbox("Titolo", keys, key="acc_k")
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

                with st.form("wiz_block"):
                    titolo_key = st.selectbox("Titolo", keys, key="blk_k")
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
        tit = st.data_editor(day.get("titoli", []), num_rows="dynamic", use_container_width=True)
        st.subheader("Transazioni (LOG source)")
        tx = st.data_editor(day.get("transazioni", []), num_rows="dynamic", use_container_width=True)
        if st.button("Salva dati tabellari"):
            day["titoli"] = tit
            day["transazioni"] = tx
            engine.save_day(paths, date_iso, day)
            st.success("Salvato.")
            st.rerun()

# ----------------------------
# Export
# ----------------------------
elif page == "Export":
    st.markdown("### Export file (LOG/LTA giornalieri + RPM mensile)")

    # --- Daily export (LOG/LTA) ---
    st.subheader("Giornaliero: LOG + LTA")
    ok_daily = file_present(paths.templ_log) and file_present(paths.templ_lta)
    if not ok_daily:
        st.warning("Carica LOG_template.xml e LTA_template.xml in Template + Import.")

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
    ok_rpm = file_present(paths.templ_rpm)
    if not ok_rpm:
        st.warning("Carica RPM_template.xml in Template + Import (puoi usare i tuoi esempi come template).")

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

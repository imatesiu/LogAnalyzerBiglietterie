# Biglietterie Web UI v7 (Streamlit)

Novità:
- Wizard con dropdown controllati per:
  - Emetti biglietti
  - Emetti biglietti abbonamento
  - Vendi abbonamenti
  - Annulla (causali da Tab.5)
  - Accessi + blocchi
- Import capienze da RPM (default) o RCA (opzione)
- Valori vincolati caricati dagli allegati:
  - Tab.2 Ordini di Posto (settori)
  - Tab.3 Tipi Titolo/Abbonamento
  - Tab.5 Causale annullamento
  - aliquote_tab1.csv (Tipo evento/TipoGenere + IVA + ISI)

## Avvio
```bash
pip install -r requirements.txt
streamlit run web_ui.py
```

## Assistente AI (voce + testo)
La UI include la pagina `Assistente AI (voce)` per inserimento rapido dati con comando naturale.
In più, la chat assistente è sempre disponibile in **sidebar** in ogni pagina (testo + voce) e può applicare automaticamente le azioni.

Setup rapido (locale con LocalAI):
```bash
docker compose up --build
```

Uso:
- usa la chat in sidebar da qualunque pagina
- apri pagina `Assistente AI (voce)`
- premi `Preset LocalAI` nella configurazione provider
- premi `Installa modello comandi` e `Installa modello trascrizione` (solo prima volta)
- usa `Test connessione AI` per verificare i modelli disponibili
- registra audio o scrivi comando (es. crea evento, emetti biglietti, vendi abbonamenti, annulla, accessi/blocchi)
- clicca `Analizza comando`
- controlla il JSON proposto e clicca `Applica azioni`

Note:
- provider supportati: `localai`, `vllm`, `openai` (switch da UI)
- modelli/configurazione AI sono salvati in `data/config.yml` (`ai.*`)
- stack Docker di default espone solo la WebUI (`8501`); LocalAI resta su rete interna compose
- se vuoi usare OpenAI cloud, imposta provider `openai` e API key dalla UI
- per vLLM (server GPU), avvia anche il profilo:
```bash
docker compose --profile vllm up --build
```
poi in UI usa `Preset vLLM` e `Base URL` `http://vllm:8000/v1`

## Avvio con Docker
```bash
docker build -t biglietterie-webui-v7 .
docker run --rm -p 8501:8501 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/reference:/app/reference" \
  -v "$(pwd)/../dati:/app_ext/dati:ro" \
  -v "$(pwd)/xsd:/app/xsd:ro" \
  -v "$(pwd)/../../src/main/resources:/app_ext/resources:ro" \
  biglietterie-webui-v7
```

Oppure con Docker Compose:
```bash
docker compose up --build
```

## Cartelle
- `../dati/` : sorgenti XML/XSI usate automaticamente (LOG/LTA/RCA/RPM)
- `xsd/` : schemi XSD di riferimento
- `templates/` : fallback opzionale (non obbligatorio)
- `data/config.yml`
- `data/journal/YYYY-MM-DD.yml`
- `reference/` : copie locali degli allegati (se presenti)

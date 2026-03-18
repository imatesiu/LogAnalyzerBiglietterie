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

## Avvio con Docker
```bash
docker build -t biglietterie-webui-v7 .
docker run --rm -p 8501:8501 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/templates:/app/templates" \
  -v "$(pwd)/reference:/app/reference" \
  biglietterie-webui-v7
```

Oppure con Docker Compose:
```bash
docker compose up --build
```

## Cartelle
- `templates/` : carica LOG/LTA/RCA/RPM
- `data/config.yml`
- `data/journal/YYYY-MM-DD.yml`
- `reference/` : copie locali degli allegati (se presenti)

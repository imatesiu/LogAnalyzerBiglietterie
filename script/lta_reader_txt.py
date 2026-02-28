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
from collections import Counter
from typing import Dict, List, Optional, Tuple

# ============================================================
# SPEC UFFICIALE (Provv. AE 4 marzo 2008 - Allegato A - LTA TXT)
# Record a campi fissi: ultima posizione 513 (6 byte) => 518 char
# - A (alfanumerico): allineato a sinistra, riempito con blank
# - N (numerico): allineato a destra, riempito con zeri
# ============================================================
RECORD_LEN = 518

# (name, pos(1-index), length, type A/N)
FIELDS: List[Tuple[str, int, int, str]] = [
    # Dati identificativi (titolare + sistema CA + evento)
    ("CFTitolareCA", 1, 16, "A"),
    ("CodiceSistemaCA", 17, 8, "A"),
    ("CFOrganizzatore", 25, 16, "A"),
    ("CodiceLocale", 41, 13, "N"),
    ("DataEvento", 54, 8, "N"),         # AAAAMMGG
    ("OraEvento", 62, 4, "N"),          # HHMM
    ("TitoloEvento", 66, 40, "A"),
    ("TipoGenere", 106, 2, "A"),        # Tab. 1 provv AE 23/7/2001
    ("DataAperturaAccessi", 108, 8, "N"),   # AAAAMMGG
    ("OraAperturaAccessi", 116, 6, "N"),    # HHMMSS

    # Dati identificativi del titolo
    ("SistemaEmissione", 122, 8, "A"),
    ("CartaAttivazione", 130, 8, "A"),
    ("ProgressivoFiscale", 138, 8, "N"),
    ("SigilloFiscale", 146, 16, "A"),
    ("DataEmissione", 162, 8, "N"),     # AAAAMMGG
    ("OraEmissione", 170, 4, "N"),      # HHMM
    ("TipoTitolo", 174, 2, "A"),
    ("CorrispettivoLordo", 176, 9, "N"),  # importo comprensivo IVA (tipicamente in centesimi)
    ("CodiceOrdinePosto", 185, 2, "A"),
    ("IdentificativoPosto", 187, 6, "A"),

    # Ulteriori dati abbonamenti/biglietti abbonamento
    ("CFAbbonamento", 193, 16, "A"),
    ("CodiceAbbonamento", 209, 8, "A"),
    ("ProgressivoAbbonamento", 217, 8, "N"),
    ("QuantitaEventiAbilitati", 225, 4, "N"),

    # Dati per titoli annullati
    ("DataAnnullamento", 229, 8, "N"),      # AAAAMMGG
    ("OraAnnullamento", 237, 4, "N"),       # HHMM
    ("CartaAttivazioneANN", 241, 8, "A"),
    ("SigilloFiscaleANN", 249, 16, "A"),
    ("ProgressivoFiscaleANN", 265, 8, "N"),

    # Dati supporto identificazione
    ("CodSupportoId", 273, 2, "A"),         # Tabella A
    ("TipoSupportoId", 275, 32, "A"),       # descrizione
    ("IdSupporto", 307, 32, "A"),
    ("IdSupportoAlt", 339, 32, "A"),

    # Partecipante
    ("CognomePartecipante", 371, 40, "A"),
    ("NomePartecipante", 411, 30, "A"),
    ("DataNascitaPartecipante", 441, 8, "N"),   # AAAAMMGG
    ("LuogoNascitaPartecipante", 449, 40, "A"),

    # Gestione LTA + controllo accessi
    ("DataInserimentoLTA", 489, 8, "N"),    # AAAAMMGG
    ("OraInserimentoLTA", 497, 6, "N"),     # HHMMSS
    ("Stato", 503, 2, "A"),                 # VT/VD/ZT/...
    ("DataIngresso", 505, 8, "N"),          # AAAAMMGG
    ("OraIngresso", 513, 6, "N"),           # HHMMSS
]

# -------------------------
# Helpers: escaping + formatting
# -------------------------
def hattr(s: str) -> str:
    return html.escape(s or "", quote=True)

def fmt_date8(yyyymmdd: str) -> str:
    s = (yyyymmdd or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[6:8]}/{s[4:6]}/{s[0:4]}"
    return s

def fmt_time4(hhmm: str) -> str:
    s = (hhmm or "").strip()
    if len(s) == 4 and s.isdigit():
        return f"{s[:2]}:{s[2:]}"
    return s

def fmt_time6(hhmmss: str) -> str:
    s = (hhmmss or "").strip()
    if len(s) == 6 and s.isdigit():
        return f"{s[:2]}:{s[2:4]}:{s[4:]}"
    return s

def money_from_cents9(digits: str) -> str:
    s = (digits or "").strip()
    if not s or not s.isdigit():
        return ""
    n = int(s)
    amount = n / 100.0
    us = f"{amount:,.2f}"
    it = us.replace(",", "X").replace(".", ",").replace("X", ".")
    return it + " EUR"

def td(content: str, sort_key: Optional[str] = None) -> str:
    safe = content if content.startswith("<") else html.escape(content, quote=False)
    sk = sort_key if sort_key is not None else re.sub(r"<[^>]+>", "", safe).strip().lower()
    return f"<td data-sort=\"{hattr(sk)}\">{safe}</td>"

def th(label: str, dtype: str) -> str:
    return f"<th class=\"sortable\" data-type=\"{hattr(dtype)}\">{html.escape(label)}</th>"

# -------------------------
# Optional: P7M extraction (if TXT is signed)
# -------------------------
def looks_pem(path: str) -> bool:
    with open(path, "rb") as f:
        head = f.read(64)
    return b"-----BEGIN" in head

def extract_p7m_to_temp_file(p7m_path: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp_path = tmp.name
    tmp.close()

    inform = "PEM" if looks_pem(p7m_path) else "DER"

    # openssl cms
    try:
        subprocess.run(
            ["openssl", "cms", "-verify", "-noverify", "-inform", inform, "-in", p7m_path, "-out", tmp_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return tmp_path
    except Exception:
        pass

    # macOS security cms -D
    try:
        with open(tmp_path, "wb") as out:
            subprocess.run(
                ["/usr/bin/security", "cms", "-D", "-i", p7m_path],
                check=True, stdout=out, stderr=subprocess.DEVNULL
            )
        return tmp_path
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise RuntimeError("Impossibile estrarre payload dal .p7m (openssl e security falliti).")

# -------------------------
# Read file text
# -------------------------
def read_lines(path: str) -> List[str]:
    # utf-8 con fallback cp1252
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        with open(path, "r", encoding="cp1252", errors="replace") as f:
            return f.read().splitlines()

# -------------------------
# Parse one LTA record line (518 chars)
# -------------------------
def slice_1based(s: str, pos: int, length: int) -> str:
    return s[pos - 1 : pos - 1 + length]

def parse_record(raw: str) -> Dict[str, str]:
    r = raw.rstrip("\n")
    rec: Dict[str, str] = {"Raw": r, "Valid": "0"}

    if len(r) != RECORD_LEN:
        # se diverso da 518, lo teniamo comunque (viewer) ma marcato invalid
        rec["Len"] = str(len(r))
        return rec

    rec["Valid"] = "1"
    rec["Len"] = str(len(r))

    for name, pos, ln, typ in FIELDS:
        val = slice_1based(r, pos, ln)
        # strip coerente per viewer (manteniamo anche raw digits quando serve)
        rec[name] = val.rstrip() if typ == "A" else val.strip()

    return rec

# -------------------------
# Output naming + open
# -------------------------
def strip_ext_for_output(name: str) -> str:
    low = name.lower()
    if low.endswith(".p7m"):
        name = name[:-4]
        low = name.lower()
    for ext in (".txt", ".lta", ".csv"):
        if low.endswith(ext):
            name = name[: -len(ext)]
            low = name.lower()
    return name

def open_in_browser(path: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", path], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", path], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore

# -------------------------
# Build HTML viewer
# -------------------------
def build_html(records: List[Dict[str, str]], title: str) -> str:
    valid = [r for r in records if r.get("Valid") == "1"]
    invalid = [r for r in records if r.get("Valid") != "1"]

    stato_counts = Counter([r.get("Stato", "").strip() for r in valid if r.get("Stato", "").strip()])
    tot_corr = sum(int(r["CorrispettivoLordo"]) for r in valid if r.get("CorrispettivoLordo", "").isdigit())

    # tabella principale (campi più usati)
    headers = (
        "<tr>"
        + th("#", "num")
        + th("Data evento", "date")
        + th("Ora evento", "time")
        + th("Titolo evento", "text")
        + th("Genere", "text")
        + th("Locale", "text")
        + th("Tipo titolo", "text")
        + th("Corrispettivo", "money")
        + th("Ord/Posto", "text")
        + th("Stato", "text")
        + th("Ingresso", "date")
        + th("Ora ingr.", "time")
        + th("Partecipante", "text")
        + "</tr>"
    )

    rows_html: List[str] = []
    details_html: List[str] = []

    for i, r in enumerate(valid, start=1):
        de = r.get("DataEvento", "")
        oe = r.get("OraEvento", "")
        titolo = r.get("TitoloEvento", "")
        genere = r.get("TipoGenere", "")
        locale = r.get("CodiceLocale", "")
        tipo_tit = r.get("TipoTitolo", "")
        corr = r.get("CorrispettivoLordo", "")
        corr_fmt = money_from_cents9(corr)
        corr_sort = corr if corr.isdigit() else "0"

        ordp = r.get("CodiceOrdinePosto", "")
        posto = r.get("IdentificativoPosto", "")
        ord_posto = (ordp + " " + posto).strip()

        stato = r.get("Stato", "")
        di = r.get("DataIngresso", "")
        oi = r.get("OraIngresso", "")

        cogn = r.get("CognomePartecipante", "")
        nome = r.get("NomePartecipante", "")
        partecipante = (cogn + " " + nome).strip()

        # formatted
        de_f = fmt_date8(de)
        oe_f = fmt_time4(oe)
        di_f = fmt_date8(di)
        oi_f = fmt_time6(oi)

        # filtro: raw + formatted + altri id chiave
        filter_blob = " ".join([
            str(i),

            # eventi (raw+fmt)
            de, de_f, oe, oe_f,
            titolo, genere, locale,

            # accessi
            stato, di, di_f, oi, oi_f,

            # titolo/ordine/posto
            tipo_tit, ordp, posto,

            # emissione/identificativi
            r.get("CFTitolareCA",""),
            r.get("CodiceSistemaCA",""),
            r.get("CFOrganizzatore",""),
            r.get("SistemaEmissione",""),
            r.get("CartaAttivazione",""),
            r.get("ProgressivoFiscale",""),
            r.get("SigilloFiscale",""),
            r.get("DataEmissione",""), fmt_date8(r.get("DataEmissione","")),
            r.get("OraEmissione",""), fmt_time4(r.get("OraEmissione","")),

            # importi (raw+fmt)
            corr, corr_fmt,

            # annullamento
            r.get("DataAnnullamento",""), fmt_date8(r.get("DataAnnullamento","")),
            r.get("OraAnnullamento",""), fmt_time4(r.get("OraAnnullamento","")),
            r.get("CartaAttivazioneANN",""),
            r.get("SigilloFiscaleANN",""),
            r.get("ProgressivoFiscaleANN",""),

            # abbonamenti
            r.get("CFAbbonamento",""),
            r.get("CodiceAbbonamento",""),
            r.get("ProgressivoAbbonamento",""),
            r.get("QuantitaEventiAbilitati",""),

            # supporto
            r.get("CodSupportoId",""),
            r.get("TipoSupportoId",""),
            r.get("IdSupporto",""),
            r.get("IdSupportoAlt",""),

            # partecipante
            cogn, nome, r.get("DataNascitaPartecipante",""), r.get("LuogoNascitaPartecipante",""),

            # gestione LTA
            r.get("DataInserimentoLTA",""), fmt_date8(r.get("DataInserimentoLTA","")),
            r.get("OraInserimentoLTA",""), fmt_time6(r.get("OraInserimentoLTA","")),

            # raw
            r.get("Raw",""),
        ]).lower()

        rows_html.append(
            f"<tr class=\"row\" data-filter=\"{hattr(filter_blob)}\" data-idx=\"{i}\">"
            + td(str(i), str(i))
            + td(de_f, de)
            + td(oe_f, oe)
            + td(titolo, titolo.lower())
            + td(genere, genere.lower())
            + td(locale, locale)
            + td(tipo_tit, tipo_tit.lower())
            + td(corr_fmt, corr_sort)
            + td(ord_posto, ord_posto.lower())
            + td(stato, stato.lower())
            + td(di_f, di)
            + td(oi_f, oi)
            + td(partecipante, partecipante.lower())
            + "</tr>"
        )

        # dettaglio: tutte le colonne (spec)
        kv_rows = []
        def kv(k: str, v: str):
            if (v or "").strip() != "":
                kv_rows.append(f"<tr><td><b>{html.escape(k)}</b></td><td>{html.escape(v)}</td></tr>")

        for name, _, _, _ in FIELDS:
            v = r.get(name, "")
            # piccoli "pretty" per alcuni campi
            if name in ("DataEvento","DataAperturaAccessi","DataEmissione","DataAnnullamento","DataNascitaPartecipante",
                        "DataInserimentoLTA","DataIngresso"):
                if v:
                    kv(name, f"{v} ({fmt_date8(v)})")
                continue
            if name in ("OraEvento","OraEmissione","OraAnnullamento"):
                if v:
                    kv(name, f"{v} ({fmt_time4(v)})")
                continue
            if name in ("OraAperturaAccessi","OraInserimentoLTA","OraIngresso"):
                if v:
                    kv(name, f"{v} ({fmt_time6(v)})")
                continue
            if name == "CorrispettivoLordo":
                if v:
                    kv(name, f"{v} ({money_from_cents9(v)})")
                continue
            kv(name, v)

        details_html.append(f"""
        <details class="rec" data-filter="{hattr(filter_blob)}" data-idx="{i}">
          <summary>{html.escape(de_f)} {html.escape(oe_f)} — {html.escape(titolo)} — {html.escape(stato)}</summary>
          <div class="pad">
            <table class="kv"><tbody>
              {''.join(kv_rows)}
            </tbody></table>
            <h4>Riga raw (518)</h4>
            <pre class="raw">{html.escape(r.get("Raw",""))}</pre>
          </div>
        </details>
        """)

    # header summary
    stato_list = ", ".join([f"{html.escape(k)}={v}" for k, v in stato_counts.most_common()]) or "n/d"

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    h1{margin:0 0 6px 0;}
    .muted{color:#666;font-size:13px;}
    .status{color:#666;font-size:12px;margin:6px 0;}
    input{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:10px 0;}
    .tablewrap{max-height:55vh;overflow:auto;border:1px solid #eee;border-radius:12px;}
    table{border-collapse:collapse;width:100%;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap;}
    th{background:#fafafa;font-weight:700;position:sticky;top:0;z-index:2;}
    .sortable{cursor:pointer;user-select:none;}
    .sortable:after{content:" ↕";color:#bbb;font-weight:600;}
    .sorted-asc:after{content:" ↑";color:#444;}
    .sorted-desc:after{content:" ↓";color:#444;}
    details{border:1px solid #eee;border-radius:10px;padding:8px 10px;margin-top:10px;background:#fcfcfc;}
    summary{cursor:pointer;font-weight:600;}
    .pad{padding:8px 2px 2px 2px;}
    .kv td{white-space:normal;}
    .kv td:first-child{width:320px;}
    pre.raw{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid #eee;border-radius:10px;padding:10px;}
    .bad{color:#8a1f1f;}
    """

    js = """
    function norm(s){ return (s||"").toString().toLowerCase(); }

    function applyFilter(){
      const qraw = norm(document.getElementById('q').value).trim();
      const toks = qraw.split(/\\s+/).filter(Boolean);

      const rows = document.querySelectorAll('#tb tr.row');
      const dets = document.querySelectorAll('details.rec');

      let shown = 0;
      const match = (el) => {
        const hay = norm(el.getAttribute('data-filter'));
        for(const t of toks){
          if(!hay.includes(t)) return false;
        }
        return true;
      };

      rows.forEach(r=>{
        const ok = match(r);
        r.style.display = ok ? "" : "none";
        if(ok) shown++;
      });

      dets.forEach(d=>{
        d.style.display = match(d) ? "" : "none";
      });

      const st = document.getElementById('status');
      st.textContent = toks.length ? `Mostrate: ${shown} / ${rows.length}` : `Totale: ${rows.length}`;
    }

    function clearSortStyles(table){
      table.querySelectorAll('th.sortable').forEach(th=>{
        th.classList.remove('sorted-asc','sorted-desc');
      });
    }

    function sortTableByCol(colIndex, type, asc){
      const table = document.getElementById('t');
      const tbody = document.getElementById('tb');
      const rows = Array.from(tbody.querySelectorAll('tr'));

      const getKey = (tr) => {
        const td = tr.children[colIndex];
        return td ? (td.getAttribute('data-sort') || td.textContent || "") : "";
      };

      const cmp = (a,b) => {
        const ka = getKey(a);
        const kb = getKey(b);
        if(['num','money','date','time'].includes(type)){
          const na = parseFloat(ka) || 0;
          const nb = parseFloat(kb) || 0;
          return na - nb;
        }
        return ka.localeCompare(kb, undefined, {numeric:true, sensitivity:'base'});
      };

      rows.sort((a,b)=> asc ? cmp(a,b) : -cmp(a,b));
      rows.forEach(r=>tbody.appendChild(r));

      clearSortStyles(table);
      const th = table.querySelectorAll('th.sortable')[colIndex];
      if(th) th.classList.add(asc ? 'sorted-asc' : 'sorted-desc');
    }

    function initSorting(){
      const table = document.getElementById('t');
      table.querySelectorAll('th.sortable').forEach((th, idx)=>{
        th.addEventListener('click', ()=>{
          const type = th.getAttribute('data-type') || 'text';
          const asc = !th.classList.contains('sorted-asc');
          sortTableByCol(idx, type, asc);
        });
      });
    }

    function init(){
      document.getElementById('q').addEventListener('input', applyFilter);
      initSorting();
      applyFilter();
    }

    if(document.readyState === 'loading'){
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
    """

    invalid_note = ""
    if invalid:
        invalid_note = f"<div class='status bad'>Record NON conformi (len != 518): {len(invalid)} (visualizzati solo nel dettaglio raw)</div>"

    html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>LTA Reader</title>
<style>{css}</style>
</head>
<body>
  <h1>LTA Reader (TXT a campi fissi)</h1>
  <div class="muted">{html.escape(title)}</div>

  <div class="status">
    Record validi (518): <b>{len(valid)}</b> — Totale corrispettivo: <b>{html.escape(money_from_cents9(str(tot_corr)))}</b><br/>
    Stati: {stato_list}
  </div>
  {invalid_note}

  <input id="q" placeholder="Cerca (es: 25/02/2026 21:00 CALCIO P0002267 A0141197 VT 129,00) ..." />
  <div id="status" class="status"></div>

  <div class="tablewrap">
    <table id="t">
      <thead>{headers}</thead>
      <tbody id="tb">
        {''.join(rows_html)}
      </tbody>
    </table>
  </div>

  <h2>Dettaglio record</h2>
  {''.join(details_html)}

  {"<h2>Record non validi (raw)</h2>" if invalid else ""}
  {"".join(f"<pre class='raw'>{html.escape(x.get('Raw',''))}</pre>" for x in invalid) if invalid else ""}

<script>{js}</script>
</body>
</html>
"""
    return html_doc


# -------------------------
# CLI
# -------------------------
def main():
    ap = argparse.ArgumentParser(description="LTA TXT Reader: viewer HTML con parsing da specifica ufficiale.")
    ap.add_argument("files", nargs="+", help="File LTA .txt (o .p7m se firmato)")
    ap.add_argument("--open", action="store_true", help="Apri il report nel browser")
    args = ap.parse_args()

    for in_path in args.files:
        p = pathlib.Path(in_path)
        if not p.exists():
            print(f"SKIP: non trovato: {in_path}", file=sys.stderr)
            continue

        actual_path = str(p)
        temp_to_cleanup = None

        if p.name.lower().endswith(".p7m"):
            temp_to_cleanup = extract_p7m_to_temp_file(str(p))
            actual_path = temp_to_cleanup

        lines = read_lines(actual_path)
        records: List[Dict[str, str]] = []
        for ln in lines:
            if not ln.strip():
                continue
            records.append(parse_record(ln))

        out_base = strip_ext_for_output(p.name)
        out_path = str(p.with_name(out_base + ".lta.html"))

        doc = build_html(records, p.name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(doc)

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

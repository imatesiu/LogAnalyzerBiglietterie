#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import uuid
import shutil
import html
import tempfile
import subprocess
import pathlib
import xml.etree.ElementTree as ET
from typing import Optional, Dict, List, Tuple

from flask import Flask, request, redirect, url_for, send_file, render_template_string, abort

# lxml per XSD
from lxml import etree

APP_DIR = pathlib.Path(__file__).resolve().parent
UPLOAD_ROOT = APP_DIR / "uploads"
UPLOAD_ROOT.mkdir(exist_ok=True)

XSD_DIR = APP_DIR / "xsd"

RPM_SCRIPT = APP_DIR / "rpm_reader.py"
RCA_SCRIPT = APP_DIR / "accessi_reader.py"
LTA_SCRIPT = APP_DIR / "lta_reader.py"
LOG_SCRIPT = APP_DIR / "log_reader.py"

MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# TLS per avvio dev con python app.py (in docker si usa gunicorn)
TLS_CERT_PATH = os.environ.get("TLS_CERT_PATH", str(APP_DIR / "tls" / "fullchain.pem"))
TLS_KEY_PATH = os.environ.get("TLS_KEY_PATH", str(APP_DIR / "tls" / "key.pem"))
USE_HTTPS = os.environ.get("USE_HTTPS", "1")  # "1"=https se cert/key esistono

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# -------------------------
# XML helpers
# -------------------------
def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag and "}" in tag else (tag or "")

def detect_root_tag(xml_path: pathlib.Path) -> str:
    root = ET.parse(str(xml_path)).getroot()
    return localname(root.tag)

# mapping root->xsd filename (autodetect)
ROOT_TO_XSD = {
    "RiepilogoMensile": "RiepilogoMensile.xsd",
    "LogTransazione": "logTransazioni.xsd",
    # il tuo file si chiama riepilogogionaliero.xsd (typo incluso)
    "RiepilogoGiornaliero": "riepilogogionaliero.xsd",
    # questi dipendono dal tag root effettivo; li lasciamo come tentativi
    "Accessi": "accessi.xsd",
    "LTA": "lta.xsd",
}

def list_xsds() -> List[str]:
    if not XSD_DIR.exists():
        return []
    return sorted([p.name for p in XSD_DIR.glob("*.xsd")])


# -------------------------
# P7M helpers (estrazione + verifica firma)
# -------------------------
def looks_pem(path: pathlib.Path) -> bool:
    with path.open("rb") as f:
        head = f.read(64)
    return b"-----BEGIN" in head

def openssl_verify_and_extract(p7m_path: pathlib.Path, out_xml: pathlib.Path) -> Tuple[bool, str]:
    """
    Verifica firma (criptografica) e contemporaneamente estrae payload in out_xml.
    Nota: -noverify = non verifica la catena/certificato rispetto a CA; verifica solo la firma.
    """
    inform = "PEM" if looks_pem(p7m_path) else "DER"
    cp = subprocess.run(
        ["openssl", "cms", "-verify", "-noverify", "-inform", inform, "-in", str(p7m_path), "-out", str(out_xml)],
        capture_output=True,
        text=True,
    )
    ok = (cp.returncode == 0)
    # openssl scrive spesso dettagli su stderr
    msg = (cp.stderr or cp.stdout or "").strip()
    if not msg:
        msg = "Verification successful" if ok else "Verification failed"
    return ok, msg

def extract_p7m_noverify(p7m_path: pathlib.Path) -> pathlib.Path:
    """
    Estrazione payload (noverify) per rilevare tipo.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
    tmp_path = pathlib.Path(tmp.name)
    tmp.close()

    inform = "PEM" if looks_pem(p7m_path) else "DER"
    try:
        subprocess.run(
            ["openssl", "cms", "-verify", "-noverify", "-inform", inform, "-in", str(p7m_path), "-out", str(tmp_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return tmp_path
    except Exception:
        # fallback macOS
        try:
            with tmp_path.open("wb") as out:
                subprocess.run(
                    ["/usr/bin/security", "cms", "-D", "-i", str(p7m_path)],
                    check=True,
                    stdout=out,
                    stderr=subprocess.DEVNULL,
                )
            return tmp_path
        except Exception:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
            raise RuntimeError("Impossibile estrarre il contenuto dal .p7m (openssl e security falliti).")


# -------------------------
# Detect kind: rpm vs log vs generic xml
# -------------------------
def detect_kind_from_root(root_tag: str) -> str:
    if root_tag == "RiepilogoMensile":
        return "rpm"
    if root_tag == "LogTransazione":
        return "log"
    if root_tag == "LTA_Giornaliera":
        return "lta"
    if root_tag == "RiepilogoControlloAccessi":
        return "rca"
    return "xml"  # generic

def detect_kind(upload_path: pathlib.Path) -> Tuple[str, str]:
    """
    returns (kind, root_tag)
    kind in: rpm|log|xml
    """
    if upload_path.name.lower().endswith(".p7m"):
        tmp = extract_p7m_noverify(upload_path)
        try:
            root_tag = detect_root_tag(tmp)
            return detect_kind_from_root(root_tag), root_tag
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
    root_tag = detect_root_tag(upload_path)
    return detect_kind_from_root(root_tag), root_tag


# -------------------------
# Output naming like readers
# -------------------------
def strip_ext_for_output(name: str) -> str:
    low = name.lower()
    if low.endswith(".p7m"):
        name = name[:-4]
        low = name.lower()
    if low.endswith(".xml") or low.endswith(".xsi"):
        name = name[:-4]
    return name


# -------------------------
# Run reader script (RPM/LOG)
# -------------------------
def run_reader(kind: str, in_file: pathlib.Path, no_cents: bool) -> pathlib.Path:
    if kind == "rpm":
        script = RPM_SCRIPT
        out_suffix = ".rpm.html"
    elif kind == "log":
        script = LOG_SCRIPT
        out_suffix = ".log.html"
    elif kind=="lta":
        script = LTA_SCRIPT
        out_suffix = ".lta.html"
    elif kind=="rca":
        script = RCA_SCRIPT
        out_suffix = ".rca.html"
    else:
        raise RuntimeError("run_reader chiamato su tipo non RPM/LOG")

    if not script.exists():
        raise RuntimeError(f"Script mancante: {script.name}")

    cmd = [sys.executable, str(script), str(in_file)]
    if no_cents:
        cmd.append("--no-cents")

    subprocess.run(cmd, check=True)

    base = strip_ext_for_output(in_file.name)
    out_path = in_file.with_name(base + out_suffix)
    if out_path.exists():
        return out_path

    # fallback: ultimo html nella cartella run
    htmls = sorted(in_file.parent.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    if htmls:
        return htmls[0]
    raise RuntimeError("Lo script ha terminato ma non trovo l'HTML di output.")


# -------------------------
# XML pretty view (per xml generici)
# -------------------------
def make_pretty_xml_html(xml_path: pathlib.Path, title: str) -> str:
    try:
        parser = etree.XMLParser(remove_blank_text=True, huge_tree=True)
        doc = etree.parse(str(xml_path), parser)
        pretty = etree.tostring(doc, pretty_print=True, encoding="utf-8").decode("utf-8", errors="replace")
    except Exception as e:
        pretty = f"Impossibile fare pretty print: {e}\n\nContenuto grezzo non mostrato."
    safe = html.escape(pretty)
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;margin:18px;}}
pre{{white-space:pre-wrap;word-break:break-word;background:#f7f7f7;border:1px solid #e5e5e5;border-radius:10px;padding:12px;}}
</style></head>
<body>
<h2>{html.escape(title)}</h2>
<pre>{safe}</pre>
</body></html>
"""


# -------------------------
# XSD validation
# -------------------------
def pick_xsd_for_root(root_tag: str) -> Optional[pathlib.Path]:
    fname = ROOT_TO_XSD.get(root_tag)
    if not fname:
        return None
    p = XSD_DIR / fname
    return p if p.exists() else None

def validate_xml_with_xsd(xml_path: pathlib.Path, xsd_path: pathlib.Path) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Returns ok + list of error dicts.
    """
    # Parser con base_url per risolvere include/import relativi
    xsd_doc = etree.parse(str(xsd_path))
    schema = etree.XMLSchema(xsd_doc)

    parser = etree.XMLParser(huge_tree=True)
    xml_doc = etree.parse(str(xml_path), parser)

    ok = schema.validate(xml_doc)
    errors: List[Dict[str, str]] = []
    if not ok:
        for e in schema.error_log:
            errors.append({
                "line": str(e.line),
                "column": str(e.column),
                "level": e.level_name,
                "type": e.type_name,
                "domain": e.domain_name,
                "message": e.message,
            })
    return ok, errors


# -------------------------
# Meta persistence
# -------------------------
def write_meta(run_dir: pathlib.Path, meta: Dict) -> None:
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def read_meta(run_dir: pathlib.Path) -> Dict:
    p = run_dir / "meta.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


# -------------------------
# UI templates
# -------------------------
INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>RPM/LOG/XML Viewer</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;max-width:900px;}
    input[type=file]{margin-top:8px;}
    button{margin-top:12px;padding:10px 14px;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer;}
    .muted{color:#666;font-size:13px;margin-top:8px;}
    label{display:flex;gap:10px;align-items:center;margin-top:10px;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;}
  </style>
</head>
<body>
  <h1>RPM / LOG / XML Viewer</h1>
  <div class="card">
    <form action="/upload" method="post" enctype="multipart/form-data">
      <div><b>Carica un file</b> RPM/LOG o un XML coperto dagli XSD (anche <code>.p7m</code>)</div>
      <input type="file" name="file" required />

      <label>
        <input type="checkbox" name="no_cents" />
        Non dividere per 100 gli importi (<code>--no-cents</code>) per i report RPM/LOG
      </label>

      <button type="submit">Carica</button>

      <div class="muted">
        Autodetect:
        <code>RiepilogoMensile</code> → RPM,
        <code>LogTransazione</code> → LOG,
        altro → XML (solo visualizzazione + validazione).
      </div>
    </form>
  </div>
</body>
</html>
"""

VIEW_WRAPPER_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Viewer</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;color:#111;}
    .bar{display:flex;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid #e5e5e5;position:sticky;top:0;background:#fff;z-index:10;}
    .btn{padding:8px 12px;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer;text-decoration:none;color:#111;}
    .btn:hover{background:#f2f2f2;}
    .sp{flex:1;}
    .meta{color:#666;font-size:13px;}
    iframe{width:100%;height:calc(100vh - 56px);border:0;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;}
  </style>
</head>
<body>
  <div class="bar">
    <a class="btn" href="/">Nuovo upload</a>
    <a class="btn" href="{{ validate_url }}">Validazione (XSD / Firma)</a>
    <a class="btn" href="{{ download_url }}">Download HTML</a>
    <div class="sp"></div>
    <div class="meta">
      <b>{{ filename }}</b> — tipo: <code>{{ kind }}</code> — root: <code>{{ root_tag }}</code>
      {% if is_p7m %} — <code>p7m</code>{% endif %}
    </div>
  </div>
  <iframe src="{{ content_url }}"></iframe>
</body>
</html>
"""

VALIDATION_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Validazione</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    .row{display:flex;gap:12px;flex-wrap:wrap;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;min-width:320px;flex:1;}
    .ok{color:#0b6b2f;font-weight:700;}
    .bad{color:#8a1f1f;font-weight:700;}
    table{border-collapse:collapse;width:100%;margin-top:10px;font-size:13px;}
    th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;vertical-align:top;}
    th{background:#fafafa;font-weight:700;}
    .muted{color:#666;font-size:13px;}
    .btn{display:inline-block;margin-right:8px;padding:8px 12px;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer;text-decoration:none;color:#111;}
    .btn:hover{background:#f2f2f2;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;}
    select{padding:8px 10px;border:1px solid #ddd;border-radius:10px;}
    button{padding:8px 12px;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer;}
  </style>
</head>
<body>
  <div style="margin-bottom:12px;">
    <a class="btn" href="{{ view_url }}">← Torna al report</a>
    <a class="btn" href="/">Nuovo upload</a>
  </div>

  <h1>Validazione (XSD / Firma)</h1>
  <div class="muted">
    File: <b>{{ filename }}</b> — root: <code>{{ root_tag }}</code> {% if is_p7m %} — <code>p7m</code>{% endif %}
  </div>

  <div class="row" style="margin-top:14px;">
    <div class="card">
      <h2>Verifica firma</h2>
      {% if not is_p7m %}
        <div class="muted">N/A (file non firmato .p7m)</div>
      {% else %}
        {% if sig_ok %}
          <div class="ok">OK</div>
        {% else %}
          <div class="bad">INSUCCESSO</div>
        {% endif %}
        <div class="muted" style="margin-top:8px;">
          Nota: la verifica usa <code>openssl cms -verify -noverify</code> (firma valida, catena certificati non verificata).
        </div>
        <pre style="white-space:pre-wrap;margin-top:10px;background:#f7f7f7;border:1px solid #eee;border-radius:10px;padding:10px;">{{ sig_msg }}</pre>
      {% endif %}
    </div>

    <div class="card">
      <h2>Validazione XSD</h2>

      <form method="get" action="{{ validate_url }}">
        <label class="muted">Schema:</label>
        <select name="schema">
          <option value="auto" {% if schema_sel == "auto" %}selected{% endif %}>auto (da root tag)</option>
          {% for x in xsds %}
            <option value="{{ x }}" {% if schema_sel == x %}selected{% endif %}>{{ x }}</option>
          {% endfor %}
        </select>
        <button type="submit">Valida</button>
      </form>

      <div class="muted" style="margin-top:8px;">
        Usato: <code>{{ schema_used }}</code>
      </div>

      {% if xsd_ok %}
        <div class="ok" style="margin-top:10px;">OK (conforme allo schema)</div>
      {% else %}
        <div class="bad" style="margin-top:10px;">NON CONFORME</div>
        {% if xsd_errors %}
          <table>
            <thead>
              <tr>
                <th>Linea</th><th>Col</th><th>Livello</th><th>Tipo</th><th>Messaggio</th>
              </tr>
            </thead>
            <tbody>
              {% for e in xsd_errors %}
              <tr>
                <td>{{ e.line }}</td>
                <td>{{ e.column }}</td>
                <td>{{ e.level }}</td>
                <td>{{ e.type }}</td>
                <td>{{ e.message }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        {% else %}
          <div class="muted" style="margin-top:10px;">Nessun dettaglio errori disponibile.</div>
        {% endif %}
      {% endif %}

      {% if xsd_note %}
        <div class="muted" style="margin-top:10px;">{{ xsd_note }}</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


# -------------------------
# Routes
# -------------------------
@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.post("/upload")
def upload():
    if "file" not in request.files:
        abort(400, "Nessun file inviato")

    f = request.files["file"]
    if not f.filename:
        abort(400, "Nome file mancante")

    run_id = uuid.uuid4().hex
    run_dir = UPLOAD_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", f.filename)
    in_path = run_dir / safe_name
    f.save(str(in_path))

    no_cents = request.form.get("no_cents") == "on"

    try:
        kind, root_tag = detect_kind(in_path)
        is_p7m = in_path.name.lower().endswith(".p7m")

        # Genera output.html:
        # - RPM/LOG: reader
        # - XML generico: pretty XML (estratto se p7m)
        if kind in ("rpm", "log", "lta", "rca"):
            out_html = run_reader(kind, in_path, no_cents=no_cents)
            shutil.copyfile(out_html, run_dir / "output.html")
        else:
            # xml generico
            if is_p7m:
                payload = run_dir / "payload.xml"
                # estrai (noverify) per render; la verifica "ufficiale" la fai su /validate
                tmp = extract_p7m_noverify(in_path)
                try:
                    shutil.copyfile(tmp, payload)
                finally:
                    try:
                        tmp.unlink(missing_ok=True)
                    except Exception:
                        pass
                html_doc = make_pretty_xml_html(payload, f"XML (da P7M): {safe_name}")
            else:
                html_doc = make_pretty_xml_html(in_path, f"XML: {safe_name}")

            (run_dir / "output.html").write_text(html_doc, encoding="utf-8")

        meta = {
            "filename": safe_name,
            "kind": kind,
            "root_tag": root_tag,
            "is_p7m": is_p7m,
            "no_cents": no_cents,
        }
        write_meta(run_dir, meta)

        return redirect(url_for("view", run_id=run_id))

    except subprocess.CalledProcessError as e:
        return f"<pre>Errore eseguendo lo script: {html.escape(str(e))}</pre>", 500
    except Exception as e:
        return f"<pre>Errore: {html.escape(str(e))}</pre>", 500


@app.get("/view/<run_id>")
def view(run_id: str):
    run_dir = UPLOAD_ROOT / run_id
    if not run_dir.exists():
        abort(404, "Run non trovato")
    meta = read_meta(run_dir)
    if not (run_dir / "output.html").exists():
        abort(404, "Output non trovato")

    return render_template_string(
        VIEW_WRAPPER_HTML,
        filename=meta.get("filename", run_id),
        kind=meta.get("kind", "unknown"),
        root_tag=meta.get("root_tag", "unknown"),
        is_p7m=bool(meta.get("is_p7m", False)),
        content_url=url_for("content", run_id=run_id),
        validate_url=url_for("validate", run_id=run_id),
        download_url=url_for("download", run_id=run_id),
    )


@app.get("/content/<run_id>")
def content(run_id: str):
    run_dir = UPLOAD_ROOT / run_id
    out_path = run_dir / "output.html"
    if not out_path.exists():
        abort(404, "Output non trovato")
    return send_file(str(out_path), mimetype="text/html")


@app.get("/download/<run_id>")
def download(run_id: str):
    run_dir = UPLOAD_ROOT / run_id
    out_path = run_dir / "output.html"
    if not out_path.exists():
        abort(404, "Output non trovato")
    return send_file(str(out_path), mimetype="text/html", as_attachment=True, download_name=f"{run_id}.html")


@app.get("/validate/<run_id>")
def validate(run_id: str):
    run_dir = UPLOAD_ROOT / run_id
    if not run_dir.exists():
        abort(404, "Run non trovato")

    meta = read_meta(run_dir)
    filename = meta.get("filename", "")
    root_tag = meta.get("root_tag", "")
    is_p7m = bool(meta.get("is_p7m", False))

    in_path = run_dir / filename
    if not in_path.exists():
        abort(404, "File originale non trovato")

    # --- firma + payload
    sig_ok = False
    sig_msg = "N/A"
    payload_xml: Optional[pathlib.Path] = None

    if is_p7m:
        payload_xml = run_dir / "payload_verified.xml"
        sig_ok, sig_msg = openssl_verify_and_extract(in_path, payload_xml)
        if not sig_ok:
            # Se firma non ok, NON validiamo XSD (puoi cambiare questa policy se vuoi)
            xsds = list_xsds()
            return render_template_string(
                VALIDATION_HTML,
                view_url=url_for("view", run_id=run_id),
                validate_url=url_for("validate", run_id=run_id),
                filename=filename,
                root_tag=root_tag,
                is_p7m=is_p7m,
                sig_ok=sig_ok,
                sig_msg=sig_msg,
                xsds=xsds,
                schema_sel=request.args.get("schema", "auto"),
                schema_used="(non eseguita: firma non valida)",
                xsd_ok=False,
                xsd_errors=[],
                xsd_note="Validazione XSD non eseguita perché la verifica firma non è andata a buon fine.",
            )
        # aggiorna root_tag dal payload verificato (in caso di mismatch)
        try:
            root_tag = detect_root_tag(payload_xml)
        except Exception:
            pass
    else:
        payload_xml = in_path

    # --- scelta schema
    xsds = list_xsds()
    schema_sel = request.args.get("schema", "auto")

    schema_path: Optional[pathlib.Path] = None
    xsd_note = ""

    if not XSD_DIR.exists():
        xsd_note = "Cartella xsd/ non trovata: aggiungi gli XSD in ./xsd"
    else:
        if schema_sel == "auto":
            schema_path = pick_xsd_for_root(root_tag)
            if schema_path is None:
                xsd_note = f"Autodetect non riuscito per root tag '{root_tag}'. Seleziona manualmente uno schema."
        else:
            candidate = XSD_DIR / schema_sel
            if candidate.exists():
                schema_path = candidate
            else:
                xsd_note = f"Schema selezionato non trovato: {schema_sel}"

    # --- validazione
    xsd_ok = False
    xsd_errors: List[Dict[str, str]] = []
    schema_used = schema_path.name if schema_path else "N/A"

    if schema_path and payload_xml:
        try:
            xsd_ok, xsd_errors = validate_xml_with_xsd(payload_xml, schema_path)
        except Exception as e:
            xsd_ok = False
            xsd_errors = [{
                "line": "",
                "column": "",
                "level": "FATAL",
                "type": "Exception",
                "domain": "app",
                "message": str(e),
            }]

    return render_template_string(
        VALIDATION_HTML,
        view_url=url_for("view", run_id=run_id),
        validate_url=url_for("validate", run_id=run_id),
        filename=filename,
        root_tag=root_tag,
        is_p7m=is_p7m,
        sig_ok=sig_ok if is_p7m else False,
        sig_msg=sig_msg,
        xsds=xsds,
        schema_sel=schema_sel,
        schema_used=schema_used,
        xsd_ok=xsd_ok if schema_path else False,
        xsd_errors=xsd_errors,
        xsd_note=xsd_note,
    )


def resolve_ssl_context():
    if USE_HTTPS.strip().lower() not in ("1", "true", "yes"):
        return None
    cert = pathlib.Path(TLS_CERT_PATH)
    key = pathlib.Path(TLS_KEY_PATH)
    if cert.exists() and key.exists():
        return (str(cert), str(key))
    return None


if __name__ == "__main__":
    ssl_ctx = resolve_ssl_context()
    if ssl_ctx:
        print("Avvio HTTPS su https://127.0.0.1:5000")
        app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=ssl_ctx)
    else:
        print("Avvio HTTP su http://127.0.0.1:5000 (TLS non trovato o disabilitato)")
        app.run(host="0.0.0.0", port=5000, debug=True)

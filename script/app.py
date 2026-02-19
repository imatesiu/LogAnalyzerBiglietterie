#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import uuid
import shutil
import tempfile
import subprocess
import pathlib
import xml.etree.ElementTree as ET
from flask import Flask, request, redirect, url_for, send_file, render_template_string, abort

APP_DIR = pathlib.Path(__file__).resolve().parent
UPLOAD_ROOT = APP_DIR / "uploads"
UPLOAD_ROOT.mkdir(exist_ok=True)

RPM_SCRIPT = APP_DIR / "rpm_reader.py"
LOG_SCRIPT = APP_DIR / "log_reader.py"

MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# TLS paths (default: ./tls/fullchain.pem e ./tls/key.pem)
TLS_CERT_PATH = os.environ.get("TLS_CERT_PATH", str(APP_DIR / "tls" / "fullchain.pem"))
TLS_KEY_PATH = os.environ.get("TLS_KEY_PATH", str(APP_DIR / "tls" / "key.pem"))
USE_HTTPS = os.environ.get("USE_HTTPS", "1")  # "1"=HTTPS se cert/key esistono, "0"=solo HTTP

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag and "}" in tag else (tag or "")


# -------------------------
# P7M extraction
# -------------------------
def looks_pem(path: pathlib.Path) -> bool:
    with path.open("rb") as f:
        head = f.read(64)
    return b"-----BEGIN" in head

def extract_p7m_to_temp_xml(p7m_path: pathlib.Path) -> pathlib.Path:
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
        pass

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


def detect_kind_from_xml(xml_path: pathlib.Path) -> str:
    root = ET.parse(str(xml_path)).getroot()
    tag = localname(root.tag)
    if tag == "RiepilogoMensile":
        return "rpm"
    if tag == "LogTransazione":
        return "log"
    return "unknown"

def detect_kind(upload_path: pathlib.Path) -> str:
    if upload_path.name.lower().endswith(".p7m"):
        tmp = extract_p7m_to_temp_xml(upload_path)
        try:
            return detect_kind_from_xml(tmp)
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
    return detect_kind_from_xml(upload_path)


def strip_ext_for_output(name: str) -> str:
    low = name.lower()
    if low.endswith(".p7m"):
        name = name[:-4]
        low = name.lower()
    if low.endswith(".xml") or low.endswith(".xsi"):
        name = name[:-4]
    return name


def run_reader(kind: str, in_file: pathlib.Path, no_cents: bool) -> pathlib.Path:
    if kind == "rpm":
        script = RPM_SCRIPT
        out_suffix = ".rpm.html"
    elif kind == "log":
        script = LOG_SCRIPT
        out_suffix = ".log.html"
    else:
        raise RuntimeError("Tipo file non riconosciuto: non è né RPM (RiepilogoMensile) né LOG (LogTransazione).")

    if not script.exists():
        raise RuntimeError(f"Script mancante: {script.name}. Mettilo nella stessa cartella di app.py")

    cmd = [sys.executable, str(script), str(in_file)]
    if no_cents:
        cmd.append("--no-cents")

    subprocess.run(cmd, check=True)

    base = strip_ext_for_output(in_file.name)
    out_path = in_file.with_name(base + out_suffix)
    if out_path.exists():
        return out_path

    # fallback: ultimo html generato nella run_dir
    htmls = sorted(in_file.parent.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    if htmls:
        return htmls[0]
    raise RuntimeError("Lo script ha terminato ma non trovo l'HTML di output.")


INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>RPM/LOG Viewer</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.35;color:#111;}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:14px;background:#fff;max-width:780px;}
    input[type=file]{margin-top:8px;}
    button{margin-top:12px;padding:10px 14px;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer;}
    .muted{color:#666;font-size:13px;margin-top:8px;}
    label{display:flex;gap:10px;align-items:center;margin-top:10px;}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;}
  </style>
</head>
<body>
  <h1>RPM / LOG Viewer</h1>
  <div class="card">
    <form action="/upload" method="post" enctype="multipart/form-data">
      <div><b>Carica un file</b> RPM o LOG (anche .p7m)</div>
      <input type="file" name="file" required />

      <label>
        <input type="checkbox" name="no_cents" />
        Non dividere per 100 gli importi (<code>--no-cents</code>)
      </label>

      <button type="submit">Carica e visualizza</button>
      <div class="muted">
        Riconoscimento automatico: <code>RiepilogoMensile</code> → RPM, <code>LogTransazione</code> → LOG.
      </div>
    </form>
  </div>
</body>
</html>
"""


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
        kind = detect_kind(in_path)
        out_html = run_reader(kind, in_path, no_cents=no_cents)
        out_fixed = run_dir / "output.html"
        shutil.copyfile(out_html, out_fixed)
        return redirect(url_for("view", run_id=run_id))
    except subprocess.CalledProcessError as e:
        return f"<pre>Errore eseguendo lo script: {html.escape(str(e))}</pre>", 500
    except Exception as e:
        return f"<pre>Errore: {html.escape(str(e))}</pre>", 500


@app.get("/view/<run_id>")
def view(run_id: str):
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


def resolve_ssl_context():
    if USE_HTTPS.strip() not in ("1", "true", "True", "YES", "yes"):
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

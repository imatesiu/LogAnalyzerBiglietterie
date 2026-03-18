
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import pandas as pd
from PyPDF2 import PdfReader

@dataclass
class RefData:
    ordini_posto: List[Dict[str,str]]          # [{"code","desc"}]
    tipi_titolo: List[Dict[str,str]]           # [{"code","desc","cat"}]
    causali_ann: List[Dict[str,str]]           # [{"code","desc"}]
    aliquote: pd.DataFrame                     # columns: Codice, Descrizione, IVA_rates_%, ISI_rates_%, ...
    aliq_map: Dict[str, Dict[str, str]]        # str(Codice)->row dict

def _pdf_extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        t = page.extract_text() or ""
        parts.append(t)
    return "\n".join(parts)

def load_ordini_posto(pdf_path: Path) -> List[Dict[str,str]]:
    if not pdf_path.exists():
        return []
    txt = _pdf_extract_text(pdf_path)
    items = []
    # lines: "AA Anello A"
    for line in txt.splitlines():
        line = line.strip()
        m = re.match(r"^([A-Z]{2})\s+(.+)$", line)
        if m and m.group(1) not in ("TAB", "NOTA"):
            code, desc = m.group(1), m.group(2).strip()
            # avoid header
            if code == "Codice":
                continue
            # drop note lines beginning with bullet
            if desc.startswith("–") or desc.startswith("-"):
                continue
            items.append({"code": code, "desc": desc})
    # unique keep order
    seen=set(); out=[]
    for it in items:
        if it["code"] in seen: 
            continue
        seen.add(it["code"]); out.append(it)
    return out

def load_causali_ann(pdf_path: Path) -> List[Dict[str,str]]:
    if not pdf_path.exists():
        return []
    txt = _pdf_extract_text(pdf_path)
    items=[]
    for line in txt.splitlines():
        line=line.strip()
        m=re.match(r"^(\d{3})\s+(.+)$", line)
        if m:
            items.append({"code": m.group(1), "desc": m.group(2).strip()})
    # unique
    seen=set(); out=[]
    for it in items:
        if it["code"] in seen: 
            continue
        seen.add(it["code"]); out.append(it)
    return out

def load_tipi_titolo(pdf_path: Path) -> List[Dict[str,str]]:
    if not pdf_path.exists():
        return []
    txt=_pdf_extract_text(pdf_path)
    items=[]
    current_cat=""
    for line in txt.splitlines():
        line=line.strip()
        # category lines
        if line.upper() in ("INTERO","RIDOTTO","OMAGGIO"):
            current_cat=line.upper()
            continue
        # entries like "I1 Intero" or "IX Intero Generico (1)"
        m=re.match(r"^([A-Z0-9]{2})\s+(.+)$", line)
        if m:
            code=m.group(1)
            desc=m.group(2).strip()
            if code in ("CODICE","TAB.","TAB"):
                continue
            # avoid page footer fragment
            if desc.startswith("–"):
                continue
            items.append({"code": code, "desc": desc, "cat": current_cat})
    # unique
    seen=set(); out=[]
    for it in items:
        if it["code"] in seen:
            continue
        seen.add(it["code"]); out.append(it)
    return out

def load_aliquote(csv_path: Path) -> Tuple[pd.DataFrame, Dict[str, Dict[str,str]]]:
    if not csv_path.exists():
        df = pd.DataFrame(columns=["Codice","Descrizione","IVA_rates_%","IVA_variable","ISI_rates_%"])
        return df, {}
    df = pd.read_csv(csv_path)
    # normalize
    df["Codice"] = df["Codice"].astype(str).str.strip()
    df["Descrizione"] = df["Descrizione"].astype(str).str.strip()
    # build dict map
    m = {}
    for _, row in df.iterrows():
        m[str(row["Codice"])] = {k: ("" if pd.isna(v) else str(v)) for k,v in row.to_dict().items()}
    return df, m

def load_all(reference_dir: Path) -> RefData:
    ordini = load_ordini_posto(reference_dir / "TAB. 2 - Ordini di Posto (Settori).pdf")
    tipi = load_tipi_titolo(reference_dir / "TAB. 3 - Tipi Titolo Abbonamento.pdf")
    causali = load_causali_ann(reference_dir / "TAB. 5 - Causale Annullamento.pdf")
    df, aliq_map = load_aliquote(reference_dir / "aliquote_tab1.csv")
    return RefData(
        ordini_posto=ordini,
        tipi_titolo=tipi,
        causali_ann=causali,
        aliquote=df,
        aliq_map=aliq_map,
    )

def fallback_ordini() -> List[str]:
    return ["UN","PT","PR","TA","TB","TC","DA","DB","DC","CA","CB","CC"]

def fallback_tipi() -> List[str]:
    return ["I1","R1","O1","O4","IX","RX","OX"]

def fallback_causali() -> List[str]:
    return ["001","002","003","004","005","006","007","008","009","010"]

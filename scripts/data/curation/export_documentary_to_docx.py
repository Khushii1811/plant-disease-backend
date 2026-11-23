"""
scripts/export_documentary_to_docx.py — Exports the 168-class Before vs After documentary
to a Microsoft Word document (.docx).

Requirements:
    uv pip install python-docx
Usage:
    .venv\\Scripts\\python.exe scripts/export_documentary_to_docx.py
"""

import csv
import json
import sys
from pathlib import Path

try:
    import docx
    from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import nsdecls, qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    print("python-docx is not installed.")
    print("To install it, run: .venv\\Scripts\\python.exe -m pip install python-docx")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
OUT_DOCX = DATA_DIR / "per_class_before_after_documentary.docx"


def set_cell_background(cell, fill_color: str):
    """Sets background color of a table cell (e.g. 'F1F5F9')."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def main():
    # 1. Load Data
    baseline_file = MODELS_DIR / "baseline_per_class_benchmark.json"
    with open(baseline_file, "r", encoding="utf-8") as f:
        baseline_list = json.load(f)

    counts_file = DATA_DIR / "processed_class_counts.csv"
    counts_map = {}
    if counts_file.exists():
        with open(counts_file, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                counts_map[r["class_name"]] = r

    # 2. Initialize Word Document
    doc = docx.Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Header
    title = doc.add_heading("🌿 Plant Disease Classification: Per-Class Evolution Documentary", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph("Comparative Analysis of Data Quality, Scores, and Curation Actions across 168 Classes.")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()  # spacing

    print(f"Building Word document for {len(baseline_list)} classes...")

    for idx, item in enumerate(baseline_list, 1):
        name = item["class_name"]
        bf1 = item["baseline_tta_f1"] * 100
        bprec = item["baseline_tta_prec"] * 100
        brec = item["baseline_tta_rec"] * 100
        bsup = item["support"]

        counts = counts_map.get(name, {})
        cur_train = counts.get("train_count", "—")

        # Class Heading
        h2 = doc.add_heading(f"{idx}. {name}", level=2)
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(4)

        # 1. Score Table
        table = doc.add_table(rows=6, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Metric", "Before (Baseline)", "After (Cleaned)", "Change (Δ)"]
        hdr_cells = table.rows[0].cells
        for i, title_text in enumerate(headers):
            hdr_cells[i].text = title_text
            hdr_cells[i].paragraphs[0].runs[0].font.bold = True
            hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_background(hdr_cells[i], "F1F5F9")
            set_cell_margins(hdr_cells[i])

        row_data = [
            ("Train Images", str(cur_train), "[ Enter count ]", "—"),
            ("Precision", f"{bprec:.1f}%", "[ Enter prec ]", "—"),
            ("Recall", f"{brec:.1f}%", "[ Enter rec ]", "—"),
            ("F1-Score", f"{bf1:.1f}%", "[ Enter F1 ]", "—"),
            ("Test Support", f"{bsup} images", "[ Enter support ]", "—"),
        ]

        for r_idx, (m, b_val, a_val, diff) in enumerate(row_data, 1):
            row_cells = table.rows[r_idx].cells
            row_cells[0].text = m
            row_cells[0].paragraphs[0].runs[0].font.bold = True
            row_cells[1].text = b_val
            row_cells[2].text = a_val
            row_cells[2].paragraphs[0].runs[0].font.italic = True
            row_cells[3].text = diff

            for c in row_cells:
                c.paragraphs[0].runs[0].font.size = Pt(9)
                set_cell_margins(c)

        # 2. Action Log Section
        doc.add_paragraph()
        p_act = doc.add_paragraph()
        r_act = p_act.add_run("🛠️ Action Taken / Cleaning Log:")
        r_act.bold = True
        r_act.font.size = Pt(9.5)
        p_act.paragraph_format.space_before = Pt(4)
        p_act.paragraph_format.space_after = Pt(2)

        p_items = doc.add_paragraph(style='List Bullet')
        p_items.add_run("Collages removed: [ e.g. 0 ]")
        p_items2 = doc.add_paragraph(style='List Bullet')
        p_items2.add_run("Noisy / out-of-domain images purged: [ e.g. fruit photos, houses ]")
        p_items3 = doc.add_paragraph(style='List Bullet')
        p_items3.add_run("New scraped images added: [ e.g. 40 Bing images ]")

        # 3. Image Comparison Box (Table placeholder for dragging and dropping images)
        p_vis = doc.add_paragraph()
        r_vis = p_vis.add_run("🖼️ Visual Comparison:")
        r_vis.bold = True
        r_vis.font.size = Pt(9.5)
        p_vis.paragraph_format.space_before = Pt(4)
        p_vis.paragraph_format.space_after = Pt(2)

        img_table = doc.add_table(rows=1, cols=2)
        img_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_before, c_after = img_table.rows[0].cells

        c_before.text = "❌ BEFORE:\n\n[ Paste / Insert Noisy / Collage Image Here ]\n"
        c_after.text = "✅ AFTER:\n\n[ Paste / Insert Clean Leaf Specimen Here ]\n"

        for cell in [c_before, c_after]:
            set_cell_background(cell, "FAFAFA")
            set_cell_margins(cell, top=200, bottom=200, left=200, right=200)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(100, 116, 139)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph()  # spacer between classes

    # Save
    doc.save(OUT_DOCX)
    print(f"\nSuccessfully created Microsoft Word document at:\n{OUT_DOCX}")


if __name__ == "__main__":
    main()

from pathlib import Path
import re
import tempfile

from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PDF_DIR = RESULTS / "pdf"
PDF_DIR.mkdir(exist_ok=True)

FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\ariali.ttf"

pdfmetrics.registerFont(TTFont("Study", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("Study-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("Study-Italic", FONT_ITALIC))


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Study-Bold",
            fontSize=22,
            leading=27,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Study-Bold",
            fontSize=18,
            leading=23,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Study-Bold",
            fontSize=15,
            leading=19,
            spaceBefore=9,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Study-Bold",
            fontSize=12.5,
            leading=16,
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Study",
            fontSize=9.4,
            leading=12.2,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="Study",
            fontSize=9.2,
            leading=12,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=6,
            backColor=colors.whitesmoke,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Study",
            fontSize=8,
            leading=10,
            spaceAfter=2,
        ),
    }


STYLES = styles()


def esc(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    return text


def clean_line(line: str) -> str:
    return line.rstrip("\n")


def paragraph(text, style="body"):
    return Paragraph(esc(text), STYLES[style])


def markdown_to_flowables(markdown: str, title: str | None = None):
    flow = []
    if title:
        flow.append(Paragraph(esc(title), STYLES["title"]))

    lines = markdown.splitlines()
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        raw = clean_line(lines[i])
        line = raw.strip()

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                flow.append(Preformatted("\n".join(code_lines), STYLES["code"]))
                in_code = False
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        if not line:
            flow.append(Spacer(1, 4))
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for idx, tl in enumerate(table_lines):
                cells = [c.strip() for c in tl.strip("|").split("|")]
                if idx == 1 and all(set(c) <= set("-: ") for c in cells):
                    continue
                rows.append([Paragraph(esc(c), STYLES["small"]) for c in cells])
            if rows:
                table = Table(rows, repeatRows=1, hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, -1), "Study"),
                            ("FONTNAME", (0, 0), (-1, 0), "Study-Bold"),
                            ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ]
                    )
                )
                flow.append(table)
                flow.append(Spacer(1, 6))
            continue

        if line.startswith("# "):
            flow.append(Paragraph(esc(line[2:].strip()), STYLES["h1"]))
        elif line.startswith("## "):
            flow.append(Paragraph(esc(line[3:].strip()), STYLES["h2"]))
        elif line.startswith("### "):
            flow.append(Paragraph(esc(line[4:].strip()), STYLES["h3"]))
        elif line.startswith("#### "):
            flow.append(Paragraph(esc(line[5:].strip()), STYLES["h3"]))
        elif line.startswith("- "):
            flow.append(Paragraph("• " + esc(line[2:].strip()), STYLES["bullet"]))
        elif re.match(r"^\d+\.\s+", line):
            flow.append(Paragraph(esc(line), STYLES["bullet"]))
        else:
            flow.append(paragraph(line))
        i += 1

    return flow


def make_pdf_from_markdown(md_path: Path, out_path: Path, title: str | None = None):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=title or md_path.stem,
    )
    flow = markdown_to_flowables(md_path.read_text(encoding="utf-8"), title=title)
    doc.build(flow)


def split_h2_sections(markdown: str):
    sections = {}
    matches = list(re.finditer(r"^##\s+(.+)$", markdown, flags=re.MULTILINE))
    for idx, match in enumerate(matches):
        header = match.group(1).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        sections[header] = body
    return sections


def image_flowable(path: Path, max_w: float, max_h: float):
    with PILImage.open(path) as im:
        w_px, h_px = im.size
    ratio = min(max_w / w_px, max_h / h_px)
    return Image(str(path), width=w_px * ratio, height=h_px * ratio)


def make_primeri_on_pages():
    md = (RESULTS / "resitve_primeri.md").read_text(encoding="utf-8")
    sections = split_h2_sections(md)
    doc = SimpleDocTemplate(
        str(PDF_DIR / "primeri_reseni_na_polah.pdf"),
        pagesize=A4,
        rightMargin=1.35 * cm,
        leftMargin=1.35 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
        title="Primeri - rešeno na polah",
    )
    flow = [Paragraph("Primeri - rešeno na polah", STYLES["title"])]

    for header, body in sections.items():
        m = re.search(r"`([^`]+\.(?:jpg|jpeg|png))`", header, flags=re.IGNORECASE)
        if not m:
            continue
        image_name = m.group(1)
        image_path = ROOT / "Primeri" / image_name
        flow.append(PageBreak())
        flow.append(Paragraph(esc(header.replace("`", "")), STYLES["h1"]))
        if image_path.exists():
            flow.append(image_flowable(image_path, 18.0 * cm, 10.0 * cm))
            flow.append(Spacer(1, 8))
        flow.append(Paragraph("Rešitev / postopek", STYLES["h2"]))
        body_without_header = "\n".join(body.splitlines()[1:]).strip()
        flow.extend(markdown_to_flowables(body_without_header))

    doc.build(flow)


def make_individual_primeri_pdfs():
    md = (RESULTS / "resitve_primeri.md").read_text(encoding="utf-8")
    sections = split_h2_sections(md)
    out_dir = PDF_DIR / "primeri_posamezno"
    out_dir.mkdir(exist_ok=True)
    for header, body in sections.items():
        m = re.search(r"`([^`]+\.(?:jpg|jpeg|png))`", header, flags=re.IGNORECASE)
        if not m:
            continue
        image_name = m.group(1)
        image_path = ROOT / "Primeri" / image_name
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", image_name.rsplit(".", 1)[0])
        out_path = out_dir / f"reseno_{safe}.pdf"
        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=A4,
            rightMargin=1.35 * cm,
            leftMargin=1.35 * cm,
            topMargin=1.2 * cm,
            bottomMargin=1.2 * cm,
            title=f"Rešeno - {image_name}",
        )
        flow = [Paragraph(esc(header.replace("`", "")), STYLES["h1"])]
        if image_path.exists():
            flow.append(image_flowable(image_path, 18.0 * cm, 10.0 * cm))
            flow.append(Spacer(1, 8))
        flow.append(Paragraph("Rešitev / postopek", STYLES["h2"]))
        flow.extend(markdown_to_flowables("\n".join(body.splitlines()[1:]).strip()))
        doc.build(flow)


def section_for_filename(sections: dict[str, str], filename: str):
    for header, body in sections.items():
        if filename in header:
            return body
    return None


def make_solution_fragment(section_md: str, out_path: Path, title: str):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=title,
    )
    flow = [Paragraph(esc(title), STYLES["title"])]
    flow.extend(markdown_to_flowables(section_md))
    doc.build(flow)


def make_augmented_lecture_pdfs():
    md = (RESULTS / "resitve_predavanja.md").read_text(encoding="utf-8")
    sections = split_h2_sections(md)
    out_dir = PDF_DIR / "predavanja_dopolnjeno"
    out_dir.mkdir(exist_ok=True)

    for original in sorted((ROOT / "Predavanja").glob("*.pdf")):
        section = section_for_filename(sections, original.name)
        if not section:
            continue
        with tempfile.TemporaryDirectory() as td:
            fragment = Path(td) / "resitve.pdf"
            make_solution_fragment(
                section,
                fragment,
                f"Dodane rešitve in dopolnitve za {original.name}",
            )
            writer = PdfWriter()
            for page in PdfReader(str(original)).pages:
                writer.add_page(page)
            for page in PdfReader(str(fragment)).pages:
                writer.add_page(page)
            out_path = out_dir / f"dopolnjeno_{original.name}"
            with out_path.open("wb") as f:
                writer.write(f)


def make_combined_study_pdf():
    parts = [
        ("Inventar", RESULTS / "inventar.md"),
        ("Rešitve predavanj", RESULTS / "resitve_predavanja.md"),
        ("Rešitve primerov", RESULTS / "resitve_primeri.md"),
        ("Super učni vodič", RESULTS / "super_ucni_vodic.md"),
        ("Izpitni povzetek A4", RESULTS / "izpitni_povzetek_A4.md"),
        ("Status", RESULTS / "status.md"),
    ]
    doc = SimpleDocTemplate(
        str(PDF_DIR / "vse_za_ucenje_skupaj.pdf"),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.25 * cm,
        title="Vse za učenje APS2",
    )
    flow = [Paragraph("Vse za učenje APS2", STYLES["title"])]
    first = True
    for title, path in parts:
        if not first:
            flow.append(PageBreak())
        first = False
        flow.append(Paragraph(esc(title), STYLES["h1"]))
        flow.extend(markdown_to_flowables(path.read_text(encoding="utf-8")))
    doc.build(flow)


def main():
    simple_docs = [
        ("inventar.md", "Inventar gradiva"),
        ("resitve_predavanja.md", "Rešitve in dopolnitve predavanj"),
        ("resitve_primeri.md", "Rešitve primerov"),
        ("super_ucni_vodic.md", "Super učni vodič APS2"),
        ("izpitni_povzetek_A4.md", "Izpitni povzetek A4"),
        ("status.md", "Status priprave"),
    ]

    for filename, title in simple_docs:
        make_pdf_from_markdown(
            RESULTS / filename,
            PDF_DIR / filename.replace(".md", ".pdf"),
            title,
        )

    make_combined_study_pdf()
    make_primeri_on_pages()
    make_individual_primeri_pdfs()
    make_augmented_lecture_pdfs()


if __name__ == "__main__":
    main()

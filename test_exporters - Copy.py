from utils.document_utils import sanitize_text, format_html_preview
from utils.exporters import format_txt, format_docx, format_pdf


SAMPLE = """NON-DISCLOSURE AGREEMENT

1. CONFIDENTIALITY
The receiving party shall protect confidential information.

2. TERM
The agreement begins on the effective date.
"""


def test_sanitize_text():
    result = sanitize_text("“Hello”—world…")
    assert result == '"Hello"-world...'


def test_html_preview_escapes_html():
    result = format_html_preview("<script>alert(1)</script>")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_txt_export():
    data = format_txt(SAMPLE)
    assert data.startswith(b"NON-DISCLOSURE")


def test_docx_export():
    data = format_docx(SAMPLE, "NDA", "Protect information; No disclosure")
    assert data[:2] == b"PK"
    assert len(data) > 5000


def test_pdf_export():
    data = format_pdf(SAMPLE, "NDA", "Protect information; No disclosure")
    assert data.startswith(b"%PDF")
    assert len(data) > 5000

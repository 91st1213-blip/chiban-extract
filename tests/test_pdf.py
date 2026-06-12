"""PDF I/O tests using in-memory PDFs generated with PyMuPDF (no binary fixtures)."""

import fitz
import pytest

from chiban_extract.pdf import read_pdf


def make_pdf(pages: list[str]) -> bytes:
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text, fontname="japan", fontsize=11)
    data = doc.tobytes()
    doc.close()
    return data


def test_read_pdf_bytes(sample_text):
    data = make_pdf([sample_text])
    doc = read_pdf(data)
    assert doc.page_count == 1
    assert "南青山1丁目1番1号" in doc.text  # NFKC-normalized


def test_read_pdf_path(tmp_path, sample_text):
    p = tmp_path / "sample.pdf"
    p.write_bytes(make_pdf([sample_text, "2ページ目"]))
    doc = read_pdf(p)
    assert doc.page_count == 2
    assert "物件概要書" in doc.text


def test_read_pdf_str_path(tmp_path, sample_text):
    p = tmp_path / "sample.pdf"
    p.write_bytes(make_pdf([sample_text]))
    doc = read_pdf(str(p))
    assert doc.page_count == 1


def test_read_pdf_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_pdf(tmp_path / "missing.pdf")


def test_read_pdf_url(monkeypatch, sample_text):
    data = make_pdf([sample_text])
    monkeypatch.setattr("chiban_extract.pdf._fetch_url", lambda url: data)
    doc = read_pdf("https://example.com/document.pdf")
    assert doc.page_count == 1
    assert "南青山" in doc.text

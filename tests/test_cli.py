import json

import pytest

from chiban_extract.cli import main
from test_pdf import make_pdf


@pytest.fixture
def sample_pdf(tmp_path, sample_text):
    p = tmp_path / "sample.pdf"
    p.write_bytes(make_pdf([sample_text]))
    return p


def test_extract_json(sample_pdf, capsys):
    rc = main(["extract", str(sample_pdf), "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["best"]["address"] == "東京都港区南青山1丁目1番1号"


def test_extract_human_readable(sample_pdf, capsys):
    rc = main(["extract", str(sample_pdf)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "best: 東京都港区南青山1丁目1番1号" in out


def test_extract_nothing_found(tmp_path, no_address_text, capsys):
    p = tmp_path / "noaddr.pdf"
    p.write_bytes(make_pdf([no_address_text]))
    assert main(["extract", str(p), "--json"]) == 1


def test_extract_missing_file(tmp_path, capsys):
    rc = main(["extract", str(tmp_path / "nope.pdf")])
    assert rc == 2
    assert "error" in capsys.readouterr().err


def test_extract_known_address_filter(sample_pdf):
    assert main(["extract", str(sample_pdf), "--known-address", "熊本県熊本市"]) == 1

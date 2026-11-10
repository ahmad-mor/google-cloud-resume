from unittest.mock import MagicMock, patch

import flask
import pytest

# نستبدل اتصال Firestore الحقيقي بواحد وهمي قبل ما نفتح main.py
with patch("google.cloud.firestore.Client"):
    import main

app = flask.Flask(__name__)


def fake_snapshot(data, exists=True):
    snap = MagicMock()
    snap.exists = exists
    snap.to_dict.return_value = data
    return snap


def call(method):
    with app.test_request_context(method=method):
        return main.hello_http(flask.request)


def test_next_count_adds_one():
    assert main.next_count(5) == 6


def test_read_count():
    assert main.read_count(fake_snapshot({"count": 7})) == 7
    assert main.read_count(fake_snapshot(None)) == 0
    assert main.read_count(fake_snapshot({}, exists=False)) == 0


def test_get_returns_count(monkeypatch):
    ref = MagicMock()
    ref.get.return_value = fake_snapshot({"count": 7})
    monkeypatch.setattr(main, "doc_ref", ref)

    body, status, _ = call("GET")
    assert status == 200
    assert body.get_json() == {"count": 7}


def test_get_does_not_increment(monkeypatch):
    ref = MagicMock()
    ref.get.return_value = fake_snapshot({"count": 7})
    monkeypatch.setattr(main, "doc_ref", ref)
    inc = MagicMock()
    monkeypatch.setattr(main, "increment", inc)

    call("GET")
    inc.assert_not_called()


def test_unknown_method_returns_405():
    _, status, _ = call("PUT")
    assert status == 405


def test_database_error_returns_500(monkeypatch):
    ref = MagicMock()
    ref.get.side_effect = Exception("database down")
    monkeypatch.setattr(main, "doc_ref", ref)

    _, status, _ = call("GET")
    assert status == 500
# /price calls the partner over HTTP, but unit tests must not so requests.get is replaced.
import requests

import app as catshop


class FakeResponse:
    def __init__(self, body, status=200):
        self._body, self.status_code = body, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self._body


def test_price_passes_the_partner_answer_through(client, monkeypatch):
    calls = []

    def fake_get(url, timeout):
        calls.append(url)
        return FakeResponse({"price": 1200, "currency": "UAH"})

    monkeypatch.setattr(catshop.requests, "get", fake_get)
    r = client.get("/price/MK-II")
    assert r.status_code == 200
    assert r.get_json()["price"] == 1200
    assert calls == [f"{catshop.PARTNER_URL}/v1/catalog/MK-II"]


def test_partner_down_is_a_502(client, monkeypatch):
    def fake_get(url, timeout):
        raise requests.ConnectionError("partner is not there")

    monkeypatch.setattr(catshop.requests, "get", fake_get)
    r = client.get("/price/MK-II")
    assert r.status_code == 502
    assert r.get_json()["error"] == "ConnectionError"


def test_partner_error_status_is_a_502(client, monkeypatch):
    monkeypatch.setattr(catshop.requests, "get", lambda url, timeout: FakeResponse({}, 500))
    assert client.get("/price/MK-II").status_code == 502

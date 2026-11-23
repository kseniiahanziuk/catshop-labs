import pytest

import app as catshop


@pytest.fixture
def counter_file(tmp_path, monkeypatch):
    path = tmp_path / "data" / "visits.txt"
    monkeypatch.setattr(catshop, "COUNTER_FILE", path)
    monkeypatch.setattr(catshop, "DATABASE_URL", None)
    return path


@pytest.fixture
def client(counter_file):
    return catshop.app.test_client()

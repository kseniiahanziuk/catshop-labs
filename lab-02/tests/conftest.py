"""Shared fixtures.

The app reads COUNTER_FILE and DATABASE_URL into module globals at import time, so the
fixtures patch those globals rather than the environment. Every test gets its own
counter file under pytest's tmp_path and runs with the file store, whatever the
environment of the machine running the suite says.
"""
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

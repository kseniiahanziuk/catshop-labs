def test_ready_with_file_store(client, counter_file):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.get_json() == {"ready": True, "store": f"file:{counter_file}"}


def test_not_ready_when_the_counter_directory_cannot_be_created(client, counter_file):
    counter_file.parent.write_text("in the way")
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.get_json()["ready"] is False

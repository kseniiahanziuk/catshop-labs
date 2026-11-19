def test_health_says_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.data == b"ok\n"


def test_health_does_not_touch_the_counter(client, counter_file):
    client.get("/health")
    assert not counter_file.exists()

def test_first_visit_is_one(client):
    r = client.get("/visits")
    assert r.status_code == 200
    assert r.get_json() == {"visits": 1, "store": "file"}


def test_each_visit_adds_exactly_one(client):
    counts = [client.get("/visits").get_json()["visits"] for _ in range(3)]
    assert counts == [1, 2, 3]


def test_count_continues_from_the_existing_file(client, counter_file):
    counter_file.parent.mkdir(parents=True)
    counter_file.write_text("41")
    assert client.get("/visits").get_json()["visits"] == 42


def test_corrupt_counter_file_is_a_503(client, counter_file):
    counter_file.parent.mkdir(parents=True)
    counter_file.write_text("not a number")
    r = client.get("/visits")
    assert r.status_code == 503
    assert r.get_json()["store"] == "file"

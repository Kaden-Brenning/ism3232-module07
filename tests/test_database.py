import database


def make_db(tmp_path):
    """Create a fresh database with the sample rows, in a folder only this test uses."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_find_order_returns_a_dictionary(tmp_path):
    db_file = make_db(tmp_path)
    order = database.find_order(db_file, "B401")
    assert order["status"] == "ordered"
    assert order["pickup_desk"] == "North Desk"


def test_approve_changes_the_address_once(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "B401", "cancel")
    assert database.approve_request(db_file, 1) == "Request 1 approved."
    assert database.find_order(db_file, "B401")["status"] == "ordered"
    assert database.approve_request(db_file, 1) == "Request 1 is already approved."
    assert database.waiting_requests(db_file) == []

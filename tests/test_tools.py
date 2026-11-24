import database
from tools import CrestviewTools


def make_tools(tmp_path):
    """Build tools over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return CrestviewTools(db_file)


def customer(text):
    """Build a history that holds one customer message."""
    return [{"role": "user", "content": text}]


def test_made_up_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "look_up_order", {"order_id": "B401"}, customer("Status on B400?")
    )
    assert "has not given that order ID" in reply


def test_lookup_order_inside_sentence(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "look_up_order", {"order_id": "B401"}, customer("Can you check order B401?")
    )
    assert reply == "Order B401 is ordered."


def test_pickup_change_waits_for_staff(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "request_address_change",
        {
            "order_id": "B401",
            "new_pickup_desk": "South Desk",
        },
        customer("Please change order B401 to South Desk."),
    )

    assert "sent to staff" in reply

    requests = database.waiting_requests(tools.db_file)
    assert len(requests) == 1
    assert requests[0]["order_id"] == "B401"
    assert requests[0]["new_pickup_desk"] == "South Desk"


def test_unknown_tool_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("cancel_order", {}, customer("Please cancel order B401."))

    assert "There is no tool named cancel_order" in reply


def test_missing_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("look_up_order", {}, customer("Where is my textbook?"))

    assert "order ID is missing" in reply

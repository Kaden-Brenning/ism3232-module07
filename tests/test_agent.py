import database
from agent import SupportChatbot
from fake_model import FakeModel
from tools import CrestviewTools


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(tmp_path, model):
    """Build a chatbot over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SupportChatbot("Don", "Be friendly.", CrestviewTools(db_file), model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_model_chosen_lookup_answers_from_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "B401"}),
            {"text": "B401 is ordered."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Is B401 ordered?")
    assert bot.history[1]["content"] == "Order B401 is ordered."


def test_made_up_address_never_reaches_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "B401", "new_pickup_desk": "South"},
            ),
            {"text": "What is the new pickup?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the pickup on order B401")
    assert database.waiting_requests(bot.tools.db_file) == []

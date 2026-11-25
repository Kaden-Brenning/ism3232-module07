# tools.py
# Author: Kaden Brenning

import database


class CrestviewTools:
    """The tools the model may ask for. Every request is checked in run first."""

    def __init__(self, db_file):
        """Remember which database the tools read and write."""
        self.db_file = db_file

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.look_up_order,
            self.look_up_textbook,
            self.request_pickup_change,
            self.check_request,
        ]

    def look_up_order(self, order_id):
        """Look up the status of one bookstore order.

        Args:
            order_id: The order ID, like B400.
        """
        for word in order_id.upper().split():
            order = database.find_order(self.db_file, word.strip("?.!,#"))
            if order is not None:
                return f"Order {order['order_id']} is {order['status']}."

        return "No order with that ID was found. Order IDs look like B400."

    def look_up_textbook(self, item):
        """Look up a textbook's stock and price.

        Args:
            item: The textbook name.
        """
        textbooks = database.query_all(
            self.db_file, "SELECT name FROM textbooks ORDER BY name"
        )

        for row in textbooks:
            name = row["name"]
            if name.lower() in item.lower():
                textbook = database.query_one(
                    self.db_file,
                    "SELECT * FROM textbooks WHERE name = ?",
                    (name,),
                )
                stock = textbook["stock"]
                return (
                    f"We have {stock} copies of {name} in stock, "
                    f"at ${textbook['price']:.2f}."
                )

        return "That textbook was not found."

    def request_pickup_change(self, order_id, new_pickup_desk):
        """Ask staff to change the pickup desk on one order.

        Args:
            order_id: The order ID, like B400.
            new_pickup_desk: The new pickup desk requested by the customer.
        """
        order_id = order_id.upper()

        if database.find_order(self.db_file, order_id) is None:
            return "No order with that ID was found. Order IDs look like B400."

        number = database.add_change_request(self.db_file, order_id, new_pickup_desk)

        return (
            f"Request {number} was sent to staff. The pickup desk has not changed yet."
        )

    def check_request(self, number):
        """Check what staff decided about one pickup change request.

        Args:
            number: The request number, like 3.
        """
        try:
            request = database.find_request(self.db_file, int(number))
        except ValueError:
            return "Request numbers look like 3."
        except OverflowError:
            return f"There is no request {number}."

        if request is None:
            return f"There is no request {number}."

        order_id = request["order_id"]

        if request["status"] == "waiting":
            return f"Request {number} for order {order_id} is waiting for staff."

        return f"Request {number} for order {order_id} was {request['status']}."

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""

        if name == "look_up_order":
            order_id = self.clean(arguments, "order_id")

            if order_id == "":
                return "The order ID is missing. Ask the customer for it."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."

            return self.look_up_order(order_id)

        if name == "look_up_textbook":
            item = self.clean(arguments, "item")

            if item == "":
                return "The textbook is missing. Ask the customer which textbook."

            if not self.customer_said(history, item):
                return "The customer has not given that textbook name. Ask them for it."

            return self.look_up_textbook(item)

        if name == "request_pickup_change":
            order_id = self.clean(arguments, "order_id")
            new_pickup_desk = self.clean(arguments, "new_pickup_desk")

            if order_id == "" or new_pickup_desk == "":
                return "The order ID and the new pickup desk are both needed."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID. Ask them for it."

            if not self.customer_said(history, new_pickup_desk):
                return "The customer has not given that pickup desk. Ask them for it."

            return self.request_pickup_change(order_id, new_pickup_desk)

        if name == "check_request":
            number = self.clean(arguments, "number")

            if number == "":
                return "The request number is missing. Ask the customer for it."

            if not self.customer_said(history, number):
                return (
                    "The customer has not given that request number. Ask them for it."
                )

            return self.check_request(number)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def words(self, text):
        """Return text in lower case as whole words, without ?.!,# around each word."""
        cleaned = []
        for word in text.lower().split():
            cleaned.append(word.strip("?.!,#"))
        return " " + " ".join(cleaned) + " "

    def customer_said(self, history, text):
        """Return True if the customer typed text as whole words."""
        wanted = self.words(text)
        for message in history:
            if message["role"] == "user" and wanted in self.words(message["content"]):
                return True
        return False

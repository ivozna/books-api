import json
import random
import string
import time
from flask import Flask, request, jsonify
import database

database.connect()
app = Flask("server")
users = []
list_of_books = [{
    "id": 1,
    "name": "The Blue Whale",
    "type": "fiction",
    "available": True
},
    {
        "id": 2,
        "name": "Just as I Am",
        "type": "non-fiction",
        "available": True
},
    {
        "id": 3,
        "name": "The Vanishing Half",
        "type": "fiction",
        "available": True
},
    {
        "id": 4,
        "name": "The Midnight Library",
        "type": "fiction",
        "available": True
},
    {
        "id": 5,
        "name": "Untamed",
        "type": "non-fiction",
        "available": True
},
    {
        "id": 6,
        "name": "5",
        "type": "fiction",
        "available": True
}
]
orders = []


def get_client_id(request):
    access_token = request.headers['Authorization'][7:]
    client_id = database.get_id_with_token(access_token)
    return client_id

@app.route('/status')
def status():
    return jsonify({'status': "ok"})


@app.route('/books', methods=['GET'])
def get_list_of_books():
    type = request.args.get('type', None)
    limit = int(request.args.get('limit', 10))
    books = database.get_all_books(type, limit)
    return jsonify(books)


@app.route('/books/<int:id>', methods=['GET'])
def get_single_book(id):
    book = database.get_one_book(id)
    return jsonify(book)


@app.route('/api-clients/', methods=['POST'])
def register_api_client():
    body = dict(request.json)
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
    register_email = body["clientEmail"]
    register_name = body["clientName"]
    if database.client_is_registered(register_email):
        return jsonify({
            "error": "API client already registered. Try a different email."
        })
    body["accessToken"] = ran
    register_token = body["accessToken"]
    new_user = database.register_client(
        register_name, register_email, register_token)
    return jsonify(new_user)


@app.route('/orders', methods=['POST'])
def order_book():
    user_id = get_client_id(request)
    if user_id is None:
        return jsonify({"error": "no authorization available, please register a client", "created": False})

    body = dict(request.json)
    book_id = body["bookId"]
    quantity = 1
    order = database.place_order(book_id, user_id, quantity)
    return jsonify(order)


@app.route('/orders', methods=['GET'])
def get_all_orders():
    user_id = get_client_id(request)
    if user_id is None:
        return jsonify({"error": "no authorization available, please register a client", "created": False})

    client_orders = database.select_all_orders(user_id)
    return jsonify(client_orders)


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    user_id = get_client_id(request)
    if user_id is None:
        return jsonify({"error": "no authorization available, please register a client", "created": False})

    order = database.select_one_order(user_id, order_id)
    return jsonify(order)


@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    user_id = get_client_id(request)
    if user_id is None:
        return jsonify({"error": "no authorization available, please register a client", "created": False})

    body = dict(request.json)
    new_quantity = body["quantity"]
    order_to_update = database.update_order(new_quantity, user_id, order_id)
    return jsonify(order_to_update)


@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    user_id = get_client_id(request)
    if user_id is None:
        return jsonify({"error": "no authorization available, please register a client", "created": False})

    count = database.delete_one_order(user_id, order_id)
    if count == 1:
        return jsonify({"deleted": True})

    return jsonify({"error": "there's no such order", "deleted": False})

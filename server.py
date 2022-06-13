import random
import string
import time
from flask import Flask, request, jsonify


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
        "name": "Viscount Who Loved Me",
        "type": "fiction",
        "available": True
}
]
orders = []


def get_client_email(request):
    access_token = request.headers['Authorization'][6:]
    for user in users:
        if access_token == user["accessToken"]:
            return user["clientEmail"]
    return None

@app.route('/status')
def status():
    return jsonify({'status': "ok"})


@app.route('/books', methods=['GET'])
def get_list_of_books():
    type = request.args.get('type', None)
    limit = request.args.get('limit', None)

    data = list(filter(lambda x: x['type'] == type if type is not None else True, list_of_books))
    return jsonify(data[:limit])


@app.route('/books/<int:id>', methods=['GET'])
def get_single_book(id):
    for book in list_of_books:
        if book["id"] == id:
            return jsonify(book)

    return jsonify({'status': 'not found'})


@app.route('/api-clients/', methods=['POST'])
def register_api_client():
    body = dict(request.json)
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
    register_email = body["clientEmail"]
    for user in users:
        if user["clientEmail"] == register_email:
            return jsonify({
                "error": "API client already registered. Try a different email."
            })
    body["accessToken"] = ran
    users.append(body)
    return jsonify({"accessToken": ran})


@app.route('/orders', methods=['POST'])
def order_book():
    body = dict(request.json)
    ran_orderid = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=21))
    order = {
        'id': ran_orderid,
        'clientEmail': get_client_email(request),
        'quantity': 1,
        'timestamp': int(time.time()),
        'bookId': body["bookId"],
        'customerName': body["customerName"]
    }
    orders.append(order)
    return jsonify({
        "created": True,
        "orderId": order["id"]
    })

@app.route('/orders', methods=['GET'])
def get_all_orders():
    return jsonify(orders)

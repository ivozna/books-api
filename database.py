import psycopg2
from psycopg2.extras import RealDictCursor

connection = None

def connect():
    global connection
    if connection is None:
        connection = psycopg2.connect(user='postgres', password='1927', host='127.0.0.1', port='1111', database='books')
    return connection

def get_all_books(type=None, limit=None):
    cursor = connect().cursor()
    if type is None:
        cursor.execute("SELECT * from books LIMIT %s", (limit,))
    else:
        cursor.execute("SELECT * from books where type = %s LIMIT %s",(type, limit))
    return cursor.fetchall()

def get_one_book(id):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * from books where id = %s", (id,))
    return cursor.fetchone()

def client_is_registered(register_email):
    cursor = connect().cursor()
    cursor.execute("SELECT * from users where client_email = %s",(register_email,))
    return cursor.fetchone()

def register_client(register_name, register_email, register_token):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("INSERT into users (client_name, client_email, token) VALUES (%s, %s, %s) RETURNING *", (register_name, register_email, register_token))
    return cursor.fetchone()

def get_id_with_token(access_token):
    cursor = connect().cursor()
    cursor.execute("SELECT id from users where token = %s", (access_token,))
    connect().commit()
    return cursor.fetchone()

def place_order(book_id, user_id, quantity):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("INSERT into orders (book_id, user_id, quantity) VALUES (%s, %s, %s) RETURNING *", (book_id, user_id, quantity))
    return cursor.fetchone()

def select_all_orders(user_id):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * from orders where user_id = %s", (user_id,))
    return cursor.fetchall()

def select_one_order(user_id, order_id):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * from orders where id = %s and user_id = %s", (order_id, user_id))
    return cursor.fetchone()

def update_order(new_quantity, user_id, order_id):
    cursor = connect().cursor(cursor_factory=RealDictCursor)
    cursor.execute("UPDATE orders set quantity = %s where user_id = %s and id = %s RETURNING *", (new_quantity, user_id, order_id))
    connect().commit()
    return cursor.fetchone()

def delete_one_order(user_id, order_id):
    cursor = connect().cursor()
    cursor.execute("DELETE from orders where user_id = %s and id = %s",(user_id, order_id))
    connect().commit()
    count = cursor.rowcount
    return count 



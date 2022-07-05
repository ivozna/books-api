import psycopg2
from psycopg2.extras import RealDictCursor

connection = None

def connect():
    global connection
    if connection is None:
        connection = psycopg2.connect(user='booker', password='booker111', host='127.0.0.1', port='1111', database='books')
    return connection

def get_all_books(type=None, limit=None):
    cursor = connect().cursor()
    if type is None:
        cursor.execute("SELECT * from books")
    else:
        cursor.execute("SELECT * from books where type = %s LIMIT %s",(type, limit))
    return cursor.fetchall()

def get_one_book(id):
    cursor = connect().cursor()
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



from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error
import requests


app = Flask(__name__)

DATABASE = 'db/database.db'

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE)
        print('Connection to SQLite DB successful')
    except Error as e:
        print(e)
    return connection

def insert_user(first_name, last_name, age, gender, email, phone, birth_date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO user (first_name, last_name, age, gender, email, phone, birth_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, gender, email, phone, birth_date))
        connection.commit()
        connection.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return get_users()
    elif request.method == 'POST':
        return add_user()

@app.route('/api/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q')
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE first_name LIKE ?", ('%' + query + '%',))
        users = cursor.fetchall()
        connection.close()
        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'age': user[3],
                'gender': user[4],
                'email': user[5],
                'phone': user[6],
                'birth_date': user[7]
            }
            user_list.append(user_dict)
        if not user_list:
            return fetch_and_add_users_from_dummyjson(query)
        return jsonify(user_list)

def fetch_and_add_users_from_dummyjson(query):
    response = requests.get(f"https://dummyjson.com/users/search?q={query}")
    if response.status_code == 200:
        users = response.json()
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            for user in users:
                insert_user(
                    user['first_name'],
                    user['last_name'],
                    user['age'],
                    user['gender'],
                    user['email'],
                    user['phone'],
                    user['birth_date']
                )
            connection.close()
            return jsonify(users)
    return jsonify({'error': 'Error fetching users from dummyjson'})

@app.route('/api/users', methods=['GET'])
def get_users():
    first_name = request.args.get('first_name')  
 
    if first_name:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user WHERE first_name LIKE ?', (f'{first_name}%',))
            users = cursor.fetchall()
            connection.close()
            user_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'first_name': user[1],
                    'last_name': user[2],
                    'age': user[3],
                    'gender': user[4],
                    'email': user[5],
                    'phone': user[6],
                    'birth_date': user[7]
                }
                user_list.append(user_dict)
            return jsonify(user_list)
    else:
        return jsonify({'error': 'Missing mandatory query parameter: first_name'}), 400



def add_user():
    new_user = request.json
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO user (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (new_user['first_name'], new_user['last_name'], new_user['age'], new_user['gender'], new_user['email'], new_user['phone'], new_user['birth_date']))
        connection.commit()
        connection.close()
        return jsonify({'message': 'User added successfully'}), 201


def search_users():
    first_name = request.args.get('first_name')

    if not first_name:
        return jsonify({'error': 'Missing mandatory query parameter: first_name'}), 400

    print("Search for:", first_name)  

    connection = create_connection()
    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM user WHERE LOWER(first_name) LIKE ?", (first_name.lower() + '%',))
        matching_users = cursor.fetchall()

        if matching_users:
            connection.close()
            user_list = []
            for user in matching_users:
                user_dict = {
                    'id': user[0],
                    'first_name': user[1],
                    'last_name': user[2],
                    'age': user[3],
                    'gender': user[4],
                    'email': user[5],
                    'phone': user[6],
                    'birth_date': user[7]
                }
                user_list.append(user_dict)
            return jsonify(user_list)
        else:
            connection.close()
            dummyjson_url = f"https://dummyjson.com/users/search?q={first_name}"
            response = requests.get(dummyjson_url)
            if response.status_code == 200:
                new_users = response.json()
                for user in new_users:
                    insert_user(user['first_name'], user['last_name'], user['age'], user['gender'], user['email'], user['phone'], user['birth_date'])

                connection = create_connection()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM user WHERE LOWER(first_name) LIKE ?", (first_name.lower() + '%',))
                    new_matching_users = cursor.fetchall()
                    connection.close()

                    user_list = []
                    for user in new_matching_users:
                        user_dict = {
                            'id': user[0],
                            'first_name': user[1],
                            'last_name': user[2],
                            'age': user[3],
                            'gender': user[4],
                            'email': user[5],
                            'phone': user[6],
                            'birth_date': user[7]
                        }
                        user_list.append(user_dict)
                    return jsonify(user_list)
                else:
                    return jsonify({'error': 'Failed to fetch users from DummyJSON API'}), 500
            else:
                return jsonify({'error': 'Failed to fetch users from DummyJSON API'}), 500
if __name__ == '__main__':
    app.run(debug=True)

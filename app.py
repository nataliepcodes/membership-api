from flask import Flask, g, request
from database import get_db

import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('DATABASE')

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/member', methods=['GET'])
def get_members():
    return '<h1>This route returns all the members</h1>'

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return '<h1>This route returns one member</h1>'

@app.route('/member', methods=['POST'])
def add_member():
    new_member_info = request.get_json()
    name = new_member_info['name']
    email = new_member_info['email']
    level = new_member_info['level']

    # test for Postman return: <h1>The name is Alice, the email is alice@whatever.com, and the level is Gold</h1>
    return '<h1>The name is {}, the email is {}, and the level is {}</h1>'.format(name, email, level)

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    return '<h1>This route updates a member by ID</h1>'

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return '<h1>This route removes member by ID</h1>'

if __name__ == '__main__':
    app.run(debug=True)
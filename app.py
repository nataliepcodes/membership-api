from flask import Flask, g, request, jsonify, render_template
from database import get_db
import os

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# TODO 
# Returns all members from the database including their information
@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()
    member_cur = db.execute('SELECT * FROM members')
    all_members = member_cur.fetchall() # returns list of tuples

    # Initialising and empty list to store a list of dictionaries, one dictionary for each member
    member_values = []

    # Build dictionary, array of objects once converted to json
    for member in all_members:
        dictionary = {}
        dictionary['id'] = member['id']
        dictionary['name'] = member['name']
        dictionary['email'] = member['email']
        dictionary['level'] = member['level']

        member_values.append(dictionary)

    return jsonify({'members' : member_values}) # returns json object

# TODO 
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return '<h1>This route returns one member</h1>'

# Adds member to the database
@app.route('/member', methods=['POST'])
def add_member():
    new_member_info = request.get_json() # gets data from Postman

    name = new_member_info['name']
    email = new_member_info['email']
    level = new_member_info['level']

    # Adding data to db
    db = get_db()
    db.execute('INSERT INTO members (name, email, level) VALUES (?, ?, ?)', [name, email, level])
    db.commit()

    # Querying data from db
    member_cur = db.execute('SELECT id, name, email, level WHERE name = ?', [name])
    new_member = member_cur.fetchone()

    # test for Postman return: <h1>The name is Alice, the email is alice@whatever.com, and the level is Gold</h1>
    # return '<h1>The name is {}, the email is {}, and the level is {}</h1>'.format(name, email, level)
    
    # Building a json object
    return jsonify({'id' : new_member['id'], 'name' : new_member['name'], 'email' : new_member['email'], 'level' : new_member['level']})

# TODO 
@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    return '<h1>This route updates a member by ID</h1>'


# TODO 
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return '<h1>This route removes member by ID</h1>'


if __name__ == '__main__':
    app.run(debug=True)
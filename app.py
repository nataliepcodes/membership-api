from flask import Flask, g, request, jsonify
from database import get_db
from functools import wraps
import os


app = Flask(__name__)

# API authentification
api_username = os.getenv('USERNAME')
api_password = os.getenv('PASSWORD')


# Authentification decorator function 
def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        else:
            return jsonify({'error' : 'Authentification failed.'}), 403  # Goal: 200 OK in GREEN
        
    return decorated


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Returns all members from the database including their information
# TODO: You usually return a paginated list. Imagine your DB has 10_000 members, and you try to send them all back to the client...
# It will take a long time to send it and the client most likely will not need all of them.
# You could also use LIMIT in your query, where the number comes from the client.
# EX.: Client sends 10, the query becomes SELECT * FROM members LIMIT 10
# The idea is to never send your whole DB to the client. Send chunks of data via paginated list and let the client decide if he wants more or not.
@app.route('/members', methods=['GET'])
@protected
def get_members():
    db = get_db()
    member_cur = db.execute('SELECT * FROM members')
    all_members = member_cur.fetchall()  # returns list of tuples

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
    
    return jsonify({'members' : member_values}) 


# Returns one member by id
# TODO: What happens if I send an invalid member_id like -1, -2, -1200?
# What happens if I send a valid member_id that doesn't exist in the DB like 99999999?
@app.route('/members/<int:member_id>', methods=['GET'])
@protected
def get_member(member_id):

    # Process: get one member information from db by member id
    db = get_db()
    member_cur = db.execute('SELECT id, name, email, level FROM members WHERE id = ?', [member_id])
    member = member_cur.fetchone()

    # Return: json object, list of dictionaries
    return jsonify({'member' : {'id' : member['id'], 'name' : member['name'], 'email' : member['email'], 'level' : member['level']}})


# Adds member to the database
# TODO: Looking at the schema.sql I noticed that only the id is UNIQUE (via PRIMARY KEY).
# What happens if I save 10 members that have the same name, email and level?
# You'll end up with 10 members with 10 different ids. I suggest you make the email UNIQUE
# This is for later: What happens if I send an empty string "" or a blank string "    "? You will want some validation for each endpoint.
@app.route('/members', methods=['POST'])
@protected
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
    
    # Return: json object, list of dictionaries
    return jsonify({'member' : {'id' : new_member['id'], 'name' : new_member['name'], 'email' : new_member['email'], 'level' : new_member['level']}})


# Updates member data
# TODO: What happens if the member_id is not present in the DB?
@app.route('/members/<int:member_id>', methods=['PUT', 'PATCH'])  # PATCH is for partial update of resource, PUT is for full update/all fields
@protected
def edit_member(member_id):
    new_member_info = request.get_json()

    # Updating data
    name = new_member_info['name']
    email = new_member_info['email']
    level = new_member_info['level']

    # Adding updated data to db
    db = get_db()
    db.execute('UPDATE members SET name = ?, email = ?, level = ? WHERE id = ?', [name, email, level, member_id])
    db.commit()

    # Querying updated data from the db
    member_cur = db.execute('SELECT id, name, email, level FROM members WHERE id = ?', [member_id])
    updated_member = member_cur.fetchone()

    # Return json object, list of dictionaries
    return jsonify({'member' : {'id' : updated_member['id'], 'name' : updated_member['name'], 'email' : updated_member['email'], 'level' : updated_member['level']}})


# Delete member from the db
# TODO: What happens if the member_id is not present in the DB?
@app.route('/members/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    db.execute('DELETE FROM members WHERE id = ?', [member_id])
    db.commit()

    return jsonify({'message' : 'The member has been deleted.'})


if __name__ == '__main__':
    app.run(debug=True)
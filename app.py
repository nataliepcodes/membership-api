from flask import Flask, g

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
    return '<h1>This route adds a new member</h1>'

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    return '<h1>This route updates a member by ID</h1>'

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return '<h1>This route removes member by ID</h1>'

if __name__ == '__main__':
    app.run(debug=True)
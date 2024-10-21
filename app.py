from flask import Flask

app = Flask(__name__)

@app.route('/members', methods=['GET'])
def get_members():
    return '<h1>This route returns all the members</h1>'

if __name__ == '__main__':
    app.run(debug=True)
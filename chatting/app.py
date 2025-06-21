# Combined Flask Chat App with Login/Register, MongoDB, SocketIO, and Styled UI

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chatdb'
mongo = PyMongo(app)
socketio = SocketIO(app)
connected_users = {}

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect('/chat')
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    if data['password'] != data['confirm_password']:
        return redirect('/register')
    hash_pass = generate_password_hash(data['password'])
    mongo.db.users.insert_one({
        'full_name': data['full_name'],
        'username': data['username'],
        'password': hash_pass
    })
    return redirect('/')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template('index.html', username=session['username'])

# Socket Events
@socketio.on('join')
def handle_join(username):
    connected_users[username] = {'name': username, 'active': True}
    emit('update_users', list(connected_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user = session.get('username')
    if user and user in connected_users:
        connected_users[user]['active'] = False
    emit('update_users', list(connected_users.values()), broadcast=True)

@socketio.on('send_request')
def handle_request(data):
    emit('receive_request', {'from': data['from']}, broadcast=True)

@socketio.on('new_private_message')
def handle_message(data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['timestamp'] = timestamp
    emit('new_private_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

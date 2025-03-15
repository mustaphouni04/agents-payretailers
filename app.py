from flask import Flask, render_template, request, redirect, session
import hashlib
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {"users": []}

def save_users(users_data):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/registration', methods=['GET'])
def register_page():
    return render_template('registration.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hash_password(password)

    users_data = load_users()
    users = users_data["users"]

    user = next((u for u in users if u['email'] == email), None)

    if user:  # User exists
        if user['password'] == hashed_password:
            session['user_id'] = email  # Store email as user ID
            return redirect('/survey')
        else:
            return "Incorrect password"
    else:  # User doesn't exist, create new user
        new_user = {'email': email, 'password': hashed_password}
        users.append(new_user)
        save_users(users_data)
        session['user_id'] = email
        return redirect('/survey')

@app.route('/survey', methods=['GET'])
def survey():
    if 'user_id' in session:
        return render_template('survey.html')
    else:
        return redirect('/')
    
@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    if 'user_id' in session:
        email = session['user_id']
        name = request.form['name']
        sex = request.form['sex']
        country = request.form['country']

        users_data = load_users()
        users = users_data["users"]

        for user in users:
            if user['email'] == email:
                user['name'] = name
                user['sex'] = sex
                user['country'] = country
                save_users(users_data)
                return 'OK'

        return 'User not found', 404
    else:
        return redirect('/')

@app.route('/main', methods=['GET'])
def main_page():
    if 'user_id' in session:
        return render_template('main.html')
    else:
        return redirect('/')

@app.route('/conversation', methods=['GET'])
def conversation_page():
    if 'user_id' in session:
        return "Conversation page"
    else:
        return redirect('/')

@app.route('/management', methods=['GET'])
def management_page():
    if 'user_id' in session:
        return "Management page"
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
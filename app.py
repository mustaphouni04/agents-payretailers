from flask import Flask, render_template, request, redirect, session, jsonify
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
    
@app.route('/get_user_name', methods=['GET'])
def get_user_name():
    """Returns the logged-in user's name as JSON."""
    print(f"Session data: {session}")
    if 'user_id' in session:
        email = session['user_id']
        users_data = load_users()
        users = users_data["users"]
        user = next((u for u in users if u['email'] == email), None)
        if user and 'name' in user:
            return jsonify({'name': user['name']})
        else:
            # Handle the case where the user or name is not found
            if user: #user exists, but name does not.
                return jsonify({'name': 'Usuario'}), 200 #return a default name.
            else: #user does not exist.
                 return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/conversation', methods=['GET'])
def chat_page():
    return render_template('chat.html')

@app.route('/chat_bot', methods=['POST'])
def chat_bot():
    message = request.form['message']
    # Call your chatbot program here and get the response
    bot_response = get_bot_response(message) # Implement this function
    return bot_response

def get_bot_response(user_message):
    # This is where you integrate your chatbot program
    # Example:
    # from your_chatbot_module import get_response
    # bot_response = get_response(user_message)
    # Replace the following with your actual chatbot logic
    return f"Bot: {user_message} (Response from bot)"


@app.route('/management', methods=['GET'])
def management_page():
    if 'user_id' in session:
        return render_template('management.html')
    else:
        return redirect('/')

@app.route('/get_paperwork_data', methods=['GET'])
def get_paperwork_data():
    if 'user_id' in session:
        email = session['user_id']
        users_data = load_users()
        users = users_data["users"]
        user = next((u for u in users if u['email'] == email), None)
        if user and 'paperwork' in user:
            return jsonify(user['paperwork'])
        else:
            return jsonify([])  # Return empty list if no paperwork data
    else:
        return redirect('/')

@app.route('/paperwork_details/<int:paperwork_id>', methods=['GET'])
def paperwork_details(paperwork_id):
    if 'user_id' in session:
        email = session['user_id']
        users_data = load_users()
        users = users_data["users"]
        user = next((u for u in users if u['email'] == email), None)
        if user and 'paperwork' in user:
            paperwork = next((p for p in user['paperwork'] if p['id'] == paperwork_id), None)
            if paperwork:
                return render_template('paperwork_details.html', paperwork=paperwork)
            else:
                return "Paperwork not found", 404
        else:
            return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
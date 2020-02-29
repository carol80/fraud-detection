import pyrebase
from flask import render_template, request, redirect, session
from app import app
import os

with open(r'C:\Users\Lenovo\Downloads\Documents\GitHub\fraud-detection\flask-api\app\credentials.txt','r') as f:
    f = f.read()
    print(f)
    apiKey, authDomain, databaseURL, projectId, storageBucket, messagingSenderId, appId  = f.split('')



config = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "databaseURL": databaseURL,
    "projectId": projectId,
    "storageBucket": storageBucket,
    "messagingSenderId":messagingSenderId,
    "appId": appId
}

# config = {
#     "apiKey": 'AIzaSyBILL-uNW2CobJgPwvUOMX6KRLAoTqvaWY',
#     "authDomain": 'sabboo-8128e.firebaseapp.com',
#     "databaseURL": 'https://sabboo-8128e.firebaseio.com',
#     "projectId": 'sabboo-8128e',
#     "storageBucket": 'sabboo-8128e.appspot.com',
#     "messagingSenderId":'641426294856',
#     "appId": '1:641426294856:web:86e396fa1eaf85328cb07d '
# }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return render_template('home.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('index.html')
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('index.html')
    return render_template('forgot_password.html')

@app.route('/inbox', methods=['GET'])
def read():
    try:
        # Check if ID was passed to URL query
        messages = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

    # return render_template('home.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()

import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from fetch_email import fetch_messages 

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
emails = db.collection('emailwa')


# @app.route('/')
# @app.route('/index', methods=['GET', 'POST'])
# def index():
#     if (request.method == 'POST'):
#             email = request.form['name']
#             password = request.form['password']
#             try:
#                 auth.sign_in_with_email_and_password(email, password)
#                 #user_id = auth.get_account_info(user['idToken'])
#                 #session['usr'] = user_id
#                 return render_template('home.html')
#             except:
#                 unsuccessful = 'Please check your credentials'
#                 return render_template('index.html', umessage=unsuccessful)
#     return render_template('index.html')

# @app.route('/create_account', methods=['GET', 'POST'])
# def create_account():
#     if (request.method == 'POST'):
#             email = request.form['name']
#             password = request.form['password']
#             auth.create_user_with_email_and_password(email, password)
#             return render_template('index.html')
#     return render_template('create_account.html')

# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if (request.method == 'POST'):
#             email = request.form['name']
#             auth.send_password_reset_email(email)
#             return render_template('index.html')
#     return render_template('forgot_password.html')

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



def spam(mails = "", spam = "1"):
    data = db.get()
    return json.dumps(data.val())

@app.route('/spam', methods=['GET'])
def get_spam():
    response = spam()
    if response != "null":
        return response
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


def inbox(mails = "", spam = "0"):
    data = db.get()
    return json.dumps(data.val())

@app.route('/inbox', methods=['GET'])
def get_inbox():
    response = inbox()
    if response != "null":
        return response
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)

def putMail(name):
    db.child(name).set("")

@app.route('/', methods=['POST'])
def create_mail():
    if not request.json or not 'mail' in request.json:
        abort(400)
    putMail(request.json['mail'])
    return jsonify({'catalogo': request.json['catalogo']}), 201



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)

import os
from flask import Flask, request, jsonify
import json
from firebase_admin import credentials, firestore, initialize_app
from fetch_email import fetch_messages,cloud

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
emails = db.collection('emailwa')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/index', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        message_list, old_id = get_messages_list(service)
        get_messages(service, message_list, old_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


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

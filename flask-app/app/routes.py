import os
from flask import Flask, request, jsonify, make_response, render_template
import json
from firebase_admin import credentials, firestore, initialize_app
from fetch_email import fetch_messages,cloud,config

app = Flask(__name__)


@app.route('/index', methods=['GET','POST'])
def create():
    try:
        service = fetch_messages.authenticate()
        message_list, old_id = fetch_messages.get_messages_list(service)
        fetch_messages.get_messages(service, message_list, old_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


def spam():
    data = config.db.collection(u"emailwa").where(u'spam',u'==',1).stream()
    return data

@app.route('/spam', methods=['GET'])
def get_spam():
    response = spam()
    my_dict = [ el.to_dict() for el in response ]
    if response != "null":
        return render_template('spam.html', saves=my_dict)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


def inbox():
    data = config.db.collection(u"emailwa").where(u'spam',u'==',0).stream()
    return data

@app.route('/inbox', methods=['GET'])
def get_inbox():
    response = inbox()
    my_dict = [ el.to_dict() for el in response ]
    print(my_dict)
    if response != "null":
        return render_template('inbox.html', saves=my_dict)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)

# def putMail(name):
#     config.db.child(name).set("")

# @app.route('/', methods=['POST'])
# def create_mail():
#     if not request.json or not 'mail' in request.json:
#         abort(400)
#     putMail(request.json['mail'])
#     return jsonify({'catalogo': request.json['catalogo']}), 201



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)

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


def spamfun():
    data = config.db.collection(u"emailwa").where(u'spam',u'==',1).stream()
    return data

@app.route('/spam', methods=['GET'])
def get_spam():
    spam = spamfun()
    my_spam = [ el.to_dict() for el in spam ]
    if spam != "null":
        return render_template('spam.html', saves=my_spam)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


def inboxfun():
    data = config.db.collection(u"emailwa").where(u'spam',u'==',0).stream()
    return data

@app.route('/inbox', methods=['GET'])
def get_inbox():
    inbox = inboxfun()
    my_ham = [ el.to_dict() for el in inbox ]
    if inbox != "null":
        return render_template('inbox.html', saves=my_ham)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/analysis', methods=['GET'])
def analysis():
    ham = config.db.collection(u"emailwa").where(u'spam', u'==', 0).stream()
    spam = config.db.collection(u"emailwa").where(u'spam', u'==', 1).stream()
    ham_mails = [ el.to_dict() for el in ham ]
    spam_mails = [ el.to_dict() for el in spam ]
    totalspam = len(spam_mails)
    totalham = len(ham_mails)
    total = totalspam + totalham
    chart1_from = []
    chart1_count = []
    chart1_cow = []
    chart1_tow = []
    chart1_to = []
    chart1_frome = []

    for i in range(0,totalspam):
        chart1_to.append(spam_mails[i]['from'])
    chart1_from = list(set(chart1_to))
    print(chart1_from)

    for i in range(0,totalham):
        chart1_tow.append(ham_mails[i]['from'])
    chart1_frome = list(set(chart1_tow))

    chart1_count = [0]*len(chart1_from)
    chart1_cow = [0]*len(chart1_frome)

    unique_user = len(list(set(chart1_from + chart1_frome)))

    for i in range(0,len(chart1_from)):
        chart1_count[i] = chart1_to.count(chart1_to[i])

    for i in range(0,len(chart1_frome)):
        chart1_cow[i] = chart1_tow.count(chart1_tow[i])

    dick = {
        "totalspam":totalspam ,
        "totalham":totalham,
        "total":total,
        "unique_user":unique_user
    }
    if dick != "null":
        return render_template('analtics.html', data=dick)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/plotly', methods=['GET'])
def ssup():
    return render_template('plotly_heatmap.html')


@app.route('/getData', methods=['GET'])
def anal():
    ham = config.db.collection(u"emailwa").where(u'spam', u'==', 0).stream()
    spam = config.db.collection(u"emailwa").where(u'spam', u'==', 1).stream()
    ham_mails = [ el.to_dict() for el in ham ]
    spam_mails = [ el.to_dict() for el in spam ]
    totalspam = len(spam_mails)
    totalham = len(ham_mails)
    chart1_from = []
    chart1_frome = []
    chart1_to = []
    chart1_tow = []

    for i in range(0,totalspam):
        from_addr = spam_mails[i]['from']
        list1 = from_addr.split(' ')
        sender = list1[0]
        chart1_to.append(sender)
    chart1_from = list(set(chart1_to))
    print(chart1_from)

    for i in range(0,totalham):
        from_addr = ham_mails[i]['from']
        list1 = from_addr.split(' ')
        sender = list1[0]
        chart1_tow.append(sender)
    chart1_frome = list(set(chart1_tow))

    chart1_count = [0]*len(chart1_from)
    chart1_cow = [0]*len(chart1_frome)

    for i in range(0,len(chart1_from)):
        chart1_count[i] = chart1_to.count(chart1_to[i])

    for i in range(0,len(chart1_frome)):
        chart1_cow[i] = chart1_tow.count(chart1_tow[i])

    dick = {
        "emails":chart1_frome,
        "emailSpam":chart1_count,
        "emailHam":chart1_cow
    }
    print(dick)
    if dick != "null":
        return dick
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/heatmap', methods=['GET'])
def doggy():
    ham = config.db.collection(u"emailwa").where(u'spam', u'==', 0).stream()
    spam = config.db.collection(u"emailwa").where(u'spam', u'==', 1).stream()
    ham_mails = [ el.to_dict() for el in ham ]
    spam_mails = [ el.to_dict() for el in spam ]
    totalspam = len(spam_mails)
    totalham = len(ham_mails)
    chart1_from = []
    chart1_frome = []
    chart1_to = []
    chart1_tow = []

    for i in range(0,totalspam):
        from_addr = spam_mails[i]['from']
        list1 = from_addr.split(' ')
        sender = list1[0]
        chart1_to.append(sender)
    chart1_from = list(set(chart1_to))
    print(chart1_from)

    for i in range(0,totalham):
        from_addr = ham_mails[i]['from']
        list1 = from_addr.split(' ')
        sender = list1[0]
        chart1_tow.append(sender)
    chart1_frome = list(set(chart1_tow))

    chart1_count = [0]*len(chart1_from)
    chart1_cow = [0]*len(chart1_frome)

    for i in range(0,len(chart1_from)):
        chart1_count[i] = chart1_to.count(chart1_to[i])

    for i in range(0,len(chart1_frome)):
        chart1_cow[i] = chart1_tow.count(chart1_tow[i])

    dick = {
        "emails":chart1_frome,
        "emailSpam":chart1_count,
        "emailHam":chart1_cow
    }
    print(dick)
    if dick != "null":
        return dick
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)

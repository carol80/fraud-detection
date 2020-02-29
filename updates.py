from auth import *



#fetching


# add do a variable
db = connect_firebase()

#and now the hard/ easy part that took me a while to figure out:
# notice the value inside the .child, it should be the parent name with all the cats keys
values = db.child('cats').get()

# adding all to a dataframe you'll need to use the .val()  
data = pd.DataFrame(values.val())


----------------

#fetching spams
docs = db.child('spam').where(u'1', u'==', True).stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

----------------

docs = db.child('spam').where(u'0', u'==', True).stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

----------------------------------



GET

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

-------------------------------------

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

--------------------------------------

POST

def putMail(name):
    db.child(name).set("")

@app.route('/', methods=['POST'])
def create_mail():
    if not request.json or not 'mail' in request.json:
        abort(400)
    putMail(request.json['mail'])
    return jsonify({'catalogo': request.json['catalogo']}), 201


@app.route('/api/v1.0/catalogos/<string:catalogo>', methods=['PUT'])
def create_area(catalogo):
    if not request.json or not 'area' in request.json:
        abort(400)
    putArea(catalogo,request.json['area'])
    return jsonify({'area': request.json['area']}), 201

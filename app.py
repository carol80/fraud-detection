from flask import Flask,url_for, request, jsonify
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from firebase_admin import credentials, firestore, initialize_app
from sklearn.multiclass import *
from sklearn.svm import *
import json

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
emails = db.collection('emailwa')


def get_predict(text):
	try:
		if len(text) > 0:
			vectorize_message = vectorizer.transform([text])
			predict = model.predict(vectorize_message)[0]
		else:
			predict = 1
	except BaseException as inst:
		error = str(type(inst).__name__) + ' ' + str(inst)
	
	return predict

app = Flask(__name__)


# train model
model = pickle.load(open('models/PassiveAggressiveClassifier_with_TfidfVectorizer.pkl', 'rb'))
vectorizer = pickle.load(open('vectors/TfidfVectorizer.pkl', 'rb'))

def putMail(name):
    db.child(name).set("")

def fetch(x):
	predict = get_predict(x)
	return predict


@app.route('/', methods=['POST'])
def main():
	data = request.get_json()
	docs = data['from']
	body = db.child("body").where(u'from', u'==', docs).stream()
	for x in body:
		data['spam'] = fetch(x)
		putMail(data['spam'])
	

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True, threaded=True)
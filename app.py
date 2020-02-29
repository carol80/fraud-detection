from flask import Flask,url_for, request, jsonify
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import *
from sklearn.svm import *
import json

def get_predict(text):
	try:
		if len(text) > 0:
			vectorize_message = vectorizer.transform([text])
			predict = model.predict(vectorize_message)[0]
		else:
			predict = 2
	except BaseException as inst:
		error = str(type(inst).__name__) + ' ' + str(inst)
	
	return predict

app = Flask(__name__)


# train model
model = pickle.load(open('models/PassiveAggressiveClassifier_with_TfidfVectorizer.pkl', 'rb'))
vectorizer = pickle.load(open('vectors/TfidfVectorizer.pkl', 'rb'))

@app.route('/', methods=['PUT'])
def main():
	data = request.get_json()
	body = data['body']
	predict = get_predict(body)
	data['spam'] = predict
	response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
	

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True, threaded=True)
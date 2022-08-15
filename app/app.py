import pickle
import flask
from flask import Flask, render_template, json, jsonify, request

import os
from flask import request
import joblib
import pandas as pd


app = Flask(__name__)
lin_reg_model = pickle.load(open('app\models\Linear_Regression_Model.pkl', 'rb'))

@app.route('/')
def index():
	return render_template('index.html')

# Get first four rows of test data
@app.route('/data/test', methods=['GET'])
def get():
	data = pd.read_csv('./data/test.csv')
	print(data.head(4))
	return(data.head(4).to_json(orient='records'))


@app.route('/predict', methods=['POST'])
def predict():

	data = request.get_json()
	
	formatInput(data)
	
	print(data)

	data = [float(x) for x in data.values()]

	# Predict
	prediction = lin_reg_model.predict([data])
	prediction = int(prediction.round())

	if (prediction == 1):
		prediction = "Yes"
	else:
		prediction = "No"

	prediction = {'Prediction': prediction}

	# Return prediction
	return jsonify(prediction)

@app.route('/accuracy', methods=['GET'])
def accuracy():
	# read content from file
	with open('./models/accuracy.txt', 'r') as f:
		data = f.read().split(':')[1]
		
		data = int(float(data))
		accuracy = {'Accuracy': data}
		return jsonify(accuracy)


def formatInput(input):

	input.pop("Loan_ID")
	# Format the gender
	if (input["Gender"] == 'Female'):
		input["Gender"] = 0
	else:
		input["Gender"] = 1
	
	# Format Married
	if (input["Married"] == "No"):
		input["Married"] = 0
	else:
		input["Married"] = 1
	
	# Format Education
	if (input["Education"] == 'Not Graduate'):
		input["Education"] = 0
	else:
		input["Education"] = 1

	# Format Self_Employed
	if (input["Self_Employed"] == 'No'):
		input["Self_Employed"] = 0
	else:
		input["Self_Employed"] = 1
	
	# Format Property_Area
	if (input["Property_Area"] == 'Rural'):
		input["Property_Area"] = 0
	elif (input["Property_Area"] == 'Semiurban'):
		input["Property_Area"] = 1
	else:
		input["Property_Area"] = 2
	

	

if __name__ == "__main__":
	# port = int(os.environ.get('PORT', 33507))
	app.run(debug=True)
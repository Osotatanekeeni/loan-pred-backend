import pickle
import flask
from flask import Flask, render_template, json, jsonify, request

import os
from flask import request
import joblib

app = Flask(__name__)
lin_reg_model = pickle.load(open('./models/Linear_Regression_Model.pkl', 'rb'))

# Loan ID
# Gender
# Marital Status
# Number of dependents
# Education status
# Employment Status
# Applicant Income
# Co applicant Income
# Loan Amount
# Loan term
# Credit history
# Property Area
@app.route('/')
def index():
	return render_template('index.html')

# Get first four rows of test data
@app.route('/data/test', methods=['GET'])
def get():
	with open('./data/test.csv', 'r') as f:
		data = f.readlines()[1:5]
		return render_template('index.html', data=data)

@app.route('/predict', methods=['POST'])
def predict():

	data = request.get_json()

	# Format the data
	formatInput(data)
	
	print(data)

	data = [float(x) for x in data.values()]

	# Predict
	prediction = lin_reg_model.predict([data])

	# Return prediction
	return render_template('index.html', prediction=int(prediction.round()))

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
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
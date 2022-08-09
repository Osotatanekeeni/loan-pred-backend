from flask import Flask, render_template, json, jsonify, request
import flask
import os
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

# Create a get enpoint to get the first four rows of the file train.csv and display it in index.html
# Add a variable to the template file index.html to display the data
@app.route('/data/test', methods=['GET'])
def get():
	with open('./data/train.csv', 'r') as f:
		data = f.readlines()[1:5]
		return render_template('index.html', data=data)




if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
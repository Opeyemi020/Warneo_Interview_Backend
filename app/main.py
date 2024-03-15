import helper
from flask import Flask, request, Response
import json
from flask_sqlalchemy import SQLAlchemy
import os

based = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(based, 'database.db')
db = SQLAlchemy(app)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

@app.route('/item/new', methods=['POST'])
def add_item():

    request_data = request.get_json() 
    item = request_data['item']

    response_data = helper.add_to_list(item)

    if response_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response
   
    response = Response(json.dumps(response_data), mimetype='application/json')
    return response


@app.route('/items/all')
def get_all_items():
    
    response_data = helper.get_all_items()

    response = Response(json.dumps(response_data), mimetype='application/json')
    return response


@app.route('/item/status', methods=['GET'])
def get_item():
    item_name = request.args.get('name')

    status = helper.get_item(item_name)

    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
        return response

    
    response_data = {
        'status': status
    }

    response = Response(json.dumps(response_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['PUT'])
def update_status():
    
    request_data = request.get_json()
    item = request_data['item']
    status = request_data['status']

    response_data = helper.update_status(item, status)

    if response_data is None:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(response_data), mimetype='application/json')

    return response


@app.route('/item/remove', methods=['DELETE'])
def delete_item():
   
    request_data = request.get_json()
    item = request_data['item']

    response_data = helper.delete_item(item)

    if response_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(response_data), mimetype='application/json')

    return response
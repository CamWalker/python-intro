from flask import Flask, jsonify, request, Response
import json, jwt, datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-little-secret'

books = [
  {
    'id': 1,
    'name': '1234',
    'price': 3.59,
  }, {
    'id': 2,
    'name': '5678',
    'price': 7.99,
  }
]

# 
# AUTH
# 

@app.route('/login')
def get_token():
  expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
  token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
  return token

def token_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    token = request.args.get('token')
    try:
      jwt.decode(token, app.config['SECRET_KEY'])
      return f(*args, **kwargs)
    except:
      return jsonify({'error': 'Need a valid token to view this data'}), 401
  return wrapper

# 
# GET
# 

@app.route('/books')
@token_required
def get_books():
  return jsonify({ 'books': books })

@app.route('/books/<int:id>')
@token_required
def get_book_by_id(id):
  return_value = {}
  for book in books:
    if book['id'] == id:
      return_value = book
  return jsonify(return_value)

# 
# POST
# 

@app.route('/books', methods=['POST'])
@token_required
def add_book():
  books.insert(0, request.get_json())
  response = Response("", 201, mimetype='application/json')
  return response

# 
# PUT
# 

@app.route('/books/<int:id>', methods=['PUT'])
@token_required
def edit_book(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['name'] = newBook['name']
      book['price'] = newBook['price']
  response = Response("", 200, mimetype='application/json')
  return response

# 
# PATCH
# 

@app.route('/books/<int:id>/price', methods=['PATCH'])
@token_required
def edit_book_price(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['price'] = newBook['price']
  response = Response("", 200, mimetype='application/json')
  return response

@app.route('/books/<int:id>/name', methods=['PATCH'])
@token_required
def edit_book_name(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['name'] = newBook['name']
  response = Response("", 200, mimetype='application/json')
  return response

# 
# DELETE
# 

@app.route('/books/<int:id>', methods=['DELETE'])
@token_required
def delete_book(id):
  i = 0
  response = Response(json.dump('cannot delete that id'), 400, mimetype='application/json')
  for book in books:
    if book['id'] == id:
      books.pop(i)
      response = Response("", 200, mimetype='application/json')
    i += 1
  return response

app.run(port=5000)
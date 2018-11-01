from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

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

@app.route('/books')
def get_books():
  return jsonify({ 'books': books })

@app.route('/books/<int:id>')
def get_book_by_id(id):
  return_value = {}
  for book in books:
    if book['id'] == id:
      return_value = book
  return jsonify(return_value)

@app.route('/books', methods=['POST'])
def add_book():
  books.insert(0, request.get_json())
  response = Response("", 201, mimetype='application/json')
  return response

@app.route('/books/<int:id>', methods=['PUT'])
def edit_book(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['name'] = newBook['name']
      book['price'] = newBook['price']
  response = Response("", 200, mimetype='application/json')
  return response

@app.route('/books/<int:id>/price', methods=['PATCH'])
def edit_book_price(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['price'] = newBook['price']
  response = Response("", 200, mimetype='application/json')
  return response

@app.route('/books/<int:id>/name', methods=['PATCH'])
def edit_book_name(id):
  newBook = request.get_json()
  for book in books:
    if book['id'] == id:
      book['name'] = newBook['name']
  response = Response("", 200, mimetype='application/json')
  return response

@app.route('/books/<int:id>', methods=['DELETE'])
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
from flask import request, jsonify

from app import app
from app import db
from app.models import Books


# 获取所有书籍信息
@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = Books.query.all()
    return jsonify([book.serialize() for book in books])


# 根据id获取特定书籍信息
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book: Books = Books.query.get(book_id)
    return jsonify([book.serialize()])


# 更新书籍信息
@app.route('/api/books/<int:book_id>', methods=['POST'])
def update_book(book_id):
    # 从请求中获取数据
    data = request.form
    bookname = data.get('bookname')
    author = data.get('author')
    publisher = data.get('publisher')
    isbn = data.get('isbn')
    totalquantity = data.get('totalquantity')
    remainingquantity = data.get('remainingquantity')

    # 查找指定的书籍
    book = Books.query.get(book_id)

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    # 更新书籍信息
    book.book_title = bookname if bookname else book.book_title
    book.author = author if author else book.author
    book.publisher = publisher if publisher else book.publisher
    book.ISBN = isbn if isbn else book.ISBN
    book.total_quantity = int(totalquantity) if totalquantity else book.total_quantity
    book.remaining_quantity = int(remainingquantity) if remainingquantity else book.remaining_quantity

    db.session.commit()

    # 返回成功响应
    return jsonify(book.serialize()), 200


@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Books(
        book_title=data['book_title'],
        author=data['author'],
        publisher=data['publisher'],
        ISBN=data['ISBN'],
        total_quantity=data['total_quantity'],
        remaining_quantity=data['remaining_quantity']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.serialize()), 201


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return '', 204

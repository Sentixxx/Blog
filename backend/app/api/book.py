
from flask import Blueprint , request

from app.models import BookInstance
from app.models import Book
from uuid import uuid4
book = Blueprint('book',__name__)

@book.route('/search',methods=['GET'])
def on_login():
    data = request.args.to_dict()
    pass
    
@book.route('/lend',methods=['POST'])
def on_lend():
    pass

@book.route('/return',methods=['POST'])
def on_return():
    pass

@book.route('/add',methods=['POST'])
def on_add():
    data = request.args.to_dict()
    book_isbn = data.get('isbn')
    location = data.get('location')
    code = uuid4()
    while BookInstance.query.filter_by(book_instance_id=code).first():
        code = uuid4()
    result = Book.query.filter_by(book_isbn_code=book_isbn).first()
    if(result):
        result.book_cur_stock_num += 1
        if not result.save():
            return "add book failed , try later" , 431
        newBookInstance = BookInstance(book_instance_id = code,book_id=result.book_id,book_instance_location=location,book_isbn_code=book_isbn)
        if not newBookInstance.save():
            return "add book instance failed , try later" , 431
        return "add book success" , 200
    else:
        press = data.get('press')
        author = data.get('author')
        name = data.get('name')
        book_type = data.get('type')
        newBook = Book(book_name=name,book_author=author,book_press=press,book_isbn_code=book_isbn,book_type=book_type,book_cur_stock_num=1)
        if not newBook.save():
            return "add book failed , try later" , 431
        newBookInstance = BookInstance(book_instance_id = code,book_id=newBook.book_id,book_instance_location=location,book_isbn_code=book_isbn)
        if not newBookInstance.save():
            return "add book instance failed , try later" , 431
        return "add book success" , 200


@book.route('/delete',methods=['POST'])
def on_delete():
    pass

@book.route('/modify',methods=['POST'])
def on_modify():
    pass

@book.route('/exist',methods=['GET'])
def if_exist():
    pass



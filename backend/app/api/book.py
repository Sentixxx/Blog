
from flask import Blueprint , request
from app.extensions import db
from app.models import BookInstance , add_book_instance, delete_book_instance
from app.models import Book , add_book, delete_book
from uuid import uuid4
from app.utils import submit
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

    sess = db.session()

    sess , result = add_book(data,sess)
    sess , code = add_book_instance(data,result,sess)

    if not submit(sess):
        return "add failed , try later" , 431
    return str(code) , 200



@book.route('/delete',methods=['POST'])
def on_delete():
    data = request.args.to_dict()

    sess = db.session()
    code = data.get('code')
    
    sess , ret = delete_book_instance(sess,code)
    if ret is False:
        return "delete failed, no such book instance!" , 431
    
    sess , ret = delete_book(sess,ret.book_id)
    if ret is False:
        return "delete failed, no such book!" , 431
    
    if not submit(sess):
        return "delete failed , try later" , 431
    return "delete success" , 200



@book.route('/modify',methods=['POST'])
def on_modify():
    pass

@book.route('/exist',methods=['GET'])
def if_exist():
    pass



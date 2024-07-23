
from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_json
from app.utils import submit
book = Blueprint('book',__name__)

@book.route('/search',methods=['GET'])
def on_login():
    data = request.args.to_dict()

    results = Book.query.filter(Book.book_name.like('%' + data.get('name') + '%')).all()
    if not results:
        return "no such book" , 200
    return to_json(results) , 200
    

@book.route('/detail',methods=['GET'])
def on_detail():
    data = request.args.to_dict()
    results = BookInstance.query.filter_by(book_id=data.get('id')).all()
    if not results:
        return "no such book instance", 200
    return to_json(results), 200
    
@book.route('/lend',methods=['POST'])
def on_lend():
    data = request.args.to_dict()

    sess = db.session()

    sess, newBorrow = add_borrow(data,sess)

    data['borrow_id'] = newBorrow.borrow_id
    sess, newBookInstance = update_book_instance(data,sess)
    if newBookInstance is False:
        return "lend failed, no such book instance!" , 200
    
    

    sess, _ = update_book(data,sess)
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
        return "add failed , try later" , 507
    return str(code) , 200



@book.route('/delete',methods=['POST'])
def on_delete():
    data = request.args.to_dict()

    sess = db.session()

    
    sess , ret = delete_book_instance(data,sess)
    if ret is False:
        return "delete failed, no such book instance!" , 200
    
    sess , ret = delete_book(sess,ret.book_id)
    if ret is False:
        return "delete failed, no such book!" , 200
    
    if not submit(sess):
        return "delete failed , try later" , 507
    return "delete success" , 200



@book.route('/modify',methods=['POST'])
def on_modify():
    pass

@book.route('/exist',methods=['GET'])
def if_exist():
    pass



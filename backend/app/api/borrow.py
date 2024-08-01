from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_dict , submit
from flask import jsonify
from app.services.borrow import delay_borrow

borrow = Blueprint('borrow',__name__)

@borrow.route('/info/all',methods=['GET'])
def on_info_all():
    ret = {}

    results = Borrow.query.filter_by(is_deleted=0).all()

    if results:
        ret['results'] = to_dict(results)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "没有借阅记录"
        ret['status'] = -2
    
    return jsonify(ret)

@borrow.route('/info/user_id/<int:user_id>',methods=['GET'])
def on_info_user(user_id):
    ret = {}

    results = Borrow.query.filter(Borrow.is_deleted==0,Borrow.user_instance_id==user_id).all()

    if results:
        ret['results'] = []
        for borrow in results:
            record = borrow.to_dict()
            book_instance = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==borrow.book_instance_id).first()
            book = Book.query.filter(Book.is_deleted==0,Book.book_id==book_instance.book_id).first()
            record['book_name'] = book.book_name
            record['book_author'] = book.book_author
            record['book_press'] = book.book_press
            record['book_isbn_code'] = book.book_isbn_code

            ret['results'].append(record)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "没有借阅记录"
        ret['status'] = -2

    return jsonify(ret)

@borrow.route('/info/borrow_id/<int:borrow_id>',methods=['GET'])
def on_info_borrow(borrow_id):
    ret = {}

    result = Borrow.query.filter(Borrow.is_deleted==0,Borrow.borrow_id==borrow_id).first()

    if result:
        ret['results'] = []
        record = result.to_dict()
        book_instance = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==borrow.book_instance_id).first()
        book = Book.query.filter(Book.is_deleted==0,Book.book_id==book_instance.book_id).first()
        record['book_name'] = book.book_name
        record['book_author'] = book.book_author
        record['book_press'] = book.book_press
        record['book_isbn_code'] = book.book_isbn_code

        ret['results'].append(record)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "借阅记录不存在"
        ret['status'] = -2

    return jsonify(ret)

@borrow.route('/info/book_instance_id/<string:book_instance_id>',methods=['GET'])
def on_info_bi(book_instance_id):
    ret = {}

    result = Borrow.query.filter(Borrow.is_deleted==0,Borrow.book_instance_id==book_instance_id).all()

    if result:
        ret['results'] = []
        record = result.to_dict()
        book_instance = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==borrow.book_instance_id).first()
        book = Book.query.filter(Book.is_deleted==0,Book.book_id==book_instance.book_id).first()
        record['book_name'] = book.book_name
        record['book_author'] = book.book_author
        record['book_press'] = book.book_press
        record['book_isbn_code'] = book.book_isbn_code

        ret['results'].append(record)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "借阅记录不存在"
        ret['status'] = -2

    return jsonify(ret)

@borrow.route('/info/book_id/<int:book_id>',methods=['GET'])
def on_info_book(book_id):
    ret = {}

    results = Borrow.query.filter(Borrow.is_deleted==0,Borrow.book_id==book_id).all()

    if results:
        ret['results'] = []
        for borrow in results:
            record = borrow.to_dict()
            book_instance = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==borrow.book_instance_id).first()
            book = Book.query.filter(Book.is_deleted==0,Book.book_id==book_instance.book_id).first()
            record['book_name'] = book.book_name
            record['book_author'] = book.book_author
            record['book_press'] = book.book_press
            record['book_isbn_code'] = book.book_isbn_code
            record['book_pic'] = book.book_pic

            ret['results'].append(record)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "借阅记录不存在"
        ret['status'] = -2

    return jsonify(ret)

@borrow.route('/delay/<int:borrow_id>',methods=['PUT'])
def on_delay(borrow_id):
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = delay_borrow(borrow_id,data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "续借失败：" + ret['results']['error_msg']
    else:
        sess.commit()
        ret['msg'] = "续借成功"
        ret['status'] = 200

    return jsonify(ret)
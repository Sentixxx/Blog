
from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_json,to_dict
from app.utils import submit
from flask import jsonify
book = Blueprint('book',__name__)

@book.route('/search',methods=['GET'])
def on_search():
    data = request.args.to_dict()
    book_name = data.get('book_name')
    book_author = data.get('book_author')
    book_press = data.get('book_press')
    book_isbn_code = data.get('book_isbn_code')
    ret = {}
    query = Book.query
    if book_name is not None:
        query = query.filter(Book.book_name.like('%' + book_name + '%'))
    if book_author is not None:
        query = query.filter(Book.book_author.like('%' + book_author + '%'))
    if book_press is not None:
        query = query.filter(Book.book_press.like('%' + book_press + '%'))
    if book_isbn_code is not None:
        query = query.filter(Book.book_isbn_code.like('%' + book_isbn_code + '%'))
    results = query.all()
    ret['results'] = to_dict(results)
    ret['status'] = 200
    ret['msg'] = "查询成功"
    return jsonify(ret) , 200
    
@book.route('/info',methods=['GET'])
def on_info():
    data = request.args.to_dict()
    ret = {}
    results = Book.query.filter_by(book_id=data.get('book_id')).all()
    ret['results'] = to_dict(results)
    ret['status'] = 200
    ret['msg'] = "查询成功"
    return jsonify(ret) , 200

@book.route('/detail',methods=['GET'])
def on_detail():
    data = request.args.to_dict()
    ret = {}
    results = BookInstance.query.filter_by(book_id=data.get('book_id')).all()
    ret['results'] = to_dict(results)
    ret['status'] = 200
    ret['msg'] = "查询成功"
    return jsonify(ret) , 200
    
@book.route('/lend',methods=['POST'])
def on_lend():
    data = request.args.to_dict()
    data['book_instance_status'] = 1

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess, ret['results'] = add_borrow(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "借阅失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    data['borrow_id'] = ret['results']['borrow_id']

    if ret['results'].get('borrow_id') is None:
        sess.rollback()
        ret['msg'] = "借阅失败，请稍后再试"
        ret['status'] = -2
        return jsonify(ret) , 200

    sess, ret['results'] = borrow_book_instance(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "借阅失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    sess, ret['results'] = delete_book(sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "借阅失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "借阅失败"
        ret['status'] = -2 
    else:
        ret['msg'] = "借阅成功"
        ret['status'] = 200

    return jsonify(ret) , 200

@book.route('/add',methods=['POST'])
def on_add():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    if data.get('book_isbn_code') is not None:
        sess , ret['results'] = add_book(data,sess,ret['results'])
    else:
        ret['results']['book_id'] = data.get('book_id')
    sess , ret['results'] = add_book_instance(data,sess,ret['results'])
    
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "添加失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200

    if not submit(sess):
        ret['msg'] = "添加成功"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "添加成功"
    ret['status'] = 200
    return jsonify(ret) , 200



@book.route('/delete',methods=['DELETE'])
def on_delete():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = delete_book_instance(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "删除失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    sess , ret['results'] = delete_book(sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "删除失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "删除失败，请稍后再试"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "删除成功"
    ret['status'] = 200
    return jsonify(ret) , 200



@book.route('/update',methods=['POST'])
def on_update():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    if data.get('book_instance_id') is not None:
        sess , ret['results'] = update_book_instance(data,sess,ret['results'])

    elif data.get('book_isbn_code') is not None:
        sess , ret['results'] = update_book(data,sess,ret['results'])

    else:
        ret['msg'] = "修改失败：缺少目标"
        ret['status'] = -1
        return jsonify(ret) , 200

    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "修改失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "修改失败，请稍后再试"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "修改成功"
    ret['status'] = 200
    return jsonify(ret) , 200



from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_dict , submit
from flask import jsonify
from app.services.book_instance import add_book_instance, delete_book_instance, update_book_instance, borrow_book, return_book
from app.services.book import reduce_stock_num, add_stock_num

book_instance = Blueprint('book_instance',__name__)

@book_instance.route('/info/all',methods=['GET'])
def on_info_all():
    ret = {}

    results = BookInstance.query.filter_by(is_deleted=0).all()

    if results:
        ret['results'] = to_dict(results)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "没有图书"
        ret['status'] = -2
    
    return jsonify(ret)

@book_instance.route('/info/book_id/<int:book_id>',methods=['GET'])
def on_info_book(book_id):
    ret = {}

    results = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_status==0,BookInstance.book_id==book_id).all()

    if results:
        ret['results'] = to_dict(results)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "图书不存在"
        ret['status'] = -2

    return jsonify(ret)

@book_instance.route('/info/book_instance/<string:book_instance_id>',methods=['GET'])
def on_info_bi(book_instance_id):
    ret = {}

    result = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==book_instance_id).first()

    if result:
        ret['results'] = result.to_dict()
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "图书不存在"
        ret['status'] = -2

@book_instance.route('/borrow',methods=['POST'])
def on_borrow():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = borrow_book(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "借阅失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    

    sess, ret['results'] = reduce_stock_num(data.get('book_id'),sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "借阅失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "借阅失败，请稍后再试"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "借阅成功"
    ret['status'] = 200
    return jsonify(ret) , 200

@book_instance.route('/return',methods=['POST'])
def on_return():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = return_book(data,sess,ret['results'])

    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "归还失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "归还失败，请稍后再试"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "归还成功"
    ret['status'] = 200
    return jsonify(ret) , 200
    

@book_instance.route('/add',methods=['POST'])
def on_add():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = add_book_instance(data,sess,ret['results'])
    
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "添加失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    sess, ret['results'] = add_stock_num(data.get('book_id'),sess,ret['results'])

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

@book_instance.route('/delete/<string:book_instance_id>',methods=['DELETE'])
def on_delete(book_instance_id):
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = delete_book_instance(book_instance_id, data, sess, ret['results'])
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

@book_instance.route('/update/<string:book_instance_id>',methods=['PUT'])
def on_update(book_instance_id):
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = update_book_instance(book_instance_id,data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "更新失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "更新失败"
        ret['status'] = -2
        return jsonify(ret) , 200
    
    ret['msg'] = "更新成功"
    ret['status'] = 200
    return jsonify(ret) , 200
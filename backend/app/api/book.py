
from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_dict
from app.services.book import add_book,update_book,delete_book
from app.utils import submit
from flask import jsonify
book = Blueprint('book',__name__)

@book.route('/info/all',methods=['GET'])
def on_info_all():
    ret = {}

    results = Book.query.filter_by(is_deleted=0).all()

    if results:
        ret['results'] = to_dict(results)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "没有图书"
        ret['status'] = -2
    
    return jsonify(ret) , 200

@book.route('/info/<int:book_id>',methods=['GET'])
def on_info(book_id):
    ret = {}

    result = Book.query.filter(Book.is_deleted==0,Book.book_id==book_id).first()

    if result:
        ret['results'] = result.to_dict()
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "图书不存在"
        ret['status'] = -2
    return jsonify(ret) , 200

@book.route('/search',methods=['GET'])
def on_search():
    print(request)
    data = request.args.to_dict()

    exact_filter = {
        'book_id'
    }
    like_filter = {
        'book_name',
        'book_author',
        'book_press',
        'book_isbn_code',
        'book_type'
    }
    ret = {}

    query = Book.query.filter(Book.is_deleted == 0)

    for field in exact_filter:
        if data.get(field) is not None:
            query = query.filter(getattr(Book,field) == data.get(field))

    for field in like_filter:
        if data.get(field) is not None:
            query = query.filter(getattr(Book,field).like('%'+data.get(field)+'%'))

    results = query.all()

    ret['results'] = to_dict(results)
    ret['status'] = 200
    ret['msg'] = "查询成功"

    return jsonify(ret) , 200

@book.route('/add',methods=['POST'])
def on_add():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = add_book(data,sess,ret['results'])
    
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



@book.route('/delete/<int:book_id>',methods=['DELETE'])
def on_delete(book_id):
    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = delete_book(book_id,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "删除失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    if not submit(sess):
        ret['msg'] = "删除失败"
        ret['status'] = -2
        return jsonify(ret) , 200
    ret['msg'] = "删除成功"
    ret['status'] = 200
    return jsonify(ret) , 200



@book.route('/update/<int:book_id>',methods=['PUT'])
def on_update(book_id):
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess , ret['results'] = update_book(book_id,data,sess,ret['results'])


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



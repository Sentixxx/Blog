from flask import Blueprint , request
from flask_jwt_extended import jwt_required , get_jwt_identity
from app.extensions import db
from app.models import *
from app.utils import to_dict , submit
from flask import jsonify
from app.services.borrow import delay_borrow

borrow = Blueprint('borrow',__name__)


@borrow.route('/all',methods=['GET'])
@jwt_required()
def on_info_all():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name == 'user':
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200
    
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

@borrow.route('/user_id/<int:user_id>',methods=['GET'])
@jwt_required()
def on_info_user(user_id):
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name == 'user' and cur_user.user_instance_id != user_id:
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200

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

@borrow.route('/borrow_id/<int:borrow_id>',methods=['GET'])
@jwt_required()
def on_info_borrow(borrow_id):
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name == 'user':
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200
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

@borrow.route('/book_instance_id/<string:book_instance_id>',methods=['GET'])
@jwt_required()
def on_info_bi(book_instance_id):
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name == 'user':
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200

    ret = {}

    results = Borrow.query.filter(Borrow.is_deleted==0,Borrow.book_instance_id==book_instance_id).all()

    if results:
        ret['results'] = []
        records = to_dict(results)
        for record in records:
            book_instance = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==record['book_instance_id']).first()
            book = Book.query.filter(Book.is_deleted==0,Book.book_id==book_instance.book_id).first()
            user = UserInstance.query.filter(UserInstance.is_deleted==0,UserInstance.user_instance_id==record['user_instance_id']).first()
            record['user_instance_name'] = user.user_instance_name
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

@borrow.route('/search',methods=['GET'])
@jwt_required()
def on_search():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    data = request.args.to_dict()


    ret = {}

    query = Borrow.query.filter(Borrow.is_deleted == 0,Borrow.user_instance_id==current_user)

    if data.get('book_name') is not None:
        query = query.join(BookInstance,BookInstance.book_instance_id == Borrow.book_instance_id).join(Book,Book.book_id == BookInstance.book_id).filter(Book.book_name.like('%'+data['book_name']+'%'))

    if data.get('book_instance_id') is not None:
        query = query.filter(Borrow.book_instance_id == data['book_instance_id'])

    results = query.all()

    ret['results'] = to_dict(results)
    ret['status'] = 200
    ret['msg'] = "查询成功"

    return jsonify(ret)

@borrow.route('/book_id/<int:book_id>',methods=['GET'])
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
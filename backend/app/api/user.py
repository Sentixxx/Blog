
from flask import Blueprint , request
from app.extensions import db
from app.models import *
from flask import jsonify
from app.utils import submit
from app.services.user import get_user_info

user = Blueprint('user',__name__)


@user.route('/return',methods=['POST'])
def on_return():
    data = request.args.to_dict()
    sess = db.session()

    ret = {}
    ret['results'] = {}
    sess, ret['results'] = return_book_instance(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "归还失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    sess,ret['results'] = return_book(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "归还失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    sess,ret['results'] = delete_borrow(data,sess,ret['results'])
    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "归还失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    
    if not submit(sess):
        ret['msg'] = "归还失败"
        ret['status'] = -2
    else:
        ret['msg'] = "归还成功"
        ret['status'] = 200
    return jsonify(ret) , 200

@user.route('/info',methods=['GET'])
def onInfo():
    data = request.args.to_dict()
    sess = db.session()
    ret = {}

    sess,ret['results'] = get_user_info(data,sess,ret['results'])

from flask import Blueprint , request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import *
from flask import jsonify
from app.utils import submit
from app.services.user import get_user_info

user = Blueprint('user',__name__)

@user.route('/info/all',methods=['GET'])
@jwt_required()
def on_get_all():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "获取用户信息失败：无法识别当前用户"
        ret['status'] = -3
        return jsonify(ret), 200
    
    ret = {}
    ret['results'] = []

    results = db.session.query(UserInstance).all()

    ret['results'] = [result.to_dict() for result in results]

    ret['msg'] = "获取用户信息成功"
    ret['status'] = 200
    return jsonify(ret) , 200

@user.route('/info/cur',methods=['GET'])
@jwt_required()
def on_info():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "获取用户信息失败：无法识别当前用户"
        ret['status'] = -3
        return jsonify(ret), 200
    # print(current_user)
    
    ret = {}
    ret['results'] = {}

    ret['results'] = get_user_info(current_user,ret['results'])

    if ret['results'].get('error_msg') is not None:
        ret['msg'] = "获取用户信息失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    else:
        ret['msg'] = "获取用户信息成功"
        ret['status'] = 200
        return jsonify(ret) , 200
    



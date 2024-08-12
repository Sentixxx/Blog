
from flask import Blueprint , request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import *
from flask import jsonify
from app.utils import submit
from app.services.user import get_user_info

user = Blueprint('user',__name__)

@user.route('/search',methods=['GET'])
def on_search_user():
    name = request.args.get('user_instance_name','')
    phone = request.args.get('user_instance_phone','')
    email = request.args.get('user_instance_email','')
    nickname = request.args.get('user_instance_nickname','')
    status = request.args.get('user_instance_status','')
    group = request.args.get('user_instance_group_name','')
    id = request.args.get('user_instance_id','')
    ret = {}
    ret['results'] = []

    if id:
        result = UserInstance.query.filter(UserInstance.user_instance_id==id).first()
        if result:
            ret['results'].append(result.to_dict())
            return jsonify(ret) , 200
        else:
            ret['msg'] = "用户不存在"
            ret['status'] = -1
            return jsonify(ret)
    

    query = UserInstance.query.filter(UserInstance.is_deleted==0)

    if name:
        query = query.filter(UserInstance.user_instance_name.like('%' + name + '%'))
    if phone:
        query = query.filter(UserInstance.user_instance_phone.like('%' + phone + '%'))
    if email:
        query = query.filter(UserInstance.user_instance_email.like('%' + email + '%'))
    if nickname:
        query = query.filter(UserInstance.user_instance_nickname.like('%' + nickname + '%'))
    if status:
        query = query.filter(UserInstance.user_instance_status==status)
    if group:
        query = query.filter(UserInstance.user_instance_group_name==group)
    
    results = query.all()
    for result in results:
        ret['results'].append(result.to_dict())
    
    ret['msg'] = "查询成功"
    ret['status'] = 200
    return jsonify(ret) , 200

@user.route('/ban/<int:id>',methods=['PUT'])
@jwt_required()
def on_ban(id):
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "修改用户状态失败：无法识别当前用户"
        ret['status'] = -3
        return jsonify(ret), 200

    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()

    if cur_user.user_instance_group_name != 'admin' and cur_user.user_instance_group_name != 'super_admin':
        ret['msg'] = "修改用户状态失败：无权限"
        ret['status'] = -5
        return jsonify(ret), 200
    
    ret = {}
    ret['results'] = []

    user = UserInstance.query.filter(UserInstance.user_instance_id == id).first()

    if user is None:
        ret['msg'] = "修改用户状态失败：用户不存在"
        ret['status'] = -2
        return jsonify(ret), 200

    if user.user_instance_group_name == 'super_admin':
        ret['msg'] = "修改用户状态失败：无法修改超级管理员"
        ret['status'] = -5
        return jsonify(ret), 200
    
    if user.user_instance_group_name != 'user' and cur_user.user_instance_group_name != 'super_admin':
        ret['msg'] = "修改用户状态失败：无法修改管理员"
        ret['status'] = -5
        return jsonify(ret), 200

    if user.user_instance_status == 0:
        user.user_instance_status = 1
    else:
        user.user_instance_status = 0

    sess = db.session()

    if submit(sess):
        ret['msg'] = "修改用户状态成功"
        ret['status'] = 200
        ret['results'] = user.to_dict()
    else:
        ret['msg'] = "修改用户状态失败：数据库提交失败"
        ret['status'] = -5

    return jsonify(ret), 200



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

    curUser = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()

    results = db.session.query(UserInstance).all()



    if curUser.user_instance_group_name == 'user':
        ret['msg'] = "获取用户信息失败：无权限"
        ret['status'] = -5
        return jsonify(ret), 200
    
    ret['results'] = [result.to_dict() for result in results]
    if curUser.user_instance_group_name != 'super_admin':
        ret['results'] = [result for result in ret['results'] if result['user_instance_group_name'] == 'user']
    else:
        ret['results'] = [result for result in ret['results'] if result['user_instance_group_name'] != 'super_admin']

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

    
    print(current_user)
    
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
    
@user.route('/info/update/<int:id>',methods=['PUT'])
@jwt_required()
def on_update(id):
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "更新用户信息失败：无法识别当前用户"
        ret['status'] = -3
        return jsonify(ret), 200

    ret = {}
    ret['results'] = {}

    sess = db.session()

    user = sess.query(UserInstance).filter(UserInstance.user_instance_id == id).first()
    curUser = sess.query(UserInstance).filter(UserInstance.user_instance_name == current_user).first()

    if user is None:
        ret['msg'] = "更新用户信息失败：用户不存在"
        ret['status'] = -2
        return jsonify(ret), 200

    data = request.get_json()
    if data is None:
        ret['msg'] = "更新用户信息失败：无法识别请求数据"
        ret['status'] = -4
        return jsonify(ret), 200
    
    if user.user_instance_name != curUser.user_instance_name and (curUser.user_instance_group_name != 'admin' or curUser.user_instance_group_name != 'super_admin'):
        ret['msg'] = "更新用户信息失败：无权限"
        ret['status'] = -5
        return jsonify(ret), 200

    user.user_instance_name = data.get('user_instance_name') or user.user_instance_name
    user.user_instance_password = data.get('user_instance_password') or user.user_instance_password
    user.user_instance_email = data.get('user_instance_email') or user.user_instance_email
    user.user_instance_phone = data.get('user_instance_phone') or user.user_instance_phone

    if submit(sess):
        ret['status'] = 200
        ret['results'] = user.to_dict()
        ret['msg'] = "更新用户信息成功"
    
    else:
        ret['msg'] = "更新用户信息失败：数据库提交失败"
        ret['status'] = -5

    return jsonify(ret), 200

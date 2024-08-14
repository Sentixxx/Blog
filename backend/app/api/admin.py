from flask import Blueprint , request ,jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from app.extensions import db
from app.models.user_group import add_group , update_group , delete_group , UserGroup
from app.models import UserInstance
from app.utils import submit

admin = Blueprint('admin',__name__)

@admin.route('/group',methods=['POST'])
@jwt_required()
def on_add_group():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name != 'super_admin':
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess, ret['results'] = add_group(data,sess,ret['results'])

    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "添加失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    if not submit(sess):
        ret['msg'] = "添加失败"
        ret['status'] = -2
    else:
        ret['msg'] = "添加成功"
        ret['status'] = 200
    return jsonify(ret) , 200

@admin.route('/group',methods=['POST'])
@jwt_required()
def on_modify_group():
    current_user = get_jwt_identity()

    if current_user is None:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200
    
    cur_user = UserInstance.query.filter(UserInstance.user_instance_id == current_user).first()
    if cur_user.user_instance_group_name != 'super_admin':
        ret['msg'] = "无权限"
        ret['status'] = -5
        return jsonify(ret), 200
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess, ret['results'] = update_group(data,sess,ret['results'])

    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "修改失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    if not submit(sess):
        ret['msg'] = "修改失败"
        ret['status'] = -2
    else:
        ret['msg'] = "修改成功"
        ret['status'] = 200
    return jsonify(ret) , 200


@admin.route('/show_all_user',methods=['GET'])
@jwt_required()
def on_show_all_user():
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
    ret['results'] = []

    results = UserInstance.query.filter_by(is_deleted=0).all()
    if results:
        ret['msg'] = "查询成功"
        ret['status'] = 200
        for result in results:
            ret['results'].append(result.to_dict())
    else:
        ret['msg'] = "用户不存在"
        ret['status'] = -1

@admin.route('/show_all_permission',methods=['GET'])
def on_show_all_permission():

    data = request.args.to_dict()
    ret = {}
    ret['results'] = []

    results = UserGroup.query.filter(UserGroup.is_deleted==0,UserGroup.user_group_name==data.get('user_group_name')).all()
    if results:
        ret['msg'] = "查询成功"
        ret['status'] = 200
        for result in results:
            ret['results'].append(result.to_dict())
    else:
        ret['msg'] = "用户组不存在"
        ret['status'] = -1
    return jsonify(ret) , 200

@admin.route('/show_all_group',methods=['GET'])
def on_show_all_group():
    ret = {}
    ret['results'] = []

    results = UserGroup.query.filter_by(is_deleted=0).all()
    if results:
        ret['msg'] = "查询成功"
        ret['status'] = 200
        for result in results:
            ret['results'].append(result.to_dict())
    else:
        ret['msg'] = "用户组不存在"
        ret['status'] = -1
    return jsonify(ret) , 200

@admin.route('/delete_group',methods=['DELETE'])
def on_delete_group():
    data = request.args.to_dict()

    sess = db.session()

    ret = {}
    ret['results'] = {}

    sess, ret['results'] = delete_group(data,sess,ret['results'])

    if ret['results'].get('error_msg') is not None:
        sess.rollback()
        ret['msg'] = "删除失败：" + ret['results']['error_msg']
        ret['results'].pop('error_msg')
        ret['status'] = -1
        return jsonify(ret) , 200
    if not submit(sess):
        ret['msg'] = "删除失败"
        ret['status'] = -2
    else:
        ret['msg'] = "删除成功"
        ret['status'] = 200
    return jsonify(ret) , 200


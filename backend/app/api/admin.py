from flask import Blueprint , request ,jsonify
from app.extensions import db
from app.models.user_group import add_group , update_group , delete_group
from app.utils import submit

admin = Blueprint('admin',__name__)

@admin.route('/add_group',methods=['POST'])
def on_add_group():
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

@admin.route('/modify_group',methods=['POST'])
def on_modify_group():
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


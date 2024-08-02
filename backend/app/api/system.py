
from flask import Blueprint , request
from app.models import UserInstance,SysLog
from uuid import uuid4
from flask import jsonify
from app.utils import submit,hash_password
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.extensions import db
from app.config import Config
system = Blueprint('system',__name__)

@system.route('/login',methods=['POST'])
def on_login():
    data = request.args.to_dict()

    name = data.get('user_instance_name')
    password = hash_password(data.get('user_instance_password'))
    ret = {}
    ret['results'] = {}

    result = UserInstance.query.filter_by(user_instance_name=name).first()
    print(name)
    
    if(result):
        if(result.user_instance_password == password):
            ret['msg'] = "登录成功"
            ret['status'] = 200
            ret['results']['accessToken'] = create_access_token(identity=result.user_instance_id)
            ret['results']['tokenType'] = 'Bearer'
            ret['results']['expires']= Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()
            return jsonify(ret) , 200
        else:
            ret['msg'] = "密码错误"
            ret['status'] = -1
            return jsonify(ret) , 200
    else:
        ret['msg'] = "用户不存在"
        ret['status'] = -1
        return jsonify(ret), 200

@system.route('/regist',methods=['POST'])
def on_regist():
    data = request.args.to_dict()

    sess = db.session()
    name = data.get('user_instance_name')
    if UserInstance.query.filter_by(user_instance_name=name).first():
        ret = {}
        ret['msg'] = "用户已存在"
        ret['status'] = -1
        return jsonify(ret) , 200
    password = hash_password(data.get('user_instance_password'))
    ret = {}
    # print(password)
    # username = 'user_'+str(uuid4())
    newUser = UserInstance(user_instance_password=password,user_instance_name=name,user_instance_group_name='user')

    sess.add(newUser)
    # sess.flush()

    ret['results'] = {}
    # ret['results']['user_instance_id'] = newUser.user_instance_id
    
    if not submit(sess):
        ret['msg'] = "注册失败,请稍后再试"
        ret['status'] = -2
    else:
        ret['msg'] = "注册成功"
        ret['status'] = 200
    return jsonify(ret) , 200

@system.route('/log',methods=['POST'])
def on_log():
    data = request.args.to_dict()

    sess = db.session()

    newlog = SysLog(log_module = data.get('log_module'),log_content = data.get('log_content'),log_user = data.get('log_user'),log_level = data.get('log_level'),log_time = data.get('log_time'),log_browser = data.get('log_browser'),log_browser_version = data.get('log_browser_version'),log_ip = data.get('log_ip'),log_create_by = data.get('log_create_by'),log_create_time = data.get('log_create_time'),log_update_by = data.get('log_update_by'),log_request_url = data.get('log_request_url'))

    newlog.add(sess)

    submit(sess)

    return 200


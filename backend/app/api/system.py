
from flask import Blueprint , request
from app.models import UserInstance,SysLog
from uuid import uuid4
from flask import jsonify
from app.utils import submit
from app.extensions import db
system = Blueprint('system',__name__)


@system.route('/login',methods=['POST'])
def on_login():
    data = request.args.to_dict()
    email = data.get('user_instance_email')
    password = data.get('user_instance_password')
    ret = {}
    # print(email)
    # print(password)
    result = UserInstance.query.filter_by(user_instance_email=email).first()
    # print(result)
    
    if(result):
        if(result.user_instance_password == password):
            ret['msg'] = "登录成功"
            ret['status'] = 200
            return jsonify(ret) , 200
        else:
            ret['msg'] = "密码错误"
            ret['status'] = -1
            return jsonify(ret) , 200
    else:
        ret['msg'] = "邮箱未注册"
        ret['status'] = -1
        return jsonify(ret), 200

@system.route('/register',methods=['POST'])
def on_register():
    data = request.args.to_dict()

    sess = db.session()
    email = data.get('user_instance_email')
    password = data.get('user_instance_password')
    username = 'user_'+str(uuid4())
    newUser = UserInstance(user_instance_name = username,user_instance_password=password,user_instance_email=email,user_instance_group_id=1,user_group_name='user')
    sess.add(newUser)
    ret = {}
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


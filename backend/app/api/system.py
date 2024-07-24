
from flask import Blueprint , request
from app.models import UserInstance
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


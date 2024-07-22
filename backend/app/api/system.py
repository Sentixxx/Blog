
from flask import Blueprint , request
from app.models import UserInstance
from uuid import uuid4
system = Blueprint('system',__name__)


@system.route('/login',methods=['POST'])
def on_login():
    data = request.args.to_dict()
    email = data.get('email')
    password = data.get('password')
    print(email)
    print(password)
    result = UserInstance.query.filter_by(user_instance_email=email).first()
    print(result)
    if(result):
        if(result.user_instance_password == password):
            return "login success" , 200
        else:
            return "password error" , 200
    else:
        return "email error" , 200

@system.route('/register',methods=['POST'])
def on_register():
    data = request.args.to_dict()
    email = data.get('email')
    password = data.get('password')
    username = 'user_'+str(uuid4())
    newUser = UserInstance(user_instance_name = username,user_instance_password=password,user_instance_email=email,user_instance_group_id=1)
    if not newUser.save():
        return "register failed , try later" , 431
    # print(email)
    # print(password)
    return "register success" , 200


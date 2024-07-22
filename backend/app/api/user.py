
from flask import Blueprint , request
from app.models import UserInstance
from uuid import uuid4
user = Blueprint('user',__name__)


@user.route('/search',methods=['GET'])
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


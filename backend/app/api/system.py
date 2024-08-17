
from flask import Blueprint , request
from app.models import UserInstance,Borrow,Book
from uuid import uuid4
from flask import jsonify
from app.utils import submit,hash_password,to_dict
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.extensions import db
import time
from app.config import Config
import qianfan
import os

system = Blueprint('system',__name__)

@system.route('/login',methods=['POST'])
def on_login():
    data = request.args.to_dict()

    name = data.get('user_instance_name')
    password = hash_password(data.get('user_instance_password'))
    ret = {}
    ret['results'] = {}

    result = UserInstance.query.filter_by(user_instance_name=name).first()
    # print(name)
    
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

@system.route('/userBorrow/<int:id>',methods=['GET'])
def on_user_borrow(id):
    sess = db.session()
    ret = {}
    ret['results'] = {}

    # print("__________________________________")
    # print(id)

    if id == 0:
        ret['status'] = 200
        return jsonify(ret) , 200

    results = Borrow.query.filter_by(user_instance_id=id).all()

    ret['results']['borrow_cnt']  = 0
    ret['results']['current_borrow_cnt'] = 0
    read_time = 0
    ret['results']['read_time'] = 0
    ret['results']['overdue'] = 0

    if(results):
        ret['msg'] = "获取成功"
        ret['status'] = 200
        dics = to_dict(results)
        for item in dics:
            ret['results']['borrow_cnt'] += 1
            if(item['is_completed'] == 0):
                ret['results']['current_borrow_cnt'] += 1
                cur_time = time.time()
                extra_return_time = item['extra_return_time'].timestamp() if item['extra_return_time'] else None
                should_return_time = item['should_return_time'].timestamp() if item['should_return_time'] else None
                if cur_time > (extra_return_time or should_return_time):
                        ret['results']['overdue'] += 1
            if item['is_completed'] == 1:
                actual_return_time = item['actual_return_time'].timestamp() if item['actual_return_time'] else None
                borrow_time = item['borrow_time'].timestamp() if item['borrow_time'] else None
                read_time += actual_return_time - borrow_time

        hours, remainder = divmod(read_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        ret['results']['read_time'] = f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"
    else:
        ret['msg'] = "无借阅记录"
        ret['status'] = -1

    all_usr = UserInstance.query.filter_by().all()
    dics = to_dict(all_usr)
    all_usr_cnt = 0
    for item in dics:
        if item['user_instance_group_name'] == 'user':
            all_usr_cnt += 1

    all_usr_borrow = Borrow.query.filter_by().all()
    all_usr_time = 0
    dics = to_dict(all_usr_borrow)
    for item in dics:
        if item['is_completed'] == 1:
            actual_return_time = item['actual_return_time'].timestamp() if item['actual_return_time'] else None
            borrow_time = item['borrow_time'].timestamp() if item['borrow_time'] else None
            all_usr_time += actual_return_time - borrow_time
    
    avg_read_time = all_usr_time / all_usr_cnt
    hours, remainder = divmod(avg_read_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    ret['results']['avg_read_time'] = f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"
    
    return jsonify(ret) , 200


@system.route('/AI/<int:id>',methods=['GET'])
def on_ai(id):
    os.environ["QIANFAN_ACCESS_KEY"] = os.environ.get("QIANFAN_ACCESS_KEY")
    os.environ["QIANFAN_SECRET_KEY"] = os.environ.get("QIANFAN_SECRET_KEY")



    ret = {}
    ret['results'] = {}

    book_name = Book.query.filter_by(book_id=id).first().book_name

    # ret['results']['book_name'] = book_name
    
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(model="Yi-34B-Chat", messages=[{
    "role": "user",
    "content": "作为一位图书推荐专家，根据用户提供的书名，使用网络搜索信息，并提供相关的阅读建议。建议应基于用户的兴趣和口味，同时考虑书籍的主题、作者、出版日期和评价等因素。建议应清晰和具体，以便用户更好地理解每本书的主要内容和特点，并做出明智的选择。请注意，回答应包括相关的详细信息和评价，以帮助用户更好地了解图书，并提供独特的推荐理由和背景信息。让我们一步一步来思考" + f"现在，请你给我介绍一下关于《{book_name}》这本书的信息，包括主题、作者、出版日期和评价等方面的内容。"
    }])

    # print(resp['body'])
    ret['status'] = 200
    ret['results'] = resp['body']['result']
    ret['msg'] = "获取成功"

    return jsonify(ret) , 200
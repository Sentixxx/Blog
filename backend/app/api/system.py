
from flask import Blueprint , request
from app.models import UserInstance,Borrow,SysLog
from uuid import uuid4
from flask import jsonify
from app.utils import submit,hash_password,to_dict
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.extensions import db
import time
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

@system.route('/info/userBorrow/<int:id>',methods=['GET'])
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
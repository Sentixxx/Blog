from flask import Blueprint , request

admin = Blueprint('admin',__name__)

@admin.route('/',methods=['GET'])
def index():
    print('admin')
    return 'admin'


@admin.route('/login',methods=['POST'])
def on_login():
    print('login')
    print('post')
    data = request.args.to_dict()
    print(data)
    username = data.get('uname')
    password = data.get('password')
    
    userid = select_user(username,password)
    return "login page" , 200
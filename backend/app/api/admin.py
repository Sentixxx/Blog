from flask import Blueprint , request

admin = Blueprint('admin',__name__)

@admin.route('/',methods=['GET'])
def index():
    print('admin')
    return 'admin'



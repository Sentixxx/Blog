from flask import Blueprint

admin = Blueprint('admin',__name__)

@admin.route('/admin',methods=['GET'])
def index():
    return 'admin'
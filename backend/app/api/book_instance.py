from flask import Blueprint , request
from app.extensions import db
from app.models import *
from app.utils import to_json,to_dict
from app.utils import submit
from flask import jsonify
book_instance = Blueprint('book_instance',__name__)

@book_instance.route('/get/all',methods=['GET'])
def on_get_all():
    ret = {}

    results = BookInstance.query.filter_by(is_deleted=0).all()

    if results:
        ret['results'] = to_dict(results)
        ret['msg'] = "获取成功"
        ret['status'] = 200
    else:
        ret['msg'] = "没有图书"
        ret['status'] = -2
    
    return jsonify(ret)

@book_instance.route('/get',methods=['GET'])
def on_get():
    data = request.args.to_dict()

    ret = {}

    if data.get('book_instance_id') is not None:
        result = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==data.get('book_instance_id')).first()
        if result:
            ret['results'] = result.to_dict()
            ret['msg'] = "获取成功"
            ret['status'] = 200
        else:
            ret['msg'] = "图书不存在"
            ret['status'] = -2

    
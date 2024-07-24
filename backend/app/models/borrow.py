# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class Borrow(BaseModel):
    __tablename__ = "borrow"
    borrow_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="借阅ID")
    user_instance_id = db.Column(db.Integer, comment="用户ID",nullable=False)
    book_instance_id = db.Column(db.String(255), comment="书籍实体编码",nullable=False)
    borrow_time = db.Column(db.DateTime, comment="借阅时间",nullable=False,default=datetime.now)
    should_return_time = db.Column(db.DateTime, comment="归还时间",nullable=True)
    extra_return_time = db.Column(db.DateTime, comment="额外归还时间",nullable=True)
    actual_return_time = db.Column(db.DateTime, comment="实际归还时间",nullable=True)
    is_completed = db.Column(db.Integer, comment="借阅状态 0:借阅中 1:已归还 2:逾期 3:遗失 4:未知状态 note",nullable=False)

def add_borrow(data,sess,ret):
    if data.get('user_instance_id') is None or data.get('book_instance_id') is None or data.get('should_return_time') is None:
        ret['error_msg'] = "borrow info is not enough"
        return sess , ret
    newBorrow = Borrow(user_instance_id=data.get('user_instance_id'),book_instance_id=data.get('book_instance_id'),should_return_time=data.get('should_return_time'),is_completed=1)
    sess.add(newBorrow)
    sess.flush()
    ret['borrow_id'] = newBorrow.borrow_id

    return sess , ret

def delete_borrow(data,sess,ret):
    code = data.get('borrow_id')
    if code is None:
        ret['error_msg'] = "ID为空"
        return sess , ret
    result = Borrow.query.filter_by(borrow_id=code).first()
    if(result):
        if result.is_deleted == 0:
            if(result.user_instance_id != data['user_instance_id'] or result.book_instance_id != data['book_instance_id']):
                ret['error_msg'] = '借阅信息ID不匹配'
                return sess , ret
            result.is_deleted = 1
            sess = result.add(sess)
            return sess , ret
        else:
            ret['error_msg'] = "借阅已删除"
            return sess , ret
    ret['error_msg'] = "借阅不存在"
    return sess , ret

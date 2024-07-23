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

def add_borrow(data,sess):
    newBorrow = Borrow(user_instance_id=data.get('user_instance_id'),book_instance_id=data.get('book_instance_id'),should_return_time=data.get('should_return_time'),is_completed=1)

    sess.add(newBorrow)

    return sess , newBorrow

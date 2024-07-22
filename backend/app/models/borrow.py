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
    borrow_is_deleted = db.Column(db.Integer, comment="是否删除",nullable=False,default=False)
    borrow_create_time = db.Column(db.DateTime, comment="创建时间",nullable=False,default=datetime.now)
    borrow_update_time = db.Column(db.DateTime, comment="更新时间",nullable=False,default=datetime.now)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)

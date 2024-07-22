# -*- coding: utf-8 -*-
from app.extensions import db
from datetime import datetime
from app.models.base_model import BaseModel

class Book(BaseModel):
    __tablename__ = "book"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="书籍ID")
    book_name = db.Column(db.String(255), comment="书籍名",nullable=False)
    book_author = db.Column(db.String(255), comment="作者",nullable=False)
    book_press = db.Column(db.String(255), comment="出版社",nullable=False)
    book_pic = db.Column(db.String(255), comment="封面",nullable=True)
    book_isbn_code = db.Column(db.String(255), comment="ISBN编码",nullable=False)
    book_type = db.Column(db.String(255), comment="类型",nullable=True)
    book_cur_stock_num = db.Column(db.Integer, comment="当前库存",nullable=False)
    book_create_time = db.Column(db.DateTime, comment="创建时间",nullable=False,default=datetime.now)
    book_update_time = db.Column(db.DateTime, comment="更新时间",nullable=False,default=datetime.now)
    book_is_deleted = db.Column(db.Integer, comment="是否删除",nullable=False,default=False)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)
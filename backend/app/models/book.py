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

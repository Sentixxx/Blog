# -*- coding: utf-8 -*-
from app.extensions import db
from datetime import datetime
from app.models.base_model import BaseModel
from uuid import uuid4


class Book(BaseModel):
    __tablename__ = "book"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="书籍ID")
    book_introduce = db.Column(db.String(255), comment="简介",nullable=True)
    book_name = db.Column(db.String(255), comment="书籍名",nullable=False)
    book_author = db.Column(db.String(255), comment="作者",nullable=False)
    book_press = db.Column(db.String(255), comment="出版社",nullable=False)
    book_pic = db.Column(db.String(255), comment="封面",nullable=True)
    book_isbn_code = db.Column(db.String(255), comment="ISBN编码",nullable=False)
    book_type = db.Column(db.String(255), comment="类型",nullable=True)
    book_cur_stock_num = db.Column(db.Integer, comment="当前库存",nullable=False)

    
def return_book(data,sess,ret):
    book_id = ret.get('book_id') or data.get('book_id')
    if book_id is None:
        ret['error_msg'] = "ID为空"
        return sess , ret
    result = Book.query.filter_by(book_id=book_id).first()
    if(result):
        result.book_cur_stock_num += 1
        ret['book_cur_stock_num'] = result.book_cur_stock_num
        sess = result.add(sess)
    else:
        ret['error_msg'] = "找不到ID"
    return sess , ret



    

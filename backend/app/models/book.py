# -*- coding: utf-8 -*-
from app.extensions import db
from datetime import datetime
from app.models.base_model import BaseModel
from uuid import uuid4


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


def add_book(data,sess):
    result = Book.query.filter_by(book_isbn_code=data.get('isbn')).first()
    if(result):
        result.book_cur_stock_num += 1
        sess = result.add(sess)
        return sess , result
    else:
        result = Book(book_name=data.get('name'),book_author=data.get('author'),book_press=data.get('press'),book_isbn_code=data.get('isbn'),book_type=data.get('type'),book_cur_stock_num=1)
        sess = result.add(sess)
        return sess , result

def delete_book(sess, book_id):
    result = Book.query.filter_by(book_id=book_id).first()
    if(result):
        if result.cur_stock_num < 0:
            return sess , False
        result.cur_stock_num -= 1
        sess = result.add(sess)
        return sess , result.cur_stock_num
    else:
        return sess , False
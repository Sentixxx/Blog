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


def add_book(data, sess, ret):
    isbn = data.get('book_isbn_code') or ret.get('book_isbn_code')
    book_id = ret.get('book_id') or data.get('book_id')
    if isbn :
        result = Book.query.filter_by(book_isbn_code=data.get('book_isbn_code')).first()
    elif book_id:
        result = Book.query.filter_by(book_id=book_id).first()
    else:
        ret['error_msg'] = "ID为空"
        return sess , ret
    book_name = data.get('book_name')
    book_author = data.get('book_author')
    book_press = data.get('book_press')
    book_type = data.get('book_type')
    if(result is not None):
        if book_name is not None and book_name != result.book_name:
            ret['error_msg'] = "book name is not match"
            return sess , ret
        if book_author is not None and book_author != result.book_author:
            ret['error_msg'] = "book author is not match"
            return sess , ret
        if book_press is not None and book_press != result.book_press:
            ret['error_msg'] = "book press is not match"
            return sess , ret
        if book_type is not None and book_type != result.book_type:
            ret['error_msg'] = "book type is not match"
            return sess , ret
        if result.book_name is None:
            result.book_name = book_name
        if result.book_author is None:
            result.book_author = book_author
        if result.book_press is None:
            result.book_press = book_press
        if result.book_type is None:
            result.book_type = book_type
        result.book_cur_stock_num += 1
        ret['book_id'] = result.book_id
        sess = result.add(sess)
        return sess , result
    else:
        result = Book(book_name=data.get('book_name'),book_author=data.get('book_author'),book_press=data.get('book_press'),book_isbn_code=data.get('book_isbn_code'),book_type=data.get('book_type'),book_cur_stock_num=1)
        sess = result.add(sess)
        sess.flush()
        ret['book_id'] = result.book_id
        return sess , ret
    
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

def delete_book(sess, ret):
    book_id = ret.get('book_id')
    if book_id is None:
        ret.pop('book_id')
        ret['error_msg'] = "book_id is None"
        return sess , ret
    
    result = Book.query.filter_by(book_id=book_id).first()
    if(result):
        if result.book_cur_stock_num <= 0:
            ret['error_msg'] = "can not delete book with stock"
            return sess , ret
        result.book_cur_stock_num -= 1
        ret['book_cur_stock_num'] = result.book_cur_stock_num
        sess = result.add(sess)
    else:
        ret['error_msg'] = "can not find such book_id"

    return sess , ret


def update_book(data,sess,ret):
    isbn = data.get('book_isbn_code')
    if isbn is None:
        isbn = ret.get('book_isbn_code')
    book_id = ret.get('book_id')
    if book_id is None:
        book_id = data.get('book_id')
    if isbn is not None:
        result = Book.query.filter_by(book_isbn_code=isbn).first()
    elif book_id is not None:
        result = Book.query.filter_by(book_id=book_id).first()
    else:
        ret['error_msg'] = "ID为空"
        return sess , ret
    for modify_item in data.keys():
        if modify_item == 'book_isbn_code':
            continue
        if hasattr(result,modify_item) and getattr(result,modify_item) is not None:
            setattr(result,modify_item,data.get(modify_item))
    sess = result.add(sess)

    for item in data.keys():
        if hasattr(result,item):
            ret[item] = getattr(result,item)
    return sess , ret

    

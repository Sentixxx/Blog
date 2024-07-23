# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel
import sys
from uuid import uuid4


class BookInstance(BaseModel):
    __tablename__ = "book_instance"
    book_instance_id = db.Column(db.String(255), primary_key=True, comment="书籍实体编码")
    book_id = db.Column(db.Integer, comment="书籍ID",nullable=False)
    borrow_id = db.Column(db.Integer, comment="借阅ID",nullable=True)
    book_instance_status = db.Column(db.Integer, comment="借阅状态 0:馆藏 1:借出 2:遗失 3:未知状态",nullable=False,default=0)
    book_instance_location = db.Column(db.String(255), comment="馆藏地点",nullable=False)

def add_book_instance(data,result,sess):
    code = uuid4()
    while BookInstance.query.filter_by(book_instance_id=code).first():
        code = uuid4()
    
    newBookInstance = BookInstance(book_instance_id = code,book_id=result.book_id,book_instance_location=data.get('location'))
    sess = newBookInstance.add(sess)

    return sess , code

def delete_book_instance(data,sess):
    code = data.get('book_instance_id')
    result = BookInstance.query.filter_by(book_instance_id=code).first()
    if(result):
        result.is_deleted = 1
        sess = result.add(sess)
        return sess , result
    else:
        return sess , False
    
def update_book_instance(data,sess):
    code = data.get('book_instance_id')
    borrow_id = data.get('borrow_id')
    result = BookInstance.query.filter_by(book_instance_id=code).first()
    if(result):
        result.borrow_id = borrow_id
        sess = result.add(sess)
        return sess , result
    else:
        return sess , False



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

def add_book_instance(data,sess,ret):
    if data.get('book_instance_id') is not None:
        code = data.get('book_instance_id')
        result = BookInstance.query.filter_by(book_instance_id=code).first()
        if(result):
            if(result.is_deleted == 1):
                ret['note'] = "图书已被删除"
                if(result.book_id != ret['book_id']):
                    ret['error_msg'] = "图书信息ID不匹配"
                    return sess , ret
                
                result.is_deleted = 0
                result.book_instance_location = data.get('book_instance_location')
                result.note1 = None
                sess = result.add(sess)

                ret['book_instance_id'] = result.book_instance

                sess = result.add(sess)
                return sess , ret
            else:
                ret['error_msg'] = "图书已存在"
                return sess , ret
            
    code = uuid4()
    while BookInstance.query.filter_by(book_instance_id=code).first():
        code = uuid4()
    
    newBookInstance = BookInstance(book_instance_id = code,book_id = ret['book_id'],book_instance_location = data.get('book_instance_location'))
    sess = newBookInstance.add(sess)

    if(newBookInstance.book_id is None):
        ret.pop('book_id')
        ret['error_msg'] = "图书信息ID为空"
        return sess , ret
        
    ret['book_instance_id'] = code
    return sess , ret

def delete_book_instance(data,sess,ret={}):
    code = data.get('book_instance_id')
    result = BookInstance.query.filter_by(book_instance_id=code).first()
    if(result):
        if result.is_deleted == 1:
            ret['error_msg'] = "图书已被删除"
            return sess , ret
        result.is_deleted = 1
        if data.get('reason') is not None:
            result.note1 = '原因：' + data.get('reason')
        ret['book_id'] = result.book_id
        sess = result.add(sess)
    else:
        ret['error_msg'] = "图书不存在"
    return sess , ret
    
def update_book_instance(data,sess,ret):
    code = data.get('book_instance_id')
    result = BookInstance.query.filter(BookInstance.is_deleted!=1,BookInstance.book_instance_id==code).first()
    if result is None:
        ret['error_msg'] = "图书不存在"
        return sess , ret
    for modify_item in data.keys():
        if modify_item == 'book_instance_id':
            continue
        if hasattr(result,modify_item):
            if getattr(result,modify_item) is not None:
                setattr(result,modify_item,data.get(modify_item))
    if data.get('book_instance_status') is not None:
        result.book_instance_status = data.get('book_instance_status')

    sess = result.add(sess)
    sess.flush()
    for item in data.keys():
        if hasattr(result,item):
            ret[item] = getattr(result,item)

    ret['book_id'] = result.book_id
    return sess , ret

def borrow_book_instance(data,sess,ret):
    code = data.get('book_instance_id')
    borrow_id = ret.get('borrow_id')
    if code is None or borrow_id is None:
        ret['error_msg'] = "信息不足"
        return sess , ret
    result = BookInstance.query.filter(BookInstance.is_deleted!=1,BookInstance.book_instance_id==code,BookInstance.book_instance_status==0).first()
    if result is None:
        ret['error_msg'] = "图书不存在或已借出"
        return sess , ret
    result.borrow_id = borrow_id
    result.book_instance_status = 1

    sess = result.add(sess)

    ret['book_id'] = result.book_id
    return sess , ret

def return_book_instance(data,sess,ret):
    code = data.get('book_instance_id')
    borrow_id = data.get('borrow_id')
    if code is None or borrow_id is None:
        ret['error_msg'] = "信息不足"
        return sess , ret
    result = BookInstance.query.filter(BookInstance.book_instance_id==code,BookInstance.book_instance_status==1).first()
    if result is None:
        ret['error_msg'] = "图书已归还"
        return sess , ret
    result.borrow_id = borrow_id
    result.book_instance_status = 0
    result.is_deleted = 0

    sess = result.add(sess)

    ret['book_id'] = result.book_id
    return sess , ret



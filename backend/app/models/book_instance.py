# -*- coding: utf-8 -*-
from app.extensions import db
from app.models.base_model import BaseModel


class BookInstance(BaseModel):
    __tablename__ = "book_instance"
    book_instance_id = db.Column(db.String(255), primary_key=True, comment="书籍实体编码")
    book_id = db.Column(db.Integer, comment="书籍ID",nullable=False)
    borrow_id = db.Column(db.Integer, comment="借阅ID",nullable=True)
    book_instance_status = db.Column(db.Integer, comment="借阅状态 0:馆藏 1:借出 2:遗失 3:未知状态",nullable=False,default=0)
    book_instance_location = db.Column(db.String(255), comment="馆藏地点",nullable=False)




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



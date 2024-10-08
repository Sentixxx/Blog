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

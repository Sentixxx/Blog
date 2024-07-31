# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class Message(BaseModel):
    __tablename__ = "message"
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="消息ID")
    message_title = db.Column(db.String(255), comment="消息标题",nullable=False)
    message_to = db.Column(db.String(255), comment="消息接收者",nullable=False)
    message_from = db.Column(db.String(255), comment="消息发送者",nullable=False)
    message_content = db.Column(db.String(255), comment="消息内容",nullable=False)
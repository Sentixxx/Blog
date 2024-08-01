# !/usr/bin/python3
# -*- coding: utf-8 -*-
from app.extensions import db
from datetime import datetime
from app.models.base_model import BaseModel


class UserInstance(BaseModel):
    __tablename__ = "user_instance"
    user_instance_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="用户ID")
    user_instance_name = db.Column(db.String(255), comment="用户名",nullable=True)
    user_instance_password = db.Column(db.String(255), comment="密码",nullable=False)
    user_instance_nickname = db.Column(db.String(255), comment="昵称",nullable=True)
    user_instance_gender = db.Column(db.String(255), comment="性别",nullable=True)
    user_instance_phone = db.Column(db.String(255), comment="手机号",nullable=True)
    user_instance_email = db.Column(db.String(255), comment="邮箱",nullable=True)
    user_instance_group_name = db.Column(db.String(255), comment="用户组名",nullable=False)
    user_instance_status = db.Column(db.Integer, comment="状态",nullable=False,default=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if c.name != "user_instance_password"}
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
    user_instance_email = db.Column(db.String(255), comment="邮箱",nullable=False)
    user_instance_group_id = db.Column(db.Integer, comment="用户组ID",nullable=False)
    user_instance_status = db.Column(db.Integer, comment="状态",nullable=False,default=True)
    user_instance_create_time = db.Column(db.DateTime, comment="创建时间",nullable=False,default=datetime.now)
    user_instance_update_time = db.Column(db.DateTime, comment="更新时间",nullable=False,default=datetime.now)
    user_instance_is_deleted = db.Column(db.Integer, comment="是否删除",nullable=False,default=False)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)

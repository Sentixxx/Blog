# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class UserGroup(BaseModel):
    __tablename__ = "user_group"
    user_group_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="用户组ID")
    user_group_name = db.Column(db.String(255), comment="用户组名",nullable=False)
    user_group_permission = db.Column(db.String(255), comment="权限",nullable=False)
    user_group_create_time = db.Column(db.DateTime, comment="创建时间",nullable=False,default=datetime.now)
    user_group_update_time = db.Column(db.DateTime, comment="更新时间",nullable=False,default=datetime.now)
    user_group_is_deleted = db.Column(db.Integer, comment="是否删除",nullable=False,default=False)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)



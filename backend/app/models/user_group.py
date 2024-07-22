# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class UserGroup(BaseModel):
    __tablename__ = "user_group"
    user_group_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="用户组ID")
    user_group_name = db.Column(db.String(255), comment="用户组名",nullable=False)
    user_group_permission = db.Column(db.String(255), comment="权限",nullable=False)



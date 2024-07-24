# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class UserGroup(BaseModel):
    __tablename__ = "user_group"
    user_group_name = db.Column(db.String(255), comment="用户组名",nullable=False)
    user_group_permission = db.Column(db.String(255), comment="权限",nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('user_group_name', 'user_group_permission', name='user_group_pk'),
    )

def add_group(data,sess,ret):
    if data.get('user_group_name') is None:
        ret['error_msg'] = "组名不能为空"
        return sess , ret
    if data.get('user_group_permission') is None:
        ret['error_msg'] = "权限不能为空"
        return sess , ret
    
    result = UserGroup.query.filter(UserGroup.user_group_name==data.get('user_group_name'),UserGroup.user_group_permission == data.get('user_group_permission'),UserGroup.is_deleted==0).first()

    if result is None:
        newGroup = UserGroup(user_group_name=data.get('user_group_name'),user_group_permission=data.get('user_group_permission'))
        sess.add(newGroup)
        return sess , ret
    else:
        ret['error_msg'] = "用户组权限已存在"
        return sess , ret
    
def delete_group(data,sess,ret):
    name = data.get('user_group_name')
    if name is None:
        ret['error_msg'] = "组名为空"
        return sess , ret
    results = UserGroup.query.filter_by(Uuser_group_name=name).all()
    if results:
        for result in results:
            if result.is_deleted == 0:
                result.is_deleted = 1
                sess = result.add(sess)
    else:
        ret['error_msg'] = "用户组不存在"
    return sess , ret

def delete_permission(data,sess,ret):
    name = data.get('user_group_name')
    perm = data.get('user_group_permission')
    result = UserGroup.query.filter(UserGroup.user_group_name==name,UserGroup.user_group_permission==perm).first()
    if(result):
            result.is_deleted = 1
            sess = result.add(sess)
            return sess , ret
    else:
        ret['error_msg'] = "用户组不存在"
    return sess , ret

def update_group(data,sess,ret):
    name = data.get('user_group_name')
    perm = data.get('user_group_permission')
    result = UserGroup.query.filter(UserGroup.user_group_name==name,UserGroup.user_group_permission==perm).first()
    if(result):
        if data.get('new_user_group_permission') is not None:
            result.user_group_permission = data.get('new_user_group_permission')
        sess = result.add(sess)
        return sess , ret
    else:
        ret['error_msg'] = "用户组权限不存在"
    return sess , ret
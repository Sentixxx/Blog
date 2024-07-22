# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.models.base_model import BaseModel


class SysLog(BaseModel):
    __tablename__ = "sys_log"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="日志ID")
    log_module = db.Column(db.String(255), comment="模块",nullable=False)
    log_level = db.Column(db.String(255), comment="级别",nullable=False)
    log_content = db.Column(db.String(255), comment="内容",nullable=False)
    log_browser = db.Column(db.String(255), comment="浏览器",nullable=False)
    log_browser_version = db.Column(db.String(255), comment="浏览器版本",nullable=False)
    log_ip = db.Column(db.String(255), comment="IP",nullable=False)
    log_request_url = db.Column(db.String(255), comment="请求URL",nullable=False)
    log_create_time = db.Column(db.DateTime, comment="创建时间",nullable=False,default=datetime.now)
    log_create_by = db.Column(db.String(255), comment="创建人",nullable=False)
    log_is_deleted = db.Column(db.Integer, comment="是否删除",nullable=False,default=False)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)




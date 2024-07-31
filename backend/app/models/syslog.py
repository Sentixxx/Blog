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
    log_create_by = db.Column(db.String(255), comment="创建人",nullable=False)
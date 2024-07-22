from app.extensions import db
from datetime import datetime
import sys
import traceback

class BaseModel(db.Model):
    __abstract__ = True

    create_at = db.Column(db.DateTime, comment="创建时间", nullable=False,default=datetime.now())
    update_at = db.Column(db.DateTime, comment="更新时间", nullable=False,default=datetime.now())
    is_deleted = db.Column(db.Integer, comment="是否删除", nullable=False, default=False)
    note1 = db.Column(db.String(255), comment="备注1",nullable=True)
    note2 = db.Column(db.String(255), comment="备注2",nullable=True)

    def add(self, session):
        try:
            session.add(self)
        except Exception as e:
            traceback.print_exc()
            session.rollback()
            return session
        return session
    
    # def save(self, session):
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         traceback.print_exc()
    #         session.rollback()
    #         return False
    #     return True
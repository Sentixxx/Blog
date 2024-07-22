from app.extensions import db
from app.models.book import Book
from app.models.user_instance import UserInstance
from app.models.borrow import Borrow
from app.models.book_instance import BookInstance
from app.models.user_group import UserGroup
from app.models.message import Message
from app.models.syslog import SysLog

def init_db_table():
    db.drop_all()
    print("db drop success")
    db.create_all()
    print("db create success")
    db.session.commit()
    print("db commit success")
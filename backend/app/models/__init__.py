from app.extensions import db
from app.models.book import *
from app.models.user_instance import *
from app.models.borrow import *
from app.models.book_instance import *
from app.models.user_group import *
from app.models.message import *
from app.models.syslog import *

def init_db_table():
    db.drop_all()
    print("db drop success")
    db.create_all()
    print("db create success")
    sess = db.session()
    UserGroup(user_group_name='super_admin',user_group_permission='all').add(sess)
    UserGroup(user_group_name='user',user_group_permission='basic').add(sess)
    UserGroup(user_group_name='user',user_group_permission='borrow').add(sess)
    sess.commit()
    print("db commit success")
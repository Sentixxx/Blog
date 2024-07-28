from app.extensions import db
from app.models.user_instance import UserInstance

def get_user_info(data,sess,ret):
    user_id = data.get('user_id')
    if(user_id is None):
        ret['error_msg'] = "参数错误"
        return sess,ret
    
    user = sess.query(UserInstance).filter(UserInstance.user_id == user_id).first()
    if user is None:
        ret['error_msg'] = "用户不存在"
        return sess,ret
    else:
        for key in user.__dict__:
            if key[0] != '_':
                ret[key] = getattr(user,key)
        return sess,ret
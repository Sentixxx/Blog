from app.extensions import db
from app.models.user_instance import UserInstance

def get_user_info(user_id,ret):
    if(user_id is None):
        ret['error_msg'] = "参数错误"
        return ret
    
    user = db.session.query(UserInstance).filter(UserInstance.user_instance_id == user_id).first()
    if user is None:
        ret['error_msg'] = "用户不存在"
        return ret
    else:
        for key in user.__dict__:
            if key[0] != '_' and key != 'user_instance_password':
                ret[key] = getattr(user,key)
        return ret
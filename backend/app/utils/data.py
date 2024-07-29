from app.extensions import db
from flask import jsonify
from app.config import Config
import hashlib
import time
import base64
import hmac

def submit(sess):
    try:
        sess.commit()
    except Exception as e:
        print(e)
        sess.rollback()
        return False
    return True

def to_json(results):
    ret = []
    print(results)
    for result in results:
        ret.append(result.to_dict())
    return jsonify(ret)

def to_dict(results):
    ret = []
    for result in results:
        ret.append(result.to_dict())
    return ret

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
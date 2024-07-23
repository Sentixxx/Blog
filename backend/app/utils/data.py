from app.extensions import db
from flask import jsonify

def submit(sess):
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        return False
    return True

def to_json(results):
    ret = []
    print(results)
    for result in results:
        ret.append(result.to_dict())
    return jsonify(ret)
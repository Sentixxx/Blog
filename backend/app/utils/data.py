from app.extensions import db


def submit(sess):
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        return False
    return True
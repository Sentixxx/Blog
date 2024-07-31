from app.models import Borrow

from datetime import datetime

def delay_borrow(data,sess,results):
    borrow_id = data.get('borrow_id')
    extra_return_time = data.get('extra_return_time')
    borrow = Borrow.query.filter(Borrow.is_deleted==0,Borrow.borrow_id==borrow_id).first()
    if borrow is None:
        results['error_msg'] = "借阅记录不存在"
        return sess,results
    if extra_return_time is None:
        results['error_msg'] = "缺少延期时间"
        return sess,results
    
    if datetime.strptime(extra_return_time, "%Y-%m-%dT%H:%M:%S.%fZ") - borrow.should_return_time < datetime.timedelta(0):
        results['error_msg'] = "延期时间不合法"
        return sess,results
    
    if datetime.strptime(extra_return_time, "%Y-%m-%dT%H:%M:%S.%fZ") - borrow.create_time > datetime.timedelta(days=30):
        results['error_msg'] = "延期时间过长"
        return sess,results
    
    if borrow.is_completed == 1:
        results['error_msg'] = "借阅已完成"
        return sess,results
    
    borrow.extra_return_time = extra_return_time

    sess = borrow.add(sess)
    return sess,results



    
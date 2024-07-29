from app.models import BookInstance,Borrow
from uuid import uuid4


def add_book_instance(data: dict,sess: any,ret: dict) -> tuple:
    '''
    添加书籍实体，传入(data,sess,ret)三个参数，返回(sess,ret)两个参数
    '''
    book_id = data.get('book_id')
    if book_id is None:
        ret['error_msg'] = "缺少图书信息ID"
        return sess , ret
    
    ret['book_id'] = book_id

    code = data.get('book_instance_id')
    ret['book_instance_id'] = code

    book_instance_location = data.get('book_instance_location')
    ret['book_instance_location'] = book_instance_location

    if book_instance_location is None:
        result['error_msg'] = "缺少图书位置信息"
        return sess , ret

    if code is not None:
        result = BookInstance.query.filter_by(book_instance_id=code).first()
        if(result):
            if(result.is_deleted == 1):
                ret['note'] = "图书已被删除"
                if(result.book_id != data['book_id']):
                    ret['error_msg'] = "图书信息ID不匹配"
                    return sess , ret
                
                result.is_deleted = 0
                result.note1 = None

                result.book_instance_location = book_instance_location

                sess = result.add(sess)

                return sess , ret
            else:
                ret['error_msg'] = "图书已存在"
                return sess , ret
            
    code = uuid4()
    while BookInstance.query.filter_by(book_instance_id=code).first():
        code = uuid4()
    

    newBookInstance = BookInstance(book_instance_id = code,book_id = book_id,book_instance_location = book_instance_location)
    sess = newBookInstance.add(sess)
    
    return sess , ret

def update_book_instance(book_instance_id:str,data:dict,sess:any,ret:dict) -> tuple:
    result = BookInstance.query.filter(BookInstance.is_deleted ==0,BookInstance.book_instance_id==book_instance_id).first()

    modify_item = {
        'book_instance_location',
        'book_instance_status'
    }

    if result is None:
        ret['error_msg'] = "图书不存在"
        return sess , ret

    for item in modify_item:
        if data.get(item) is not None:
            setattr(result,item,data.get(item))

    sess = result.add(sess)
    sess.flush()

    ret = result.to_dict()

    return sess , ret

def delete_book_instance(book_instance_id: str, data: dict, sess:any, ret:dict) -> tuple:
    result = BookInstance.query.filter_by(book_instance_id=book_instance_id).first()
    if(result):
        if result.is_deleted == 1:
            ret['error_msg'] = "图书已被删除"
            return sess , ret
        result.is_deleted = 1
        if data.get('reason') is not None:
            result.note1 = '原因：' + data.get('reason')
        ret['book_id'] = result.book_id
        sess = result.add(sess)
    else:
        ret['error_msg'] = "图书不存在"
    return sess , ret

def borrow_book(data: dict, sess: any, ret: dict) -> tuple:
    '''
    借阅书籍实体，传入(data,sess,ret)三个参数，返回(sess,ret)两个参数
    '''
    book_instance_id = data.get('book_instance_id')
    if book_instance_id is None:
        ret['error_msg'] = "缺少书籍实体ID"
        return sess , ret

    ret['book_instance_id'] = book_instance_id

    user_instance_id = data.get('user_instance_id')
    if user_instance_id is None:
        ret['error_msg'] = "缺少用户ID"
        return sess , ret

    ret['user_instance_id'] = user_instance_id

    result = BookInstance.query.filter(BookInstance.is_deleted == 0,BookInstance.book_instance_id == book_instance_id).first()
    if result is None:
        ret['error_msg'] = "书籍不存在"
        return sess , ret

    if result.book_instance_status != 0:
        ret['error_msg'] = "书籍不可借阅"
        return sess , ret

    result.book_instance_status = 1
    sess = result.add(sess)

    newBorrow = Borrow(user_instance_id = user_instance_id,book_instance_id = book_instance_id,is_completed = 0)

    sess = newBorrow.add(sess)
    sess.flush()

    ret['borrow_id'] = newBorrow.borrow_id

    return sess , ret
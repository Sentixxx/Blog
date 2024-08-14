from app.models import Book, BookInstance

def add_book(data, sess, ret):
    optional_attrs = ['book_pic','book_type']
    must_attrs = ['book_name','book_author','book_press','book_isbn_code','book_introduce']

    result = Book.query.filter(Book.is_deleted==0,Book.book_isbn_code==data.get('book_isbn_code')).first()

    if result is not None:
        ret['error_msg'] = "图书信息已存在"
        return sess , ret
    
    newBook = Book(book_cur_stock_num=0)
    for attr in must_attrs:
        if data.get(attr) is None:
            ret['error_msg'] = "缺少必要信息"
            return sess , ret
        setattr(newBook,attr,data.get(attr))
    for attr in optional_attrs:
        if data.get(attr) is not None:
            setattr(newBook,attr,data.get(attr))
    
    sess = newBook.add(sess)
    sess.flush()

    ret = newBook.to_dict()
    # ret['book_id'] = newBook.book_id

    return sess , ret
    
    
def add_stock_num(book_instance_id,sess,ret):
    book = BookInstance.query.filter(BookInstance.is_deleted==0,BookInstance.book_instance_id==book_instance_id).first()

    if book is None:
        ret['error_msg'] = "图书实例ID不存在"
        return sess , ret

    book_id = book.book_id

    result = Book.query.filter(Book.is_deleted==0,Book.book_id==book_id).first()
    
    if result is None:
        ret['error_msg'] = "图书ID不存在"
        return sess , ret
    
    result.book_cur_stock_num += 1
    sess = result.add(sess)

    ret['book_cur_stock_num'] = result.book_cur_stock_num

    return sess , ret

def reduce_stock_num(book_id,sess,ret):
    result = Book.query.filter(Book.is_deleted==0,Book.book_id==book_id).first()
    
    if result is None:
        ret['error_msg'] = "图书ID不存在"
        return sess , ret
    
    if result.book_cur_stock_num == 0:
        ret['error_msg'] = "图书库存为0"
        return sess , ret
    
    result.book_cur_stock_num -= 1
    sess = result.add(sess)

    ret['book_cur_stock_num'] = result.book_cur_stock_num

    return sess , ret

def delete_book(book_id,sess,ret):
    result = Book.query.filter(Book.is_deleted==0,Book.book_id==book_id).first()

    if result is None:
        ret['error_msg'] = "图书ID不存在"
        return sess , ret
    
    if result.book_cur_stock_num > 0:
        ret['error_msg'] = "图书库存不为0"
        return sess , ret
    
    result.is_deleted = 1
    sess = result.add(sess)

    return sess , ret

def update_book(book_id,data,sess,ret):
    result = Book.query.filter(Book.is_deleted==0,Book.book_id==book_id).first()
    
    if result is None:
        ret['error_msg'] = "图书ID不存在"
        return sess , ret
    
    optional_attrs = ['book_pic','book_type']
    must_attrs = ['book_name','book_author','book_press','book_isbn_code','book_introduce']
    ok = False
    for attr in must_attrs:
        if data.get(attr) is not None:
            setattr(result,attr,data.get(attr))
            ok = True
    if not ok:
        ret['error_msg'] = "缺少必要信息"
        return sess , ret
    for attr in optional_attrs:
        if data.get(attr) is not None:
            setattr(result,attr,data.get(attr))
    
    sess = result.add(sess)
    sess.flush()

    ret = result.to_dict()

    return sess , ret
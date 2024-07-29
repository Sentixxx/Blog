import request from '@/utils/request'

const BOOK_INSTANCE_BASE_URL = '/book_instance'

class BookInstanceAPI {
    /**
     * @returns 图书信息
     */

    static getAll(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_BASE_URL}/info/all`,
            method: 'get'
        })
    }

    static getById(book_id: number): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_BASE_URL}/info/book_id/${book_id}`,
            method: 'get'
        })
    }

    static get(book_instance_id: string): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_BASE_URL}/info/book_instance/${book_instance_id}`,
            method: 'get'
        })
    }

    static add(): Promise<BookInstance> {
        return request<any, BookInstance>({
            url: `${BOOK_INSTANCE_BASE_URL}/add`,
            method: 'post'
        })
    }

    static delete(book_instance_id: string): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_BASE_URL}/delete/${book_instance_id}`,
            method: 'delete'
        })
    }

    static update(book_instance_id: string): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_BASE_URL}/update/${book_instance_id}`,
            method: 'put'
        })
    }

    static borrow(
        book_instance_id: string,
        user_instance_id: any,
        should_return_time: any
    ): Promise<BookInstance> {
        return request<any, BookInstance>({
            url: `${BOOK_INSTANCE_BASE_URL}/borrow`,
            method: 'post',
            params: {
                user_instance_id: user_instance_id,
                should_return_time: should_return_time,
                book_instance_id: book_instance_id
            }
        })
    }

    static returnBookInstance(book_instance_id: string): Promise<BookInstance> {
        return request<any, BookInstance>({
            url: `${BOOK_INSTANCE_BASE_URL}/return/${book_instance_id}`,
            method: 'post'
        })
    }
}

export default BookInstanceAPI

export interface BookInstance extends BasicAPI {
    book_id: number
    book_instance_id: string
    book_instance_status: number
    borrow_id?: number
    book_instance_location: string
}

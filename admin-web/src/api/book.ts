import request from '@/utils/request'

const BOOK_BASE_URL = '/book'

const BOOK_INSTANCE_URL = '/book_instance'

class BookAPI {
    /**
     * @returns 图书信息
     */
    static getBookInfoAll(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/info/all`,
            method: 'get'
        })
    }

    static getBookInstanceAll(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_BASE_URL}/instance/all`,
            method: 'get'
        })
    }

    static getBookInfo(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/info`,
            method: 'get'
        })
    }

    static getBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_BASE_URL}/instance`,
            method: 'get'
        })
    }

    static addBookInfo(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/add`,
            method: 'post'
        })
    }

    static addBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_BASE_URL}/add`,
            method: 'post'
        })
    }

    static deleteBookInfo(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/delete`,
            method: 'delete'
        })
    }

    static deleteBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_BASE_URL}/delete`,
            method: 'delete'
        })
    }

    static updateBookInfo(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/update`,
            method: 'put'
        })
    }

    static updateBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_BASE_URL}/update`,
            method: 'put'
        })
    }

    static borrowBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_URL}/borrow`,
            method: 'post'
        })
    }

    static returnBookInstance(): Promise<BookInstance[]> {
        return request<any, BookInstance[]>({
            url: `${BOOK_INSTANCE_URL}/return`,
            method: 'post'
        })
    }
}

export default BookAPI

export interface BookInfo {
    book_id: string
    book_name: string
    book_author?: string
    book_isbn_code: string
    book_press?: string
}

export interface BookInstance {
    book_id: string
    book_instance_id: string
    book_instance_status: string
    borrow_id?: string
    book_instance_location: string
}

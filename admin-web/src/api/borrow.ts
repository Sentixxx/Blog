import request from '@/utils/request'

const Borrow_BASE_URL = '/borrow'

class BorrowAPI {
    /**
     * @returns 图书信息
     */

    static getAll(): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/info/all`,
            method: 'get'
        })
    }

    static getByBookId(book_id: number): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/info/book_id/${book_id}`,
            method: 'get'
        })
    }

    static getByUserId(user_id: number): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/info/user_id/${user_id}`,
            method: 'get'
        })
    }
}

export default BorrowAPI

export interface BorrowLog extends BasicAPI {
    borrow_id: number
    book_name: string
    borrow_time: string
    is_completed: number
    should_return_time: string
    extra_return_time?: string
    book_instance_id: string
    book_author?: string
    book_press?: string
    book_isbn_code?: string
    book_pic?: string
}

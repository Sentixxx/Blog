import request from '@/utils/request'

const Borrow_BASE_URL = '/borrow'

class BorrowAPI {
    /**
     * @returns 图书信息
     */

    static search(search_option: string, search_value: string): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/search`,
            method: 'get',
            params: {
                [search_option]: search_value
            }
        })
    }

    static getAll(): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/all`,
            method: 'get'
        })
    }

    static getByBookInstanceId(book_instance_id: string): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/book_instance_id/${book_instance_id}`,
            method: 'get'
        })
    }

    static getByUserId(user_id: number): Promise<BorrowLog[]> {
        return request<any, BorrowLog[]>({
            url: `${Borrow_BASE_URL}/user_id/${user_id}`,
            method: 'get'
        })
    }

    static getByBorrowId(borrow_id: number): Promise<BorrowLog> {
        return request<any, BorrowLog>({
            url: `${Borrow_BASE_URL}/borrow_id/${borrow_id}`,
            method: 'get'
        })
    }

    static delay(borrow_id: number, extra_return_time: string): Promise<BorrowLog> {
        return request<any, BorrowLog>({
            url: `${Borrow_BASE_URL}/delay/${borrow_id}`,
            method: 'put',
            params: {
                extra_return_time: extra_return_time
            }
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

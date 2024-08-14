import request from '@/utils/request'

const BOOK_BASE_URL = '/book'
class BookAPI {
    /**
     * @returns 图书信息
     */
    static getAll(): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/all`,
            method: 'get'
        })
    }

    static get(book_id: number): Promise<BookInfo> {
        return request<any, BookInfo>({
            url: `${BOOK_BASE_URL}/${book_id}`,
            method: 'get'
        })
    }

    static search(search_option: string, search_value: string): Promise<BookInfo[]> {
        console.log(search_option)
        console.log(search_value)
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/search`,
            method: 'get',
            params: {
                [search_option]: search_value
            }
        })
    }

    static add(data: BookInfo): Promise<BookInfo> {
        return request<any, BookInfo>({
            url: `${BOOK_BASE_URL}`,
            method: 'post',
            params: {
                ...data
            }
        })
    }

    static delete(book_id: number): Promise<BookInfo[]> {
        return request<any, BookInfo[]>({
            url: `${BOOK_BASE_URL}/${book_id}`,
            method: 'delete'
        })
    }

    static updateBook(book_id: number, data: BookInfo): Promise<BookInfo> {
        return request<any, BookInfo>({
            url: `${BOOK_BASE_URL}/${book_id}`,
            method: 'put',
            params: {
                ...data
            }
        })
    }
}

export default BookAPI

export interface BookInfo extends BasicAPI {
    book_id: number
    book_name: string
    book_author?: string
    book_isbn_code: string
    book_press?: string
    book_introduce?: string
    book_pic?: string
    book_type?: string
    book_cur_stock_num?: number
}

declare global {
    /**
     * 响应数据
     */

    interface BasicAPI {
        create_time?: string
        update_time?: string
        is_deleted?: number
        note1?: string
        note2?: string
    }
    interface ResponseData<T = any> {
        status: string
        results: T
        msg: string
    }

    /**
     * 页签对象
     */
    interface TagView {
        /** 页签名称 */
        name: string
        /** 页签标题 */
        title: string
        /** 页签路由路径 */
        path: string
        /** 页签路由完整路径 */
        fullPath: string
        /** 页签图标 */
        icon?: string
        /** 是否固定页签 */
        affix?: boolean
        /** 是否开启缓存 */
        keepAlive?: boolean
        /** 路由查询参数 */
        query?: any
    }
    /**
     * System Settings
     */
    interface AppSettings {
        title: string
        version: string
        showSettings: boolean
        fixedHeader: boolean
        tagsView: boolean
        sidebarLogo: boolean
        layout: string
        themeColor: string
        themeMode: string
        size: string
        language: string
        watermarkEnabled: boolean
        watermarkContent: string
    }
}

export {}

/**
 * 判断是否是外部链接
 *
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path: string) {
    const isExternal = /^(https?:|http?:|mailto:|tel:)/.test(path)
    return isExternal
}

/**
 * @description: 处理路由地址
 * @param {string} routePath 路由路径 /user
 * @param {string} basePath 基础路径 http://www.xxx.com
 * @return {string} 完整路由地址 http://www.xxx.com/user
 */
export function resolvePath(routePath: string, basePath: string) {
    if (isExternal(routePath)) {
        return routePath
    }
    if (isExternal(basePath)) {
        return basePath
    }
    const base = new URL(basePath, window.location.origin)
    console.log('newroutePath', routePath)
    const fullpath = new URL(routePath, base)
    return fullpath.toString()
}

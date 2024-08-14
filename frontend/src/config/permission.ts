import { NavigationGuardNext, RouteLocationNormalized, RouteRecordRaw } from 'vue-router'

import NProgress from '@/utils/nprogress'
import { TOKEN_KEY } from '@/enums/cacheEnum'
import router from '@/router'
import { useUserStore } from '@/stores'

export function setupPermission() {
    // 黑名单路由
    const blackList = ['/borrow', '/','/user','/manage']
    console.log(blackList)
    router.beforeEach(async (to, from, next) => {
        NProgress.start()
        const hasToken = localStorage.getItem(TOKEN_KEY)

        if (hasToken) {
            if (to.path === '/login') {
                // 如果已登录，跳转到首页
                next({ path: '/' })
                NProgress.done()
            } else {
                const userStore = useUserStore()
                const hasgroup = userStore.user.user_instance_id

                if (hasgroup) {
                    // 如果未匹配到任何路由，跳转到404页面
                    if (to.matched.length === 0) {
                        next(from.name ? { name: from.name } : '/404')
                    } else {
                        // 如果路由参数中有 title，覆盖路由元信息中的 title
                        const title = (to.params.title as string) || (to.query.title as string)
                        if (title) {
                            to.meta.title = title
                        }
                        next()
                    }
                } else {
                    try {
                        await userStore.getUserInfo()
                        next({ ...to, replace: true })
                    } catch (error) {
                        // 移除 token 并重定向到登录页，携带当前页面路由作为跳转参数
                        await userStore.resetToken()
                        redirectToLogin(to, next)
                        NProgress.done()
                    }
                }
            }
        } else {
            // 未登录
            if (!blackList.includes(to.path)) {
                next() // 在白名单，直接进入
            } else {
                redirectToLogin(to, next)
                NProgress.done()
            }
        }
    })

    router.afterEach(() => {
        NProgress.done()
    })
}

/** 重定向到登录页 */
function redirectToLogin(to: RouteLocationNormalized, next: NavigationGuardNext) {
    const params = new URLSearchParams(to.query as Record<string, string>)
    const queryString = params.toString()
    const redirect = queryString ? `${to.path}?${queryString}` : to.path
    next(`/login?redirect=${encodeURIComponent(redirect)}`)
}

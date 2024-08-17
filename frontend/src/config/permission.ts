import { NavigationGuardNext, RouteLocationNormalized, RouteRecordRaw } from 'vue-router'

import NProgress from '@/utils/nprogress'
import { TOKEN_KEY } from '@/enums/cacheEnum'
import router from '@/router'
import { useUserStore, useUserStoreHook } from '@/stores'
import { isAdmin } from '@/utils/perm'

export function setupPermission() {
    const blackList = ['/borrow','/user','/manage/book','/manage/user']
    const adminList = ['/manage/book','/manage/user']
    router.beforeEach(async (to, from, next) => {
        NProgress.start()
        const hasToken = localStorage.getItem(TOKEN_KEY)

        if (hasToken) {
            if (to.path === '/login') {
                next({ path: '/' })
                NProgress.done()
            } else {
                await useUserStoreHook().getUserInfo()
                if(!isAdmin() && adminList.includes(to.path)){
                    next('/401')
                }
                if (to.matched.length === 0) {
                    next(from.name ? { name: from.name } : '/404')
                } else {
                    const title = (to.params.title as string) || (to.query.title as string)
                    if (title) {
                        to.meta.title = title
                    }
                    next()
                } 
            }
        } else {
            if (!blackList.includes(to.path)) {
                next()
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

function redirectToLogin(to: RouteLocationNormalized, next: NavigationGuardNext) {
    const params = new URLSearchParams(to.query as Record<string, string>)
    const queryString = params.toString()
    const redirect = queryString ? `${to.path}?${queryString}` : to.path
    next(`/login?redirect=${encodeURIComponent(redirect)}`)
}

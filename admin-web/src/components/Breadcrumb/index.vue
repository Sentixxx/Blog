<template>
    <el-breadcrumb class="flex-y-center">
        <transition-group enter-active-class="animate__animated animate__fadeInRight">
            <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="item.path">
                <span
                    v-if="item.redirect === 'noredirect' || index === breadcrumbs.length - 1"
                    class="color-gray-400"
                    >{{ translateRouteTitle(item.meta.title) }}</span
                >
                <a v-else @click.prevent="handleLink(item)">
                    {{ translateRouteTitle(item.meta.title) }}
                </a>
            </el-breadcrumb-item>
        </transition-group>
    </el-breadcrumb>
</template>

<script setup lang="ts">
import { RouteLocationMatched } from 'vue-router'
import { compile } from 'path-to-regexp'
import router from '@/router'
import { translateRouteTitle } from '@/utils/i18n'

const currentRoute = useRoute()
const pathCompile = (path: string) => {
    const { params } = currentRoute
    const toPath = compile(path)
    return toPath(params)
}

const breadcrumbs = ref<Array<RouteLocationMatched>>([])

function getBreadcrumb() {
    let matched = currentRoute.matched.filter((item) => item.meta && item.meta.title)
    for (const item of matched) {
        console.log(item)
    }
    const first = matched[0]
    if (!isHome(first)) {
        matched = [{ path: '/home', meta: { title: 'Home' } } as any].concat(matched)
    }
    breadcrumbs.value = matched.filter((item) => {
        if (item.meta && item.meta.title == 'default_book_id') {
            item.meta.title = currentRoute.meta.title
        }
        return item.meta && item.meta.title && item.meta.breadcrumb !== false
    })
    // console.log(breadcrumbs)
}

function isHome(route: RouteLocationMatched) {
    const name = route && route.name
    if (!name) {
        return false
    }
    console.log(name.toString().trim().toLocaleLowerCase())
    return name.toString().trim().toLocaleLowerCase() === 'Home'.toLocaleLowerCase()
}

function handleLink(item: any) {
    const { redirect, path } = item
    if (redirect) {
        router.push(redirect).catch((err) => {
            console.warn(err)
        })
        return
    }
    router.push(pathCompile(path)).catch((err) => {
        console.warn(err)
    })
}

watch(
    () => currentRoute.path,
    (path) => {
        if (path.startsWith('/redirect/')) {
            return
        }
        getBreadcrumb()
    }
)

onBeforeMount(() => {
    getBreadcrumb()
})
</script>

<style lang="scss" scoped>
// 覆盖 element-plus 的样式
.el-breadcrumb__inner,
.el-breadcrumb__inner a {
    font-weight: 400 !important;
}
</style>

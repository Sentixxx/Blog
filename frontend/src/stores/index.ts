import type { App } from 'vue'
import { createPinia } from 'pinia'

const store = createPinia()

export function setupStore(app: App<Element>) {
    app.use(store)
}

export * from './modules/tagsView'
export * from './modules/permission'
export * from './modules/user'
export * from './modules/settings'
export * from './modules/app'
export { store }

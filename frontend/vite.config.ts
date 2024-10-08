import { fileURLToPath, URL } from 'node:url'

import { defineConfig, UserConfig, ConfigEnv, loadEnv } from 'vite'
import path from 'path'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import UnoCSS from 'unocss/vite'
import { name, version, dependencies, devDependencies } from './package.json'

const __APP_INFO__ = {
    pkg: { name, version, dependencies, devDependencies },
    buildTimestamp: Date.now()
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
    const env = loadEnv(mode, process.cwd())
    return {
        plugins: [
            vue(),
            vueJsx(),
            vueDevTools(),
            AutoImport({
                imports: ['vue', 'pinia', 'vue-router', '@vueuse/core', 'vue-i18n'],
                eslintrc: {
                    enabled: true,
                    filepath: './.eslintrc-auto-import.json'
                },
                resolvers: [ElementPlusResolver(), IconsResolver({})],
                dts: fileURLToPath(new URL('./src/types/auto-imports.d.ts', import.meta.url))
            }),
            Components({
                resolvers: [ElementPlusResolver(), IconsResolver({ enabledCollections: ['ep'] })],
                dts: fileURLToPath(new URL('./src/types/components.d.ts', import.meta.url)),
                dirs: ['src/components', 'src/**/components']
            }),
            Icons({
                autoInstall: true
            }),
            createSvgIconsPlugin({
                // 指定需要缓存的图标文件夹
                iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
                // 指定symbolId格式
                symbolId: 'icon-[dir]-[name]'
            }),
            UnoCSS({
                /* options */
            })
        ],
        resolve: {
            alias: {
                '@': path.join(__dirname, './src')
            }
        },
        css: {
            // CSS 预处理器
            preprocessorOptions: {
                //define global scss variable
                scss: {
                    javascriptEnabled: true,
                    additionalData: `@use "@/styles/variables.scss" as *;`
                }
            }
        },
        server: {
            fs: {
                cachedChecks: false
            },
            host: '0.0.0.0',
            port: Number(env.VITE_APP_PORT),
            proxy: {
                [env.VITE_APP_BASE_API]: {
                    target: 'http://0.0.0.0:8090',
                    changeOrigin: true,
                    rewrite: (path: string) => {
                        const newPath = path.replace(new RegExp(`^${env.VITE_APP_BASE_API}`), '')
                        console.log(env.VITE_APP_BASE_API)
                        console.log(`Rewriting path from ${path} to ${newPath}`)
                        return newPath
                    },
                    configure: (proxy, options) => {
                        // Add a logging middleware
                        proxy.on('proxyReq', (proxyReq, req, res) => {
                            console.log(`[Proxy] ${req.method} ${req.url} -> ${proxyReq.path}`)
                        })
                        proxy.on('proxyRes', (proxyRes, req, res) => {
                            console.log(
                                `[Proxy] Response from target: ${proxyRes.statusCode} ${req.url}`
                            )
                        })
                    }
                }
            }
        },
        define: {
            __APP_INFO__: JSON.stringify(__APP_INFO__) // expose app info to client
        }
    }
})

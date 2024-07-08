import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
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

const rootDir = fileURLToPath(new URL('.', import.meta.url))
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsx(),
        vueDevTools(),
        AutoImport({
            imports: ['vue'],
            eslintrc: {
                enabled: false,
                filepath: './.eslintrc-auto-import.json'
            },
            resolvers: [ElementPlusResolver(), IconsResolver({})],
            dts: fileURLToPath(new URL('./src/types/auto-imports.d.ts', import.meta.url))
        }),
        Components({
            resolvers: [ElementPlusResolver(), IconsResolver({ enabledCollections: ['ep'] })],
            dts: fileURLToPath(new URL('./src/types/components.d.ts', import.meta.url))
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
            '@': rootDir + '/src'
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
    }
})

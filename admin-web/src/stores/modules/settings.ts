import defaultSettings from '@/config/settings'
import { ThemeEnum } from '@/enums/themeEnum'
import Color from 'color'

type SettingsValue = boolean | string

export const useSettingsStore = defineStore('settings', () => {
    const settingsVisible = ref(false)

    const tagsView = useStorage<boolean>('tagsView', defaultSettings.tagsView)

    const sidebarLogo = useStorage<boolean>('sidebarLogo', defaultSettings.sidebarLogo)

    const fixedHeader = useStorage<boolean>('fixedHeader', defaultSettings.fixedHeader)

    const layout = useStorage<string>('layout', defaultSettings.layout)

    const themeColor = useStorage<string>('themeColor', defaultSettings.themeColor)

    const themeMode = useStorage<string>('themeMode', defaultSettings.themeMode)

    const watermarkEnabled = useStorage<boolean>(
        'waterMarkEnabled',
        defaultSettings.watermarkEnabled
    )

    watch(
        [themeMode, themeColor],
        ([newTheme, newThemeColor], [oldTheme, oldThemeColor]) => {
            if (newTheme !== oldTheme) {
                if (newTheme === ThemeEnum.DARK) {
                    document.documentElement.classList.add('dark')
                } else {
                    document.documentElement.classList.remove('dark')
                }
            }

            if (newThemeColor !== oldThemeColor) {
                const rootStyle = document.documentElement.style
                rootStyle.setProperty(`--el-color-primary`, newThemeColor)
                rootStyle.setProperty(`--el-color-primary-dark-2`, newThemeColor)

                for (let i = 1; i < 10; i++) {
                    rootStyle.setProperty(
                        `--el-color-primary-light-${i}`,
                        `${Color(newThemeColor).alpha(1 - i * 0.1)}`
                    )
                }
            }
        },
        { immediate: true }
    )

    const settingsMap: Record<string, Ref<SettingsValue>> = {
        fixedHeader,
        tagsView,
        sidebarLogo,
        layout,
        watermarkEnabled
    }

    function setSetting({ key, value }: { key: string; value: SettingsValue }) {
        const setting = settingsMap[key]
        if (setting) {
            setting.value = value
        }
    }

    function setThemeMode(val: string) {
        themeMode.value = val
    }

    function setThemeColor(val: string) {
        themeColor.value = val
    }

    function setLayout(val: string) {
        layout.value = val
    }

    return {
        settingsVisible,
        tagsView,
        fixedHeader,
        sidebarLogo,
        layout,
        themeColor,
        themeMode,
        watermarkEnabled,
        setSetting,
        setThemeMode,
        setThemeColor,
        setLayout
    }
})

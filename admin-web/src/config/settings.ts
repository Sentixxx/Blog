import { LayoutEnum } from '@/enums/layoutEnum'
import { SizeEnum } from '@/enums/sizeEnum'
import { ThemeEnum } from '@/enums/themeEnum'
import { LanguageEnum } from '@/enums/languageEnum'

const { pkg } = __APP_INFO__

const defaultSettings: AppSettings = {
    title: pkg.name,
    version: pkg.version,
    showSettings: true,
    tagsView: true,
    fixedHeader: true,
    sidebarLogo: true,
    layout: LayoutEnum.LEFT,
    themeMode: ThemeEnum.LIGHT,
    size: SizeEnum.DEFAULT,
    themeColor: '#409eff',
    watermarkContent: pkg.name,
    watermarkEnabled: false,
    language: LanguageEnum.ZH_CN
}

export default defaultSettings

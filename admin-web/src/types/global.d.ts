declare global {

    /**
     * System Settings
     */
    interface AppSettings { 
        title: string;
        version: string;
        showSettings: boolean;
        fixedHeader: boolean;
        tagsView: boolean;
        sidebarLogo: boolean;
        layout: string;
        themeColor: string;
        themeMode: string;
        size: string;
        language: string;
        watermarkEnabled: boolean;
        watermarkContent: string;
    }
    
    /**
    * 组件数据源
    */
    interface OptionType {
        /** 值 */
        value: string | number;
        /** 文本 */
        label: string;
        /** 子列表  */
        children?: OptionType[];
    }
}

export {};
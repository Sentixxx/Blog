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
        navbarLayout: string;
        themeColor: string;
        themeMode: string;
        layoutSize: string;
        language: string;
        watermarkEnabled: boolean;
        watermarkContent: string;
    }
}

export {};
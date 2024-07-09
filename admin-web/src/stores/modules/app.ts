import defaultSettings from "@/config/settings";

import zhcn from "element-plus/es/locale/lang/zh-cn"
import en from "element-plus/es/locale/lang/en"
import { store } from "@/stores"
import { DeviceEnum } from "@/enums/deviceEnum";
import { SidebarStatusEnum } from "@/enums/sidebarStatusEnum";

export const useAppStore = defineStore("app", () => {
    const device = useStorage("device",DeviceEnum.DESKTOP);

    const layoutSize = useStorage("layoutSize",defaultSettings.layoutSize);

    const language = useStorage("language",defaultSettings.language);

    const sidebarStatus = useStorage("sidebarStatus",SidebarStatusEnum.OPENED);
    const sidebar = reactive({
        opened: sidebarStatus.value === SidebarStatusEnum.OPENED,withoutAnimation: false,
    });

    const activeTopMenuPath = useStorage("activeTopMenuPath","");

    const locale = computed(() => {
        if(language?.value == "en") {
            return en;
        }
        else {
            return zhcn;
        }
    });

    function toggleSidebar() {
        sidebar.opened = !sidebar.opened;
        sidebarStatus.value = sidebar.opened ? SidebarStatusEnum.OPENED : SidebarStatusEnum.CLOSED;
    }

    function closeSidebar() {
        sidebar.opened = false;
        sidebarStatus.value = SidebarStatusEnum.CLOSED;
    }

    function openSidebar() {
        sidebar.opened = true;
        sidebarStatus.value = SidebarStatusEnum.OPENED;
    }

    function toggleDevice(val: string) {
        device.value = val;
    }

    /**
     * @param {string} val 布局大小 default | small | large
     */
    function setLayoutSize(val: string) {
        layoutSize.value = val;
    }

    /**
     * @param {string} val 语言
     */
    function setLanguage(val: string) {
        language.value = val;
    }

    function setActiveTopMenuPath(val: string) {
        activeTopMenuPath.value = val;
    }

    return {
        device,
        sidebar,
        language,
        locale,
        layoutSize,
        activeTopMenuPath,
        toggleSidebar,
        closeSidebar,
        openSidebar,
        toggleDevice,
        setLayoutSize,
        setLanguage,
        setActiveTopMenuPath,
    };
});

export function useAppStoreHook() {
    return useAppStore(store);
}
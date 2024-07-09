import { setupStore } from '@/stores';
import { setupI18n } from '@/lang';
import { setupRouter } from '@/router';
import { setupElIcons } from './icons';
import type { App } from 'vue';

export default {
    install(app: App<Element>) {
        setupStore(app);
        setupI18n(app);
        setupRouter(app);
        setupElIcons(app);
    },
};
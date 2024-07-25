export default {
    route: {
        Dashboard: 'Dashboard',
        Book: 'Book',
        User: 'User'
    },
    login: {
        username: 'Username',
        password: 'Password',
        login: 'Login',
        rigiser: 'Register',
        capslock: 'Caps Lock is On',
        back: 'Back',
        message: {
            username: {
                required: 'Please enter Username'
            },
            password: {
                required: 'Please enter Password',
                min: 'The password can not be less than 6 digits'
            },
            captcha: {
                required: 'Please enter Captcha',
                error: 'Captcha error'
            }
        }
    },
    navbar: {
        notice: 'notification',
        langSelect: {
            tooltip: 'language select',
            message: {
                success: 'Language switch success'
            }
        },
        fullscreen: 'full screen',
        sizeSelect: {
            tooltip: 'layout size',
            default: 'default',
            large: 'large',
            small: 'small',
            message: {
                success: 'Layout size set successfully'
            }
        },
        settings: {
            project: 'Book Management System',
            tooltip: 'system settings',
            theme: 'theme',
            interface: 'interface',
            navigation: 'navigation',
            themeColor: 'theme color',
            tagsView: 'tags view',
            fixedHeader: 'fixed header',
            sidebarLogo: 'sidebar logo',
            message: {
                success: 'System settings success'
            }
        },
        dashboard: 'dashboard',
        logout: 'logout'
    }
}

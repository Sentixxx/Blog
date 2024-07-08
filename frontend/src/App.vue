<template>
    <div>
        <div id="bg"></div>
        <div id="app">
            <RouterView />
        </div>
    </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router';
import LoginView from './views/login/Index.vue';

export default {
    components: {
        RouterLink,
        RouterView,
        LoginView
    }
};
</script>

<style scoped>
body,
html {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}
#bg {
    background-image: url('./assets/pics/background.png');
    background-size: cover;
    position: fixed; /* 将背景层固定定位 */
    width: 100%;
    height: 100vh;
    overflow: hidden;
    z-index: -1; /* 设置z-index，保证背景层在内容之下 */
}
#app {
    height: 100%; /* 视需要设定，根据实际用途调整 */
    overflow: auto; /* 将滚动限制在内容层 */
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #000000;
    justify-content: center;
    margin: auto auto;
}
</style>

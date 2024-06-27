<template>
    <div id="app">
        <RouterView />
    </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router';
import LoginView from './views/login/LoginView.vue';

export default {
    components: {
        RouterLink,
        RouterView,
        LoginView
    }
};
</script>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    justify-content: center;
    margin: auto auto;
}
</style>

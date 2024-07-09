<template>
    <div class="wh-full" :class="classObj">
        <!--遮罩-->
        <div
            v-if="isMobile && isOpenSidebar"
            class="wh-full fixed-lt z-999 bg-black bg-opacity-30"
            @click="handleOutsideClick"
        ></div>

        <!--侧边栏-->
        <Sidebar class="sidebar-container" />

        <!--混合布局-->
        <div v-if="navbarLayout === LayoutEnum.MIX" class="mix-container">
            <div class="mix-container-left"></div>
        </div>
    </div>
</template>

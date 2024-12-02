<template>
  <div :class="['app-container', { 'side-menu-close': !isSideMenuOpen, 'single-column': isLoginPage }]">
    <!-- Header Menu -->
    <div v-if="!isLoginPage" class="header-container">
      <HeaderMenu2 @toggleSideMenu="toggleSideMenu" class="head-menu" />
      <SetInterval class="SetInterval" />
      <Breadcrumb_components :breadcrumbs="breadcrumbs" />
    </div>

    <!-- Side Menu -->
    <div v-if="!isLoginPage" :class="['side-menu', { 'd-none': !isSideMenuOpen }]">
      <SideMenu class="" />
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

import HeaderMenu2 from './components/HeaderMenu2.vue';
import SetInterval from './components/SetInterval.vue';
import SideMenu from './components/SideMenu.vue';
import Breadcrumb_components from '@/components/Breadcrumb_components.vue';

const isSideMenuOpen = ref(true);
const store = useStore();
const breadcrumbs = computed(() => store.getters.breadcrumbs);

// ตรวจสอบเส้นทางปัจจุบัน
const route = useRoute();
const isLoginPage = computed(() => route.path === '/login2'); // ตรวจสอบว่าเป็นหน้า login หรือไม่

function toggleSideMenu() {
  isSideMenuOpen.value = !isSideMenuOpen.value;
}
</script>

<style lang="scss">
@import "./styles/main.scss";
@import "~bootstrap/scss/bootstrap";
</style>

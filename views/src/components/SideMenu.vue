<template>
  <nav class="side-menu box-shadow">
    <img :src="require('@/assets/images/logo/bg_project_1@2x.png')" class="logoSide" />
    <div class="mt-4">
      <div v-for="(item, index) in menu" :key="index">
        <router-link v-if="!item.has_submenu" :to="item.url" :class="{ 'active-link': isActive(item.url) }">
          <div class="menu-item">
            <i :class="item.selected_icon"></i>
            <p>{{ item.menu_name }}</p>
          </div>
        </router-link>

        <!-- เมนูหลักที่มีเมนูย่อย -->
        <div v-else :class="['hamburger-menu', { 'active-submenu': hasActiveSubmenu(item) }]" >
          <div class="menu-header" @click="toggleSubmenu(index)">
            <div class="menu-item">
              <i :class="item.selected_icon"></i>
              <p>{{ item.menu_name }}</p>
            </div>
            <i :class="activeIndex === index ? 'pi pi-angle-down' : 'pi pi-angle-left'" class="arrow"></i>
          </div>

          <!-- เมนูย่อย -->
          <div v-if="activeIndex === index" class="submenu-items">
            <router-link v-for="(submenu, subIndex) in item.submenus" :key="subIndex" :to="submenu.url"
              :class="{ 'active-link': isActive(submenu.url) }">
              <i class="pi pi-angle-right"></i>
              <p>{{ submenu.name }}</p>
            </router-link>
          </div>

        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';
import SetUpMenu from '@/components/SetUpMenu.vue'; // นำเข้า Component

// นิยาม Interface ของ Menu และ Submenu
interface Submenu {
  name: string;
  selected_system: string;
  url: string;
}

interface Menu {
  menu_name: string;
  has_submenu: boolean;
  submenus: Submenu[];
  selected_system: string | null;
  selected_icon: string;
  url: string;
}

const menu = ref<Menu[]>([]);
const route = useRoute();
const activeIndex = ref<number | null>(null);

// ฟังก์ชันตรวจสอบ active link
const isActive = (menuUrl: string) => {
  return route.path === menuUrl;
};

// ฟังก์ชันสลับแสดงเมนูย่อย
const toggleSubmenu = (index: number) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};

const hasActiveSubmenu = (menu: Menu) => {
  return menu.submenus.some((submenu) => isActive(submenu.url));
};
// ดึงข้อมูลเมนูจาก API เมื่อ component ถูก mounted
onMounted(async () => {
  try {
    const response = await apiService.getMenu();
    menu.value = response.data;
  } catch (error) {
    console.error('Error fetching menu:', error);
  }
});
</script>

<style scoped lang="scss">
p {
  margin: 0 0 0 5px;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* ทำให้ชิดซ้าย */
  padding: 10px 15px;
}

.menu-item i {
  margin-right: 10px; 
}

.menu-header {
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  padding: 20px 0 20px 0px;
}

.hamburger-menu {
  &.active-submenu {
    border-top: 1px solid #ffffff;
    border-bottom: 1px solid #ffffff;
    font-weight: bold;
  }
}

.hamburger-menu .arrow {
  font-size: 16px;
  padding: 15px 0px 0px 0px;
}

.submenu-items {
  padding-left: 20px;
}

.active-link {

  font-weight: bold;
}

</style>

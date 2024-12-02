<template>
  <div class="tabs-container">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button @click="showComponent('myProject')" :class="{'active': activeComponent === 'myProject'}" 
          class="nav-link" id="nav-myProject-tab" data-bs-toggle="tab" data-bs-target="#nav-myProject" 
          type="button" role="tab" aria-controls="nav-myProject" aria-selected="true">
          My Project
        </button>
        <button @click="showComponent('inTeam')" :class="{'active': activeComponent === 'inTeam'}" 
          class="nav-link" id="nav-inTeam-tab" data-bs-toggle="tab" data-bs-target="#nav-inTeam" 
          type="button" role="tab" aria-controls="nav-inTeam" aria-selected="false">
          In Team
        </button>  
      </div>
    </nav>

    <div class="tab-content">
      <ProCureMent v-if="activeComponent === 'myProject'" :tasks="options" />
      <ProCureTeam v-if="activeComponent === 'inTeam'" :tasks="options" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { apiService } from '../Service/apiService';
import ProCureMent from '../components/ProCureMent.vue';
import ProCureTeam from '../components/ProCureTeam.vue';
import { useStore } from 'vuex';

const options = ref([]); // เก็บข้อมูล tasks ที่ดึงจาก API
const activeComponent = ref('myProject'); // ควบคุมการแสดง component
const store = useStore();

// ฟังก์ชันสำหรับเปลี่ยน component ที่แสดง
const showComponent = (component: string) => {
  activeComponent.value = component;
};

// ดึงข้อมูลจาก API เมื่อ component ถูก mount
onMounted(async () => {
  updateBreadcrumbs();
  try {
    const response = await apiService.getTask(); // ดึงข้อมูลจาก API
    options.value = response.data; // เก็บข้อมูลใน options
  } catch (error) {
    console.error('Error fetching tasks:', error); // แสดงข้อผิดพลาดถ้ามี
  }
});

const updateBreadcrumbs = () => {
  store.dispatch('breadcrumbs/updateBreadcrumbs', [
    { name: 'Home', path: '/', icon: 'pi pi-home' },
    { name: 'Procurement', path: '/Options', icon: 'pi pi-inbox' },
  ]);
};
</script>

<style lang="scss" scoped>
.tabs {
  display: flex;
  border-bottom: 2px solid #ccc;
}

.tabs button {
  background-color: transparent;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tabs button.active {
  border-bottom: 2px solid #007bff;
  color: #007bff;
}

.tabs button:hover {
  color: #0056b3;
}

.tab-content {
  padding: 20px;
  // border: 1px solid #ccc;
}

.nav-link{
  background-color: rgb(233, 233, 233);
  color: rgb(0, 0, 0);
  border-bottom-color: rgb(222, 226, 230); 
}
.nav-link.active {
  background-color: rgb(245, 246, 250);
  color: rgb(0, 0, 0);
  border-bottom-color: rgb(245, 246, 250); 
}
</style>

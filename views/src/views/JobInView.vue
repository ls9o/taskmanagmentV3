<template>
  <div class="tabs-container">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button @click="showComponent('jobIn')" :class="{'active': activeComponent === 'jobIn'}" 
          class="nav-link" id="nav-myProject-tab" data-bs-toggle="tab" data-bs-target="#nav-myProject" 
          type="button" role="tab" aria-controls="nav-myProject" aria-selected="true">
          My Project
        </button>
        <button @click="showComponent('jobInTeam')" :class="{'active': activeComponent === 'jobInTeam'}" 
          class="nav-link" id="nav-inTeam-tab" data-bs-toggle="tab" data-bs-target="#nav-inTeam" 
          type="button" role="tab" aria-controls="nav-inTeam" aria-selected="false">
          In Team
        </button>  
      </div>
    </nav>

    <div class="tab-content">
      <JobIn v-if="activeComponent === 'jobIn'" :tasks="options" />
      <JobInTeam v-if="activeComponent === 'jobInTeam'" :tasks="options" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { apiService } from '../Service/apiService';
import JobIn from '../components/JobIn.vue';
import JobInTeam from '../components/JobInTeam.vue';
import { useStore } from 'vuex';
// สร้าง ref สำหรับเก็บ options จาก API
const options = ref([]); 
const store = useStore();
const activeComponent = ref('jobIn'); // ควบคุมการแสดง component

// ฟังก์ชันสำหรับเปลี่ยน component ที่แสดง
const showComponent = (component: string) => {
  activeComponent.value = component;
};

// ดึงข้อมูลจาก API เมื่อ component ถูก mount
onMounted(async () => {
  updateBreadcrumbs();
  try {
    const response = await apiService.getOptions2();
    options.value = response.data;
  } catch (error) {
    console.error('Error fetching options:', error);
  }
});

const updateBreadcrumbs = () => {
  store.dispatch('breadcrumbs/updateBreadcrumbs', [
    { name: 'Home', path: '/', icon: 'pi pi-home' },
    { name: 'In House', path: '/Options', icon: 'pi pi-inbox' },
  ]);
};
</script>

<style lang="scss" scoped>
.tabs-container{
  height: 100%;
}
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
  height: 100%;
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

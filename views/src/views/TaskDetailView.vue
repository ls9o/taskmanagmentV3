<template>
  <TaskDetail />
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import TaskDetail from '@/components/TaskDetail.vue';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';

// สร้าง ref สำหรับเก็บข้อมูลที่ได้จาก API ทั้งสองเส้นทาง
const task = ref([]);
const process = ref([]);
const Subprocess = ref([]);
const store = useStore();

// ดึงข้อมูลจาก API เมื่อ component ถูก mount
onMounted(async () => {
  updateBreadcrumbs();
  try {
    // เรียก API แรก
    const taskResponse = await apiService.getTask();
    task.value = taskResponse.data;

    // เรียก API ที่สอง
    const processResponse = await apiService.getProcess();
    process.value = processResponse.data;

    const subprocessResponse = await apiService.getSubProcess();
    Subprocess.value = subprocessResponse.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});

const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'Task', path: '/Options', icon: 'pi pi-pencil' },
    ]);
};
</script>

<style>

</style>

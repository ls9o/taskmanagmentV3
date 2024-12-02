<template>
    <AddInfo />
</template>

<script lang="ts" setup>
import { ref, onMounted, compile } from 'vue';
import { apiService } from '../Service/apiService';
import AddInfo from '../components/AddInfo.vue';
import { useStore } from 'vuex';



// สร้าง ref สำหรับเก็บ options จาก API
const options = ref([]);
const store = useStore();

// ดึงข้อมูลจาก API เมื่อ component ถูก mount
onMounted(async () => {
  updateBreadcrumbs();
  // try {
  //   const response = await apiService.getOptions2();
  //   options.value = response.data;
  // } catch (error) {
  //   console.error('Error fetching options:', error);
  // }
});

const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'New Project', path: '/Options', icon: 'pi pi-pencil' },
    ]);
};
</script>

<style lang="scss" scoped>
div{
  height: 100%;

}
</style>

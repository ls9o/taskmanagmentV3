<template>
  <div class="container-fluid">
    <h1>My Project</h1>
    <Paginator :first="(currentPage - 1) * itemsPerPage" :rows="itemsPerPage" :totalRecords="Tasks.length"
            @page="onPageChangeDataInfo"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords}" class="mb-3"/>
    <div class="row">
      <div class="col-12">
        <div v-if="Tasks.length > 0">
          <div class="custom-border"></div>
          <div class="card mb-3" v-for="(item, index) in paginatedTasks" :key="index">
            <div v-if="item.infotype === 'จัดซื้อจัดจ้าง' ">
              <div class="card-body d-flex justify-content-between">
                <span class="col-3">Name Project: {{ truncate(item.infoname, 20) }}</span>
                <span>manager: {{ item.manager }}</span>
                <span>ระยะเวลางาน : {{ item.statusprogress }}%</span>
                <span>ความคืบหน้า Process : {{ item.progressPercentage }}%</span>
                <div>
                  <i class="fa-solid bi bi-calendar icon-pad"></i>
                  <span>{{ functions.formatDateToThai (item.infostart,3) }}</span>
                  <span> — </span>
                  <span>{{ functions.formatDateToThai (item.infoend,3) }}</span>
                </div>
                <button @click="moreinfo(item.id)" type="button" class="btn btn-outline-primary">
                  <i class="fa-solid fa-magnifying-glass"></i>
                </button>
              </div>
            </div>
          </div>
          
        </div>
        <div v-else>
          <h1 class="text-Result">No Result</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import Paginator from 'primevue/paginator';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';
import * as functions  from '../function/function.inc'

const store = useStore();
const userStorage = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());
const Tasks = ref<any[]>([]);
const loading = ref(true);
const router = useRouter();
const itemsPerPage = ref(4);
const currentPage = ref(1);

const getUserFromLocalStorage = () => {
    const user = localStorage.getItem("user");
    if (user) {
        try {
            return JSON.parse(user);
        } catch (error) {
            console.error("Error parsing user data from localStorage:", error);
            return null;
        }
    }
    return null;
};

const truncate = (text: string, length: number) => {
  return text.length > length ? text.substring(0, length) + '...' : text;
};

const moreinfo = (id: number) => {
  router.push(`/TaskDetail/${id}`);
};

const fetchTask = async () => {
  try {
    const response = await apiService.getTask(userStorage.value.userID); // ส่ง userID แทน usernamecode
    Tasks.value = response.data.filter(item => item.infotype === 'จัดซื้อจัดจ้าง');
  } catch (error) {
    console.error('Error fetching Tasks:', error);
  }
};

// คำนวณข้อมูลที่จะถูกแสดงตามหน้า
const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return Tasks.value.slice(start, start + itemsPerPage.value);
});

// ฟังก์ชันเปลี่ยนหน้า
const onPageChangeDataInfo = (event: { page: number; rows: number }) => {
  currentPage.value = event.page + 1; // Paginator เริ่มที่หน้า 0 ต้องบวก 1
  itemsPerPage.value = event.rows;
};

onMounted(() => {
  fetchTask();
});
</script>

<style scoped>
@import './Sass/Homepage.scss';
</style>

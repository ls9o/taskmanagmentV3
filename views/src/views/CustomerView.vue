<template>
  <div class="page-layout" :style="{ gridTemplateColumns }">
    <Search_component v-if="!loading" :options="options" :isCollapsed="isCollapsed" @search="handleSearch"
      @toggleCollapse="toggleCollapse" />

    <div v-if="loading" class="loading-indicator">
      กำลังโหลดข้อมูล...
    </div>

    <div v-if="!loading && showCustomerInfo">
      <div v-if="pathname == '/Options'">
        <SubMenu2 @navigate="handleNavigation" :isCollapsed="isCollapsed" class="submenu-background" />
      </div>
      <div :style="{ marginTop: pathname == '/Options' ? '4rem' : '0' }" class="customer-info-container">
        <CustomerInformation :headers="currentHeaders" :dataApi="dataApi" :showDeleteIcon="showDeleteIcon" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import Search_component from '../components/Search_component.vue';
import CustomerInformation from '../components/CustomerInformation.vue';
import SubMenu2 from '@/components/SubMenu2.vue';
import { apiService } from '../Service/apiService';
import { contains } from 'bootstrap-vue-3/dist/utils';

const options = ref<Array<{
  head?: string;
  label: string;
  show?: string;
  options: { value: string; text: string }[];
}>>([]);

const loading = ref(true);
const pathname = ref(window.location.pathname);
const searchParams = ref<any>({});
const showCustomerInfo = ref(false);
const store = useStore();
const route = useRoute();
const router = useRouter();
const currentHeaders = ref<any[]>([]);
const isCollapsed = ref(false);
const showDeleteIcon = ref(false);
const dataApi = ref<any[]>([]);

const fetchOptions = async () => {
  loading.value = true; // เริ่มการโหลด
  try {
    const response = await apiService.getOptions();
    options.value = response.data.filter((a: any) => a.show === pathname.value) || [];
    
    // ตรวจสอบการตั้งค่า head ให้ถูกต้อง
    if (pathname.value === "/Customer") {
      options.value.push({ head: "ค้นหาข้อมูลลูกค้า", label: "ค้นหา", options: [] }); // ใส่ label และ options ตามที่ต้องการ
    }
    if (pathname.value === "/Options") {
      options.value.push({ head: "รหัสเข้าใช้งาน (รหัส Outlook)", label: "ตัวเลือก", options: [] }); // ใส่ label และ options ตามที่ต้องการ
    }
  } catch (error) {
    console.error('Error fetching options:', error);
  } finally {
    loading.value = false;
  }
};


const updateBreadcrumbs = (path: string) => {
  const breadcrumbs = [
    { name: 'Home', path: '/', icon: 'pi pi-home' },
    { name: 'ข้อมูลลูกค้า', path: '/Customer', icon: 'pi pi-users' },
  ];
  store.dispatch('breadcrumbs/updateBreadcrumbs', breadcrumbs);
};

const setHeaders = (headers: any[]) => {
  currentHeaders.value = headers;
};

const handlePathUpdate = () => {
  showCustomerInfo.value = false;
  showDeleteIcon.value = false;

  const path = route.path;
  pathname.value = path;

  if (path === '/Customer') {
    fetchOptions();
    updateBreadcrumbs(path);
    setHeaders([
      { key: "id13", text: "เลขบัตรประชาชน" },
      { key: "RegistrationNumber", text: "เลขทะเบียน" },
      { key: "FirstName", text: "ชื่อ" },
      { key: "LastName", text: "นามสกุล" },
      { key: "PhoneNumber", text: "เบอร์โทรศัพท์ มือถือ" },
      { key: "RegistrationStatus", text: "สถานะ การสมัคร" },
      { key: "CustomerStatus", text: "สถานะลูกค้า" },
      { key: "DateModified", text: "บันทึกเวลา การแก้ไข" },
    ]);
  } else if (path === '/Options') {
    fetchOptions();
    updateBreadcrumbs(path);
    setHeaders([
      { key: "username", text: "สำนักงาน/สาขา" },
      { key: "usernamecode", text: "รหัสการใช้งาน" },
      { key: "password", text: "ชื่อ" },
      { key: "BranchDepartment", text: "นามสกุล" },
      { key: "jobposition", text: "ทีมการทำงาน" },
      { key: "Branch", text: "สถานะพนักงาน" },
      { key: "level", text: "บันทึกเวลา การแก้ไข" },
      { key: "level", text: "บันทึกเวลา การแก้ไข" },
    ]);
  }
};

const handleNavigation = (path: string) => {
  if (path === '/back') {
    router.push('/Options');
  } else if (path === '/add') {
    router.push({ path: `/employee/${0}`, query: { status: "add" } });
  } else if (path === '/delete') {
    showDeleteIcon.value = !showDeleteIcon.value;
  }
};

const handleSearch = (params: any) => {
  searchParams.value = params;
  showCustomerInfo.value = true;
};

const toggleCollapse = (collapsed: boolean) => {
  isCollapsed.value = collapsed;
};

const gridTemplateColumns = computed(() => {
  return isCollapsed.value ? '0fr 1fr' : '300px 1fr';
});

const loadData = async () => {
  loading.value = true; // เริ่มการโหลด
  const path = route.path;
  try {
    const response = path === "/Customer" ? await apiService.getUser() : await apiService.getUser();
    if (response) {
      dataApi.value = response.data;
    }
  } catch (error) {
    console.error("Error fetching items:", error);
  } finally {
    loading.value = false; // โหลดเสร็จสิ้น
  }
};

onMounted(() => {
  handlePathUpdate();
  loadData();
});

watch(() => route.path, () => {
  handlePathUpdate();
  loadData();
});
</script>

<style lang="scss" scoped></style>

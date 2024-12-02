<template>
  <header class="header-menu-container d-flex justify-content-between align-items-center ">
    <!-- ปุ่มขีดขีดทางด้านซ้ายและชื่อ -->
    <div class="d-flex align-items-center p-3">
      <button class="btn btn-outline-secondary me-2" @click="toggleSidebar">
        <i class="fa fa-bars"></i>
      </button>
      <div class="d-flex flex-column">
        <p class="mb-0">ธนาคารพัฒนาวิสาหกิจขนาดกลางและขนาดย่อมแห่งประเทศไทย</p>
        <p class="mb-0">Small and Medium Enterprise Development Bank of Thailand</p>
      </div>
    </div>

    <div class="menu d-flex align-items-center ms-auto">
      <!-- รูปโปรไฟล์และข้อมูลด้านขวาสุด -->
      <div class="d-flex align-items-center profile-info ms-3 p-3">
        <img src="https://via.placeholder.com/40" alt="โปรไฟล์" class="profile-image rounded-circle" width="60"
          height="60" />
        <div class="ms-3">
          <h5 class="profile-name mb-0">ชื่อ: {{ user.username }}</h5>
          <h5 class="profile-position mb-0">{{ user.EmployeeTerm }}</h5>
          <h5 class="profile-position mb-0">{{ user.Branch }}</h5>
        </div>
        <button class="btn btn-outline-secondary ms-5" @click="logout">
          <i class="pi pi-power-off"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { computed, defineEmits } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const emit = defineEmits(['toggleSideMenu']);
const store = useStore();
const router = useRouter();


function getUserFromLocalStorage() {
  const user = localStorage.getItem("user");
  if (user) {
    try {
      return JSON.parse(user);
    } catch (e) {
      console.error("Error parsing user data from localStorage:", e);
      return null;
    }
  }
  return null;
}

const user = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());

function toggleSidebar() {
  emit('toggleSideMenu');
}

function logout() {
  store.dispatch('logout');
  router.push('/login2');
}
</script>

<style lang="scss" scoped>
</style>

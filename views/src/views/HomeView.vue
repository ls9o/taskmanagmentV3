<!-- src/views/Home.vue -->
<template>
  <div class="container text-center mt-5">
    <h1 class="mb-4">Task Management</h1>
    <h3 class=" p-3 mb-2 ">Created by</h3>
    <div class="row justify-content-center">
      <div class="col-6">
        <div class="">
          <p class="mb-0">6430200086 นายเจษฎากร ยาวิเริง</p>
        </div>
        <div class="">&</div>
        <div class="">
          <p class="mb-0">6430200299 นายธัญกร อีซา</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
const store = useStore();
onMounted(() => {
  store.dispatch("breadcrumbs/updateBreadcrumbs", [
    { name: "Home", path: "/", icon: "pi pi-home" },
  ]);
});
</script>

<style scoped>
/* ปรับสไตล์เพิ่มเติมถ้าต้องการ */
.border {
  border-radius: 8px; /* เพิ่มความโค้งมน */
}
</style>
<template>
  <div class="container-xl">
    <form @submit.prevent="confirmEdit">
      <h1 class="text-center mb-4">แก้ไขข้อมูล</h1>
      <div class="row mb-3">
        <div class="col">
          <label class="form-label">รายละเอียด:</label>
          <textarea class="form-control bg-secondary-custom" rows="5" v-model="editData.editDetail"></textarea>
        </div>
      </div>
      <div class="row mb-3">
        <div v-if="isDate" class="col-6">
          <label class="form-label">วันที่เริ่ม:</label>
          <input class="form-control bg-secondary-custom" type="date" v-model="editData.editStart">
        </div>
        <div class="col-6" v-if="!isDate">
          <label class="form-label">จำนวนวันทำงาน:</label>
          <input class="form-control bg-secondary-custom" type="number" v-model="editData.workingDays">
        </div>
        <div class="col-6">
          <label class="form-label">วันที่จบ:</label>
          <input class="form-control bg-secondary-custom" type="date" v-model="editData.editEnd">
        </div>
      </div>
      <div class="row">
        <div class="col">
          <button class="btn btn-danger button-right" type="button" @click="cancelEdit">ยกเลิก</button>
          <button class="btn btn-success button-right" type="submit">บันทึก</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// Initialize reactive data for editing
const editData = reactive({
  editDetail: '',
  editStart: '',
  editEnd: '',
  workingDays: ''
});

const isDate = ref(true);

// Use Vue Router for navigation
const route = useRoute();
const router = useRouter();

// Load the task details from Local Storage when the component is mounted
onMounted(() => {
  const taskDetail = JSON.parse(localStorage.getItem('infoData') || '[]').find((task: any) => task.infoname === route.query.infoname);
  if (taskDetail) {
    if (route.query.editType === 'info') {
      const subTask = taskDetail.subInputBoxesinfo.find((sub: any) => sub.infodetails === route.query.editDetail);
      if (subTask) {
        editData.editDetail = subTask.infodetails;
        editData.editStart = subTask.infostart;
        editData.editEnd = subTask.infoend;
        isDate.value = true;
      }
    } else if (route.query.editType === 'process') {
      taskDetail.processes.forEach((process: any) => {
        const subProcess = process.subProcesses.find((sub: any) => sub.procesdetails === route.query.editDetail);
        if (subProcess) {
          editData.editDetail = subProcess.procesdetails;
          editData.workingDays = subProcess.processtart;
          editData.editEnd = subProcess.procesend;
          isDate.value = false;
        }
      });
    }
  }
});

// Confirm the edit and update the Local Storage
const confirmEdit = () => {
  const allData = JSON.parse(localStorage.getItem('infoData') || '[]');
  const taskDetail = allData.find((task: any) => task.infoname === route.query.infoname);
  
  if (taskDetail) {
    if (route.query.editType === 'info') {
      const subTaskIndex = taskDetail.subInputBoxesinfo.findIndex((sub: any) => sub.infodetails === route.query.editDetail);
      if (subTaskIndex !== -1) {
        taskDetail.subInputBoxesinfo[subTaskIndex] = {
          infodetails: editData.editDetail,
          infostart: editData.editStart,
          infoend: editData.editEnd,
        };
      }
    } else if (route.query.editType === 'process') {
      taskDetail.processes.forEach((process: any) => {
        const subProcessIndex = process.subProcesses.findIndex((sub: any) => sub.procesdetails === route.query.editDetail);
        if (subProcessIndex !== -1) {
          process.subProcesses[subProcessIndex] = {
            procesdetails: editData.editDetail,
            processtart: editData.workingDays,
            procesend: editData.editEnd,
          };
        }
      });
    }
    
    localStorage.setItem('infoData', JSON.stringify(allData));
    alert('บันทึกการแก้ไขสำเร็จ');
    router.push({ name: 'TaskDetail', query: { infoname: route.query.infoname } });
  }
};

// Cancel the edit and return to the TaskDetail page
const cancelEdit = () => {
  router.push({ name: 'TaskDetail', query: { infoname: route.query.infoname } });
};
</script>

<style scoped>
.container-xl {
  max-width: 50rem;
  margin: 0 auto;
}

button {
  margin-top: 0.2rem;
}

.btn {
  margin: 5px;
}
</style>

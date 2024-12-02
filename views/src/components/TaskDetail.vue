<template>
  <div class="container-xl">
    <form @submit.prevent="">
      <div class="row" v-if="isLoading">
        <p class="text-center">กำลังโหลดข้อมูล...</p>
      </div>
      <div class="row" v-if="taskDetail && !isLoading">
        <div class="card mb-3">
          <div class="container my-4">
            <h1 class="text-center">รายละเอียดงาน</h1>

            <div class="row mb-3">
              <div class="col-12">
                <label><strong>ชื่องาน:</strong></label>
                <input type="text" class="form-control" :value="taskDetail.infoname" readonly>
              </div>
            </div>

            <div class="row mb-3">
              <div class="col-12">
                <label><strong>รายละเอียด:</strong></label>
                <textarea v-model="taskDetail.infodetails" class="form-control textareareadonly"></textarea>
              </div>
            </div>


            <div class="row mb-3">
              <div class="col-3">
                <label><strong>วันที่เริ่ม:</strong></label>
                <input type="text" class="form-control" :value="functions.formatDateToThai(taskDetail.infostart, 3)"
                  readonly>
              </div>
              <div class="col-3">
                <label><strong>วันที่จบ:</strong></label>
                <input type="text" class="form-control" :value="functions.formatDateToThai(taskDetail.infoend, 3)"
                  readonly>
              </div>
              <div class="col-2">
                <label><strong>จำนวนวันทั้งหมด:</strong></label>
                <input type="text" class="form-control" :value="taskDetail.dayDiff" readonly>
              </div>
              <div class="col-2">
                <label><strong>ระยะเวลางาน:</strong></label>
                <input type="text" class="form-control" :value="status + ' %'" readonly>
              </div>
              <div class="col-2">
                <label><strong>ความคืบหน้า Process:</strong></label>
                <input type="text" class="form-control" :value="progressPercentage + ' %'" readonly>
              </div>
            </div>

            <div class="row mb-2">
              <div class="col-3">
                <label><strong>ประเภทงาน:</strong></label>
                <input type="text" class="form-control" :value="taskDetail.infotype" readonly>
              </div>
              <div class="col-2">
                <label><strong>Project Manager:</strong></label>
                <input type="text" class="form-control"
                  :value="taskDetail.manager && taskDetail.manager !== 'None None' ? taskDetail.manager : ''" readonly>
              </div>
              <div class="col-7">
                <label><strong>ทีม:</strong></label>
                <input type="text" class="form-control" :value="formatTeamNames(taskDetail.userandteam)" readonly>
              </div>
            </div>
          </div>

          <div v-for="(Subtask, infoIndex) in SubtaskDetail" :key="infoIndex" class="card mb-3">
            <div class="card-body">
              <div>
                <label class="form-label">รายละเอียด:</label>
                <input type="text" class="form-control bg-secondary-custom" v-model="Subtask.subinfodetails" readonly />
              </div>
              <div class="row">
                <div class="col-6 mb-3">
                  <label class="form-label">วันที่เริ่ม:</label>
                  <input type="date" class="form-control bg-secondary-custom" v-model="Subtask.subinfostart" readonly />
                </div>
                <div class="col-6 mb-3">
                  <label class="form-label">วันที่จบ:</label>
                  <input type="date" class="form-control bg-secondary-custom" v-model="Subtask.subinfoend" readonly />
                </div>
              </div>
              <div>
                <button @click="edit('info', null, infoIndex)" class="btn btn-primary button-right">แก้ไข</button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!hasSubtaskEntries && !isAddingInfo">
          <button @click="startAddingInfo" class="btn btn-secondary mb-3">ยืนยันแผน</button>
        </div>

        <div v-if="isAddingInfo && !hasSubtaskEntries">
          <div class="card mb-3">
            <div class="card-body mb-2">
              <label class="form-label">รายละเอียด: <span class="text-danger">*</span></label>
              <textarea class="form-control bg-secondary-custom" rows="2"
                v-model="newInfoDetails.subinfodetails"></textarea>
            </div>
            <div class="row">
              <div class="card-body col-2 mb-3 ms-2">
                <label class="form-label">วันที่เริ่ม: <span class="text-danger">*</span></label>
                <input class="form-control bg-secondary-custom" type="date" v-model="newInfoDetails.subinfostart">
              </div>
              <div class="card-body col-2 mb-3">
                <label class="form-label">วันที่จบ: <span class="text-danger">*</span></label>
                <input class="form-control bg-secondary-custom" type="date" v-model="newInfoDetails.subinfoend">
              </div>
              <div class="col-6"></div>
            </div>

            <div class="d-flex justify-content-end pe-3">
              <button class="btn btn-success mb-2 me-2" type="button" @click="confirm('info')">บันทึก</button>
              <button class="btn btn-danger mb-2" type="button" @click="cancel('info')">ยกเลิก</button>
            </div>
          </div>
        </div>

        <div v-if="editSubtask && selectedSubtask.index === 0" class="card mb-3">
          <div class="card-body mb-3">
            <label class="form-label">รายละเอียด:</label>
            <textarea class="form-control bg-secondary-custom" rows="3"
              v-model="newInfoDetails.subinfodetails"></textarea>
          </div>
          <div class="row">
            <div class="card-body col-2 mb-3 ms-2">
              <label class="form-label">วันที่เริ่ม:</label>
              <input class="form-control bg-secondary-custom" type="date" v-model="newInfoDetails.subinfostart">
            </div>
            <div class="card-body col-2 mb-3">
              <label class="form-label">วันที่จบ:</label>
              <input class="form-control bg-secondary-custom" type="date" v-model="newInfoDetails.subinfoend">
            </div>
            <div class="col-6"></div>
          </div>

          <div class="d-flex justify-content-end pe-3">
            <button class="btn btn-success mb-2 me-2" type="button" @click="confirm('info')">บันทึก</button>
            <button class="btn btn-danger mb-2" type="button" @click="cancel('info')">ยกเลิก</button>
          </div>
        </div>

        <div v-for="(process, processIndex) in Process" :key="processIndex"
          :class="{ 'bg-custom': process.processisvisible }" class="card mb-3">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <label class="form-label">ชื่อ Process:</label>
                <input type="text" class="form-control bg-secondary-custom" v-model="process.procesname" readonly />
                <label class="form-label">รายละเอียด:</label>
                <input type="text" class="form-control bg-secondary-custom" v-model="process.procesdetails" readonly />
                <div class="row">
                  <div class="col-6">
                    <label class="form-label">จำนวนวันทำงาน:</label>
                    <input type="number" class="form-control bg-secondary-custom" v-model="process.processtart"
                      readonly />
                  </div>
                  <div class="col-6">
                    <label class="form-label">วันกำหนดส่ง:</label>
                    <input type="text" class="form-control bg-secondary-custom"
                      :value="functions.formatDateToThai(process.procesend, 3)" readonly />
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div v-for="(subprocess, subprocessIndex) in subProcess" :key="subprocessIndex">
                  <div v-if="process.id === subprocess.idprocess" :class="{ 'bg-custom': process.processisvisible }"
                    class="card mb-3">
                    <div class="card-body">
                      <label class="form-label">รายละเอียดย่อย:</label>
                      <input type="text" class="form-control bg-secondary-custom" v-model="subprocess.subprocesdetails"
                        readonly />
                      <div class="row">
                        <div class="col-6">
                          <label class="form-label ">จำนวนวันทำงาน:</label>
                          <input type="number" class="form-control bg-secondary-custom"
                            v-model="subprocess.subprocesstart" readonly />
                        </div>
                        <div class="col-6">
                          <label class="form-label">กำหนดการส่ง: 1</label>
                          <input type="text" class="form-control bg-secondary-custom"
                            :value="functions.formatDateToThai(subprocess.subprocesend, 3)" readonly />
                        </div>
                      </div>
                      <div v-if="!process.processisvisible">
                        <button @click="edit('subprocess', subprocess, processIndex)"
                          class="btn btn-primary mt-3 button-right">แก้ไข</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="!hasMatchingSubprocess(process.id) && addsubprocessShow && !process.processisvisible">
                <button @click="edit('addsubprocess', processIndex, processIndex)"
                  class="btn btn-secondary mb-4 button-right">ยืนยันขั้นตอน</button>
              </div>
              <div v-if="editSubProcess && selectedSubProcess.index === processIndex" class="card mt-3 mb-3">
                <div class="card-body mb-3">
                  <label class="form-label">รายละเอียด: <span class="text-danger">*</span></label>
                  <textarea class="form-control bg-secondary-custom" rows="3"
                    v-model="newSubProcessDetails.procesdetails"></textarea>
                </div>
                <div class="row">
                  <div class="card-body col-2 mb-3 ms-2">
                    <label class="form-label">จำนวนวันทำงาน: <span class="text-danger">*</span></label>
                    <input class="form-control bg-secondary-custom" type="number"
                      v-model="newSubProcessDetails.processtart">
                  </div>
                  <div class="card-body col-2 mb-3">
                    <label class="form-label">กำหนดการส่ง: <span class="text-danger">*</span></label>
                    <input class="form-control bg-secondary-custom" type="date"
                      v-model="newSubProcessDetails.procesend">
                  </div>
                  <div class="col-6"></div>
                </div>
                <div class="d-flex justify-content-end pe-3">
                  <button class="btn btn-success mb-2 me-2" type="button" @click="confirm('subprocess')">บันทึก</button>
                  <button class="btn btn-danger mb-2" type="button" @click="cancel('subprocess')">ยกเลิก</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-10"></div>
          <div class="col-2">
            <button class="btn btn-primary button-right mb-3" @click="fixinfo(taskDetail)">แก้ไข</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from "vue-router";
import { apiService } from '../Service/apiService';
import { AxiosError } from 'axios';
import * as functions from '../function/function.inc'

const router = useRouter();
const route = useRoute();
const taskDetail = ref<any>(null);
const SubtaskDetail = ref<any>(null);
const editSubtask = ref(false);
const selectedSubtask = ref<any>(null);
const addsubtaskShow = ref(true);
const Process = ref<any>(null);
const subProcess = ref<any>(null);
const isAddingInfo = ref(false);
const AddSubProcess = ref(false);
const editSubProcess = ref(false);
const addsubprocessShow = ref(true);
const selectedSubProcess = ref<any>(null);
const isLoading = ref(true);
const date = ref(new Date());

const newInfoDetails = ref({
  subinfodetails: '',
  subinfostart: '',
  subinfoend: ''
});

const newSubProcessDetails = ref({
  procesdetails: '',
  processtart: '',
  procesend: ''
});

onMounted(async () => {
  isLoading.value = true; // เริ่มโหลดข้อมูล
  await loadTaskDetail(); // รอให้โหลด Task Detail เสร็จ
  await loadSubTaskDetail(); // รอให้โหลด Sub Task Detail เสร็จ
  await loadProcessDetail(); // รอให้โหลด Process Detail เสร็จ
  await loadSubProcessDetail(); // รอให้โหลด Sub Process Detail เสร็จ
  isLoading.value = false; // เสร็จสิ้นการโหลดข้อมูล
});

const hasSubtaskEntries = computed(() => {
  return SubtaskDetail.value && SubtaskDetail.value.length > 0;
});
const progressPercentage = computed(() => {
  if (!taskDetail.value || !Process.value || Process.value.length === 0) {
    return 0;
  }
  return functions.progressPercentage(Process.value, subProcess.value);
});

const formatTeamNames = (userAndTeam: string[]) => {
  return userAndTeam.join(', '); // แยกชื่อด้วยคอมมา
};

const status = computed(() => {
  return functions.CheckProgressPercentage(taskDetail.value)
});


const updateTask = async () => {
  if (taskDetail.value) {
    const taskId = taskDetail.value.id;

    const statusProgressValue = typeof status.value === 'number' ? status.value : Number(status.value);

    // ใช้ ?? เพื่อเช็คเฉพาะค่าที่เป็น null หรือ undefined
    const taskData = {
      statusprogress: statusProgressValue,
      progressPercentage: progressPercentage.value ?? 0, // ใช้ ?? แทน || เพื่อป้องกันการใช้ค่าที่ไม่ควรเป็น 0
    };

    console.log('Task data:', taskData);

    try {
      await apiService.updatePercentageTask(taskId, taskData); // ตรวจสอบชื่อฟังก์ชันให้ตรงกัน
      console.log('Task updated successfully');
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Error updating task:', axiosError.response?.data || axiosError.message);
    }
  }
};

watch([status, progressPercentage], () => {
  if (status.value !== null && progressPercentage.value !== null) {
    updateTask();
  }
});

const loadTaskDetail = async () => {
  const id = Number(route.params.id);
  if (!isNaN(id)) {
    try {
      const response = await apiService.getTask();
      const assets = response.data;
      taskDetail.value = assets.find((a: any) => a.id === id) || null;
    } catch (error) {
      console.error('Error fetching task details:', error);
    }
  }
};

const loadSubTaskDetail = async () => {
  const id = Number(route.params.id);
  if (!isNaN(id)) {
    try {
      const response = await apiService.getSubtask();
      SubtaskDetail.value = response.data.filter((a: any) => a.idtask === id);
    } catch (error) {
      console.error('Error fetching subtask details:', error);
    }
  }
};


const loadProcessDetail = async () => {
  try {
    const response = await apiService.getProcess();
    const assets = response.data;
    // ตรวจสอบว่ามีค่า taskDetail.value ก่อนเข้าถึง id
    if (taskDetail.value && taskDetail.value.id) {
      Process.value = assets.filter((process: any) => process.idtask === taskDetail.value.id);
    } else {
      console.error("taskDetail.value หรือ taskDetail.value.id ไม่ถูกต้อง");
    }
  } catch (error) {
    console.error('Error fetching process details:', error);
  }
};


const loadSubProcessDetail = async () => {
  try {
    const response = await apiService.getSubProcess();
    const assets = response.data;

    if (Process.value && Process.value.length > 0) {
      let matchingSubProcesses: any = [];
      Process.value.forEach((process: any) => {
        const filteredSubProcesses = assets.filter((subProcess: any) => subProcess.idprocess === process.id);
        matchingSubProcesses = matchingSubProcesses.concat(filteredSubProcesses);
      });
      subProcess.value = matchingSubProcesses;
    }
  } catch (error) {
    console.error('Error fetching process details:', error);
  }
};

const startAddingInfo = () => {
  isAddingInfo.value = true;
};

const hasMatchingSubprocess = (processId: number) => {
  return subProcess.value && subProcess.value.some((subprocess: any) => subprocess.idprocess === processId);
};
const edit = (type: string, subprocess: any, processIndex: number) => {
  if (type === 'subprocess') {
    selectedSubProcess.value = { index: processIndex, id: subprocess.id };
    newSubProcessDetails.value = {
      procesdetails: subprocess.subprocesdetails,
      processtart: subprocess.subprocesstart,
      procesend: subprocess.subprocesend
    };
    editSubProcess.value = true;
  } else if (type === 'addsubprocess') {
    selectedSubProcess.value = { index: processIndex, id: null };
    newSubProcessDetails.value = {
      procesdetails: '',
      processtart: '',
      procesend: ''
    };
    addsubprocessShow.value = false;
    editSubProcess.value = true;
  } else if (type === 'info') {
    selectedSubtask.value = { index: processIndex, id: null };
    newInfoDetails.value = {
      subinfodetails: SubtaskDetail.value[0].subinfodetails,  // ตรวจสอบว่ามีค่าหรือไม่
      subinfostart: SubtaskDetail.value[0].subinfostart || '',
      subinfoend: SubtaskDetail.value[0].subinfoend || ''
    };
    editSubtask.value = true;  // เปิดโหมดแก้ไข
  }
};

const confirm = async (str: string) => {
  if (str === 'info') {
    if (taskDetail.value && !taskDetail.value.subInputBoxesinfo) {
      taskDetail.value.subInputBoxesinfo = [];
    }

    // สร้างอ็อบเจ็กต์ใหม่จากข้อมูล info
    const newInfo = {
      idtask: taskDetail.value.id,
      ...newInfoDetails.value
    };

    try {
      // ส่งข้อมูลไปยัง API
      if (SubtaskDetail.value[0] && SubtaskDetail.value[0].id) {
        // กรณีที่แก้ไข subprocess ที่มีอยู่
        await apiService.updateSubtask(SubtaskDetail.value[0].id, newInfo);
        alert('แก้ไขข้อมูล subtask สำเร็จ');
      } else {
        // กรณีที่เพิ่ม subprocess ใหม่
        const response = await apiService.postSubtask(newInfo);
        taskDetail.value.subInputBoxesinfo.push(response.data);
      } // เพิ่มข้อมูลที่ได้รับกลับเข้ามาในอาเรย์

      selectedSubtask.value = null;
      editSubtask.value = false;
      addsubtaskShow.value = true;
      // ปิดการเพิ่มข้อมูล
      isAddingInfo.value = false;
    } catch (error) {
      console.error('Error saving info:', error);
      alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล info');
    }
  }

  if (str == 'subprocess') {
    try {
      const newSubProcess = {
        idprocess: Process.value[selectedSubProcess.value.index].id,
        subprocesdetails: newSubProcessDetails.value.procesdetails,
        subprocesstart: newSubProcessDetails.value.processtart,
        subprocesend: newSubProcessDetails.value.procesend
      };

      if (selectedSubProcess.value.id) {
        // กรณีที่แก้ไข subprocess ที่มีอยู่
        await apiService.updateSubProcess(selectedSubProcess.value.id, newSubProcess);
        alert('แก้ไขข้อมูล subprocess สำเร็จ');
      } else {
        // กรณีที่เพิ่ม subprocess ใหม่
        const response = await apiService.postSubProcess(newSubProcess);
        subProcess.value.push(response.data);
      }

      selectedSubProcess.value = null;
      editSubProcess.value = false;
      addsubprocessShow.value = true;
    } catch (error) {
      console.error('Error creating/updating subprocess:', error);
      alert('เกิดข้อผิดพลาดในการบันทึก subprocess');
    }
  }
}

const cancel = (type: string) => {
  if (type === 'info') {
    isAddingInfo.value = false;
  } else if (type === 'subprocess') {
    addsubprocessShow.value = true;
    editSubProcess.value = false;
    selectedSubProcess.value = null;

  }
};

function fixinfo(task: any) {
  const id = Number(route.params.id);
  router.push({ path: `/Addinfo/${id}` });
}
</script>

<style scoped>
.button-right {
  float: right;
}

.bg-custom {
  background-color: #c7c7c7;
}

input[readonly] {
  background-color: #f2f2f2;
  /* เปลี่ยนเป็นสีที่ต้องการ เช่น สีเทาอ่อน */
  color: #495057;
  /* เปลี่ยนเป็นสีข้อความที่ต้องการ */
  border: 1px solid #ced4da;
  /* สีของกรอบ input */
}

.textareareadonly {
  background-color: #f2f2f2;
  /* สีพื้นหลังที่คุณต้องการ */
  color: #495057;
  /* เปลี่ยนสีข้อความที่ต้องการ (ถ้าต้องการ) */
  border: 1px solid #ced4da;
  /* สีกรอบ textarea */
  resize: none;
  /* ป้องกันไม่ให้เปลี่ยนขนาด */
}
</style>
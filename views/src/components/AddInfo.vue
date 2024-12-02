  <template>
    <!-- <div class="p-grid p-2">
      <div class="card"> -->
    <div class="container-xl ">
      <h1 class="text-center mb-4">{{ isEditMode ? 'Edit Task' : 'Create Task' }}</h1>

      <div v-if="loading">
        <p>กำลังโหลด...</p>
      </div>

      <form v-if="!loading" @submit.prevent="confirminfo">
        <div>
          <div>
            <label class="form-label">ชื่องาน: <span class="text-danger">*</span> </label>
            <input class="form-control p-3 mb-5" type="text" v-model="Datainfo.infoname" />
          </div>
          <div>
            <label class="form-label">รายละเอียด: <span class="text-danger">*</span></label>
            <textarea class="form-control p-3 mb-5" rows="1" v-model="Datainfo.infodetails"></textarea>
          </div>
          <div class="row">
            <div class="col-md-2 mb-3">
              <label class="form-label">วันที่เริ่ม: <span class="text-danger">*</span></label>
              <input class="form-control " type="date" v-model="Datainfo.infostart" />
            </div>
            <div class="col-2 mb-3">
              <label class="form-label">วันที่จบ: <span class="text-danger">*</span></label>
              <input class="form-control " type="date" v-model="Datainfo.infoend" />
            </div>
          </div>
          <div class="col-2 mb-3">
            <label class="form-label">จำนวนวัน:</label>
            <input class="form-control " type="text" :value="daysBetween" readonly />
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">ประเภทงาน: <span class="text-danger">*</span></label><br />
              <div class="form-check form-check-inline" v-for="type in taskTypes" :key="type">
                <input class="form-check-input" type="radio" :value="type" v-model="Datainfo.infotype" />
                <label class="form-check-label">{{ type }}</label>
              </div>
            </div>

            <div class="col-md-2 mb-4">
              <label class="form-label">Project Manager:</label>
              <select class="form-control" v-model="Datainfo.manager">
                <option v-for="manager in users" :key="manager" :value="manager.id">{{ manager.username }}</option>
              </select>
            </div>

            <div class="col-md-2 mb-5">
              <label class="form-label">team:</label>
              <select class="form-control" v-model="Datainfo.team">
                <option v-for="team in teams" :key="team.id" :value="team.user">{{ team.teamname }}</option>
              </select>
            </div>


            <div class="col-md-2 mb-5">
              <label class="form-label">user in team:</label>
              <MultiSelect v-model="selectedUsers" :options="users" optionLabel="username" optionValue="id"
                :maxSelectedLabels="3" @change="onChange" filter placeholder="Select User" class="w-full md:w-80" />
            </div>
          </div>

          <div v-for="(subProcess, index) in Process" :key="index" class="card mb-3">
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">ชื่อ process: <span class="text-danger">*</span></label>
                <input class="form-control " type="text" v-model="subProcess.procesname" />
              </div>
              <div class="mb-3">
                <label class="form-label">รายละเอียด: <span class="text-danger">*</span></label>
                <textarea class="form-control " rows="1" v-model="subProcess.procesdetails"></textarea>
              </div>
              <div class="row">
                <div class="col-2 mb-3">
                  <label class="form-label">จำนวนวันทำงาน: <span class="text-danger">*</span></label>
                  <input class="form-control " type="number" v-model="subProcess.processtart" />
                </div>
                <div class="col-2 mb-3">
                  <label class="form-label">กำหนดการส่ง: <span class="text-danger">*</span></label>
                  <input class="form-control " type="date" v-model="subProcess.procesend" />
                </div>
              </div>
              <button class="btn btn-danger me-2 button-right" type="button"
                @click="delProcess(subProcess.id, index)">ลบ</button>
              <button class="btn btn-secondary me-2 button-right" type="button" @click="toggleVisibility(index)">
                {{ subProcess.processisvisible ? 'แสดง' : 'ซ่อน' }}
              </button>
            </div>
          </div>
          <div class="row">
            <div class="mb-1">
              <button type="button" class="btn btn-secondary" @click="addProcess">เพิ่ม process</button>
            </div>
            <div class="mb-3 text-end">
              <button type="submit" class="btn btn-success button-right">ยืนยัน</button>
              <div class="mt-3"></div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, toRefs, defineProps, defineEmits } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';
import MultiSelect from 'primevue/multiselect';
import * as functions from '../function/function.inc'

const router = useRouter();
const route = useRoute();
const loading = ref(true);
const isEditMode = ref(false);
const Process = ref<SubInputBoxType[]>([]);
const store = useStore();
const users = ref([]);
const selectedUsers = ref<string[]>([]);
const selectedManager = ref<string | null>(null);
const teams = ref([]);

interface DatainfoType {
  infoname: string;
  infodetails: string;
  infostart: string;
  infoend: string;
  infotype: string;
  manager: string;
  team: string[];
}

interface SubInputBoxType {
  id: number;
  idtask: number;
  procesname: string;
  procesdetails: string;
  processtart: string;
  procesend: string;
  processisvisible: boolean;
}

const Datainfo = ref<DatainfoType>({
  infoname: '',
  infodetails: '',
  infostart: '',
  infoend: '',
  infotype: '',
  manager: '',
  team: [],
});

const taskTypes = ['ภายใน', 'จัดซื้อจัดจ้าง'];
const userStorage = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());

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



const onChange = (selectedUsersValue: any) => {
  if (!Array.isArray(selectedUsersValue)) {
    return;  // ออกจากฟังก์ชันถ้าค่าไม่เป็น array หรือ undefined
  }
  // เช็คเพื่อไม่ให้ซ้ำซ้อนใน team
  selectedUsers.value = selectedUsersValue;

  // สามารถเปลี่ยนแปลงการจัดการ team ได้ตามที่คุณต้องการ
  Datainfo.value.team = selectedUsersValue; // หรืออาจจะต้องการเพิ่มเป็น team ก็ได้
};

const toggleVisibility = (index: number) => {
  const process = Process.value[index];
  if (process) {
    process.processisvisible = !process.processisvisible; // สลับค่า ProcessisVisible
  }
};


const daysBetween = computed(() => {
  if (!Datainfo.value.infostart || !Datainfo.value.infoend) {
    return 0;
  }
  return functions.daysBetween(Datainfo.value.infostart, Datainfo.value.infoend);
});

const confirminfo = async () => {
  const missingFields = [];

  if (!Datainfo.value.infoname) {
    missingFields.push('ชื่องาน');
  }
  if (!Datainfo.value.infodetails) {
    missingFields.push('รายละเอียด');
  }
  if (!Datainfo.value.infostart) {
    missingFields.push('วันที่เริ่ม');
  }
  if (!Datainfo.value.infoend) {
    missingFields.push('วันที่จบ');
  }
  if (!Datainfo.value.infotype) {
    missingFields.push('ประเภทงาน');
  }

  // ถ้ามีฟิลด์ที่ยังไม่ได้กรอก แสดงคำเตือน
  if (missingFields.length > 0) {
    alert(`กรุณากรอกข้อมูลต่อไปนี้: ${missingFields.join(', ')}`);
    return;
  }

  // ตรวจสอบ sub-process
  for (const subInputBox of Process.value) {
    const { procesname, procesdetails, processtart, procesend } = subInputBox;
    if (!procesname || !procesdetails || processtart === undefined || !procesend) {
      alert('กรุณากรอกข้อมูลในทุก Process ที่จำเป็น');
      return;
    }
  }

  // ถ้ากรอกครบแล้ว ส่งข้อมูล
  await submitData(daysBetween);
};
// const confirminfo = async () => {
//   if (!Datainfo.value.manager) {
//     // ถ้าเป็นค่าว่าง ให้ใช้ usernamecode ของผู้ใช้ที่ล็อกอินมา
//     Datainfo.value.manager = userStorage.value.userID;
//   }
//   for (const subInputBox of Process.value) {
//     const { procesname, procesdetails, processtart, procesend } = subInputBox;
//     if (!procesname || !procesdetails || processtart === undefined || !procesend) {
//       alert('กรุณากรอกข้อมูลในทุก Process ที่จำเป็น');
//       return;
//     }
//   }
//   await submitData(daysBetween);
// };

const submitData = async (daysBetween: any) => {
  const teamArray = Object.values(Datainfo.value.team);

  const userandteam = [...teamArray, ...selectedUsers.value];

  const task = {
    infoname: Datainfo.value.infoname,
    infodetails: Datainfo.value.infodetails,
    infostart: Datainfo.value.infostart,
    infoend: Datainfo.value.infoend,
    infotype: Datainfo.value.infotype,
    manager: Datainfo.value.manager,
    userandteam,
    dayDiff: daysBetween.value,
    progressPercentage: 999,
    statusprogress: 0,
    create_by: userStorage.value.userID, // เพิ่ม create_by
  };

  console.log('Task to submit:', task);

  try {
    if (isEditMode.value) {
      const taskId = Number(route.params.id);
      await apiService.updateTask(taskId, task);
      await saveProcesses(taskId);
      router.push(`/taskdetail/${taskId}`);
    } else {
      const response = await apiService.postTask(task);
      const taskId = response.data.id;
      await saveProcesses(taskId);
      router.push(`/taskdetail/${taskId}`);
      alert('บันทึกข้อมูลสำเร็จ');
    }
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการบันทึกข้อมูล:', error);
    alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล');
  }
};

const saveProcesses = async (taskId: number) => {
  const processPromises = Process.value.map(async (process, index) => {
    const processData = {
      id: process.id,
      idtask: taskId,
      procesname: process.procesname,
      procesdetails: process.procesdetails,
      processtart: process.processtart,
      procesend: process.procesend,
      processisvisible: process.processisvisible // เพิ่มการส่งค่า ProcessisVisible
    };
    console.log(processData);

    if (process.id) {
      // มี process.id => อัปเดต
      return apiService.updateProcess(process.id, processData);
    } else {
      // ไม่มี process.id => สร้างใหม่
      processData.id = index + 1;
      return apiService.postProcess(processData);
    }
  });

  await Promise.all(processPromises);
};


const addProcess = () => {
  Process.value.push({
    id: NaN,
    idtask: NaN,
    procesname: '',
    procesdetails: '',
    processtart: '',
    procesend: '',
    processisvisible: false,
  });
};

const delProcess = async (processId: number, index: number) => {
  try {
    // ตรวจสอบก่อนว่ามี processId เพื่อส่งไปยัง API
    if (processId) {
      await apiService.deleteProcess(processId);
      console.log(`Process with ID ${processId} deleted successfully.`);
    }

    // ลบข้อมูลออกจาก array Process ทันทีหลังจากลบสำเร็จ
    Process.value.splice(index, 1);

  } catch (error) {
    console.error('Error deleting process:', error);
  }
};

onMounted(async () => {
  try {
    // ดึงข้อมูลผู้ใช้
    const userResponse = await apiService.getUser();
    users.value = userResponse.data.map(user => ({
      id: user.usernamecode,        // หรือชื่อฟิลด์ที่เหมาะสมจาก API
      username: user.username, // หรือชื่อฟิลด์ที่เหมาะสมจาก API
    }));
    const teamResponse = await apiService.getTeams();
    teams.value = teamResponse.data; // ตั้งค่า teams ให้เป็นข้อมูลจาก API
    if (route.params.id) {
      isEditMode.value = true;
      const taskId = Number(route.params.id);

      // ดึงข้อมูลงานและข้อมูล process
      const taskResponse = await apiService.getTaskById(taskId);
      const taskData = taskResponse.data;
      Object.assign(Datainfo.value, taskData);

      const processResponse = await apiService.getProcessByTaskId(taskId);
      Process.value = processResponse.data;

      selectedUsers.value = taskResponse.data.userandteam; // ตั้งค่า selectedUsers จากข้อมูลงาน

      Datainfo.value.manager = userStorage.value.userID;

      // หากคุณต้องการให้ผู้ใช้ได้เลือก manager จาก users
      // คุณอาจต้องการค้นหาผู้ใช้ที่มี ID ตรงกัน
      const defaultManager = users.value.find(user => user.id === userStorage.value.userID);
      if (defaultManager) {
        Datainfo.value.manager = defaultManager.id; // ตั้งค่า manager เป็น ID ของ user
      }
    }
  } catch (error) {
    console.error("Error loading data:", error);
    alert('เกิดข้อผิดพลาดในการโหลดข้อมูล');
  } finally {
    loading.value = false; // ปิดสถานะการโหลดเมื่อข้อมูลทั้งหมดถูกดึงแล้ว
  }
});

const props = defineProps<{
  selectedDate: { id: string; title: string; start: string; end: string; priority: number } | null; // แก้ไขประเภทให้ตรงกับวัตถุ
}>(); const emit = defineEmits<{ (e: 'update-date', event: any): void; }>();
// Watch สำหรับ infoname, infostart, และ infoend
watch(() => Datainfo.value, (newValue) => {
  if (newValue.infoname && newValue.infostart && newValue.infoend) {
    const event = {
      id: functions.createEventId(),
      title: newValue.infoname,
      start: newValue.infostart,
      end: newValue.infoend,
      priority: 1,
    };

    emit('update-date', event); // ส่งอีเวนต์ไปยัง CalendarEvents
  }
}, { deep: true }); // ใช้ deep: true เพื่อจับการเปลี่ยนแปลงใน Datainfo
</script>

<style scoped>
.container-xl {
  /* max-width: 800px; */
  margin: auto;
}

.button-right {
  float: right;
}
</style>

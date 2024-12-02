<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-4">
                <div class="section left">
                    <h5>{{ status === 'add' ? 'เพิ่มสิทธิ์การใช้งาน' : 'แก้ไขข้อมูลพนักงาน' }}</h5>
                    <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                        <div class="message-box fix">{{ item.label }}<span
                                v-if="item.key === 'employeeID' || item.key === 'FirstName' || item.key === 'LastName' || item.key === 'Mail'"
                                class="text-danger">*</span></div>
                        <div class="message-box">
                            <input
                                v-if="item.key !== 'Branch' && item.key !== 'EmployeeTerm' && item.key !== 'EmployeeStatus'"
                                v-model="formData[item.key as keyof FormData]" type="text" class="" />
                            <select v-if="item.key === 'Branch'" v-model="formData[item.key as keyof FormData]" class="">
                                <option v-for="option in options.find(opt => opt.label === 'สำนักงาน/สาขา')?.options"
                                    :key="option.value" :value="option.value">{{ option.text }} </option>
                            </select>
                            <select v-if="item.key === 'EmployeeTerm'" v-model="formData.EmployeeTerm" class="">
                                <option v-for="option in options.find(opt => opt.label === 'ทีมการทำงาน')?.options"
                                    :key="option.value" :value="option.value">{{ option.text }}</option>
                            </select>
                            <select v-if="item.key === 'EmployeeStatus'" v-model="formData.EmployeeStatus" class="">
                                <option v-for="option in options.find(opt => opt.label === 'สถานะพนักงาน')?.options"
                                    :key="option.value" :value="option.value">{{ option.text }}</option>
                            </select>
                        </div>
                    </div>
                    <button @click="EmployeeDetails" class="btn btn-primary">บันทึก</button>
                </div>
            </div>
            <div class="col-md-4">
                <div class="section center">
                </div>
            </div>
            <div class="col-md-4">
                <div class="section right">
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits, defineProps } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';

// กำหนดประเภทสำหรับ formData
type FormData = {
    employeeID: string;
    FirstName: string;
    LastName: string;
    Mail: string;
    PhoneNumber: number; // แก้ไขให้ตรงกับประเภท
    Branch: string;
    EmployeeStatus: string;
    EmployeeTerm: string;
};

const route = useRoute();
const store = useStore();
const status = ref<string>(String(route.query.status || 'view'));
const formData = ref<FormData>({
    employeeID: '',
    FirstName: '',
    LastName: '',
    Mail: '',
    PhoneNumber: 0, // ใช้เป็น 0 แทน int
    Branch: '',
    EmployeeStatus: '',
    EmployeeTerm: ''
});
const options = ref<any[]>([]);
const emit = defineEmits(['update:visible', 'confirm']);
const props = defineProps<{
    Employeedata: any; // เปลี่ยนชื่อเป็น Employeedata
}>();

const leftInfo = [
    { label: 'รหัสเข้าใช้งาน', key: 'employeeID' },
    { label: 'ชื่อ', key: 'FirstName' },
    { label: 'นามสกุล', key: 'LastName' },
    { label: 'อีเมล', key: 'Mail' },
    { label: 'เบอร์ติดต่อ', key: 'PhoneNumber' },
    { label: 'สำนักงาน/สาขา', key: 'Branch' },
    { label: 'ทีมการทำงาน', key: 'EmployeeTerm' },
    { label: 'สถานะพนักงาน', key: 'EmployeeStatus' }
];

// กำหนดค่าเริ่มต้นให้ formData จาก Employeedata
const setFormData = () => {
    if (props.Employeedata) {
        formData.value.employeeID = props.Employeedata.employeeID || '';
        formData.value.FirstName = props.Employeedata.FirstName || '';
        formData.value.LastName = props.Employeedata.LastName || '';
        formData.value.Mail = props.Employeedata.Mail || '';
        formData.value.PhoneNumber = Number(props.Employeedata.PhoneNumber) || 0; // แปลงเป็น number
        formData.value.Branch = props.Employeedata.Branch || '';
        formData.value.EmployeeStatus = props.Employeedata.EmployeeStatus || '';
        formData.value.EmployeeTerm = props.Employeedata.EmployeeTerm || '';
    }
};

const fetchOptions = async () => {
    try {
        const response = await apiService.getOptions();
        options.value = response.data;
    } catch (error) {
        console.error('Error fetching options:', error);
    }
};

const EmployeeDetails = () => {
    if(status.value === "add") emit("confirm", "add", formData.value);
    else emit("confirm", "save", formData.value ,null);
};

onMounted(() => {
    fetchOptions();
    setFormData(); // เรียกใช้งานเพื่อกำหนดค่าเริ่มต้น

    const id = Number(route.params.id);
    if (status.value === "add") {
        store.dispatch('breadcrumbs/updateBreadcrumbs', [
            { name: 'Home', path: '/', icon: 'pi pi-home' },
            { name: 'ตั้งค่า', path: '/Options', icon: 'pi pi-cog' },
            { name: 'รายละเอียด', path: '/employee/' + id, icon: '' },
            { name: 'เพิ่มสิทธิ์การใช้งาน', path: '/employee/' + id, icon: '' },
        ]);
    } else {
        store.dispatch('breadcrumbs/updateBreadcrumbs', [
            { name: 'Home', path: '/', icon: 'pi pi-home' },
            { name: 'ตั้งค่า', path: '/Options', icon: 'pi pi-cog' },
            { name: 'รายละเอียด', path: '/employee/' + id, icon: '' },
            { name: 'แก้ไขช้อมูลพนักงาน', path: '/employee/' + id, icon: '' },
        ]);
    }
});
</script>

<style scoped lang="scss">
@import "~bootstrap/scss/bootstrap";

.container-fluid {
    padding: 0;
    margin-top: 1rem;
}

.left {
    height: 100%;
}

.left,
.right {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-color: #ffffff;
    padding: 10px;
    border-radius: 20px;
}

.center {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.top,
.bottom {
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    border-radius: 20px;
}

.info {
    display: grid;
    grid-template-columns: 40% 60%;
    gap: 10px;
    align-items: center;
    padding-right: 10px;
}

input,
select {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}

.message-box {
    border: 1px solid #dee2e6;
    border-radius: 5px;
    background-color: #e9ecef;
}

.fix {
    background-color: #ffffff00;
    border: none;
}

.right {
    background-color: #f8f9fa;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #ffffff;
}

.text-danger {
    color: red;
}
</style>

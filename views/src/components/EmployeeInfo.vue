<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-4">
                <div class="section left">
                    ข้อมูลพนักงาน
                    <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                        <div :class="['message-box', 'fix', { 'required': isRequired(item.key) }]">
                            {{ item.label }}
                        </div>
                        <div class="message-box">{{ Employeedata ? Employeedata[item.key] : 'ไม่มีข้อมูล' }}</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="section center">
                    <div class="top">
                        <!-- ตรวจสอบว่า Employeedata มีค่าก่อน -->
                        <ShowLog v-if="Employeedata" :id="Employeedata.employeeID" />
                        <div v-else>ไม่มีข้อมูลพนักงาน</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="section right">
                    <!-- อาจจะเพิ่มข้อมูลที่นี่ -->
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref, onMounted , defineProps} from 'vue';
import ShowLog from './ShowLog.vue';

const props = defineProps<{
    Employeedata: any;
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

const isRequired = (key: string) => {
    const requiredKeys = ['employeeID', 'FirstName', 'LastName', 'Mail'];
    return requiredKeys.includes(key);
};
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

.message-box {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 5px;
    background-color: #e9ecef;
}

.fix {
    background-color: #ffffff00;
    border: none;
}

.required::after {
    content: '*';
    color: red;
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
</style>


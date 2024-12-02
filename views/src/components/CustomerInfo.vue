<template>
    <div v-if="!isLoading" class="container-fluid">
        <div class="row">
            <div class="col-md-4">
                <div class="section left">
                    <h3>ข้อมูลลูกค้า</h3>
                    <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                        <div class="message-box fix">{{ item.label }}</div>
                        <div class="message-box">{{ user?.[item.key] }}</div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="section center">
                    <div class="top">
                        <h3>ข้อมูลการลงทะเบียน</h3>
                        <div v-for="(item, index) in centerTopInfo" :key="'center-top-' + index" class="info">
                            <div class="message-box fix">{{ item.label }}</div>
                            <div class="message-box">{{ user?.[item.key] }}</div>
                        </div>
                    </div>
                    <div class="section bottom">
                        <ShowLog :id="user.id13" />
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="section right">
                </div>
            </div>
        </div>
    </div>
    <div v-else class="loading">
        <p>กำลังโหลดข้อมูล...</p>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';
import ShowLog from './ShowLog.vue';

const route = useRoute();
const emit = defineEmits(['refreshCustomerInfo']);
const user = ref<any>(null);
const isLoading = ref<boolean>(true);
const dialogVisible = ref<boolean>(false);

const leftInfo = [
    { label: 'เลขประจำตัว 13 หลัก', key: 'id13' },
    { label: 'เลขทะเบียนลูกค้า', key: 'RegistrationNumber' },
    { label: 'ชื่อ', key: 'FirstName' },
    { label: 'นามสกุล', key: 'LastName' },
    { label: 'วันเกิด', key: 'Birthday' },
    { label: 'หมายเลขโทรศัพท์มือถือ', key: 'PhoneNumber' },
    { label: 'อีเมล', key: 'Mail' },
    { label: 'สถานะลูกค้า', key: 'CustomerStatus' },
    { label: 'วันลงทะเบียน', key: 'RegistrationDay' },
    { label: 'สถานะการลงทะเบียน', key: 'RegistrationStatus' }
];

const centerTopInfo = [
    { label: 'เลขประจำตัว 13 หลัก', key: 'id13' },
    { label: 'เลขทะเบียนลูกค้า', key: 'RegistrationNumber' },
    { label: 'ชื่อ', key: 'FirstName' },
    { label: 'นามสกุล', key: 'LastName' },
    { label: 'วันเกิด', key: 'Birthday' }
];

const fetchUser = async (id: number) => {
    isLoading.value = true;  // ตั้งค่าเป็นโหลดใหม่
    try {
        const response = await apiService.getUser();
        const users = response.data;
        user.value = users.find((a: any) => a.id === id) || null;
    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    const id = Number(route.params.id);
    if (!isNaN(id)) {
        fetchUser(id);
    } else {
        isLoading.value = false;
    }
});
</script>

<style scoped lang="scss">
.container-fluid {
    padding: 0;
    margin-top: 1rem;
}

.info {
    display: grid;
    grid-template-columns: 40% 60%;
    gap: 10px;
    align-items: center;
    padding-right: 10px;
}
</style>

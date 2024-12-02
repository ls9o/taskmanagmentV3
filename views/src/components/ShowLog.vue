<template>
    <h3>บันทึกการเปลียนแปลง</h3>
    <div v-if="LOG" class="log">
        <div v-for="(item, index) in centerTopInfo" :key="'center-top-' + index" class="info">
            <div class="message-box fix">{{ item.label }}</div>
            <div class="message-box">{{ formatUserData(LOG, item.key) }}</div>
        </div>
    </div>
    <div v-else>
        กำลังโหลดข้อมูล...
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineProps } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';

const route = useRoute();
const LOG = ref<any>(null);
const isLoading = ref<boolean>(true);
const props = defineProps<{
    id: any;
}>();

const centerTopInfo = [
    { label: 'วันที่และเวลา', key: 'modified_date' },
    { label: 'ผู้ดำเนินการ', key: 'FirstName' },
    { label: 'รหัสการเปลี่ยนแปลง', key: 'changecode' },
    { label: 'ทีมผู้ดำเนินการ', key: 'EmployeeTerm' },
    { label: 'รายละเอียด ', key: 'description' }
];

const fetchLOG = async () => {
    try {
        const response = await apiService.getLog(props.id); 
        // const LOGs = response.data;
        LOG.value = response.data;

    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        isLoading.value = false;
    }
};

const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 19).replace("T", " ");
};

const formatUserData = (user: any, key: string) => {
    if (!user || user[0][key]=== undefined) {
        return 'ไม่มีข้อมูล';
    }
    if (key === 'modified_date') {
        return formatDateTime(user[0][key]);
    }
    return user[0][key];
};

onMounted(() => {
    fetchLOG();
});
</script>

<style scoped lang="scss">
@import "~bootstrap/scss/bootstrap";

.log{
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
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

<template>
    <div v-if="!isLoading" class="container-fluid">
        <div class="row">
            <!-- ข้อมูลลูกค้า -->
            <div class="col-md-4">
                <div class="section left">
                    ข้อมูลลูกค้า
                    <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                        <div class="message-box fix">{{ item.label }}</div>
                        <div class="message-box">{{ asset?.[item.key] }}</div>
                    </div>
                </div>
            </div>

            <!-- ข้อมูลการลงทะเบียน -->
            <div class="col-md-4">
                <div class="section center">
                    <div class="top">
                        ข้อมูลการลงทะเบียน
                        <div v-for="(item, index) in centerTopInfo" :key="'center-top-' + index" class="info">
                            <div class="message-box fix">{{ item.label }}</div>
                            <div class="message-box">{{ asset?.[item.key] }}</div>
                        </div>
                    </div>
                    <div class="bottom">
                        <ShowLog :id="asset.id13" />
                    </div>
                </div>
            </div>

            <!-- ขวา -->
            <div class="col-md-4">
                <div class="section right">
                    <!-- อาจจะมีเนื้อหาที่นี่ -->
                </div>
            </div>
        </div>
    </div>

    <!-- แสดงสถานะการโหลด -->
    <div v-else class="loading">
        <p>กำลังโหลดข้อมูล...</p>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';
import ShowLog from './ShowLog.vue';

const route = useRoute();
const asset = ref<any>(null);
const isLoading = ref<boolean>(true);

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

const fetchAsset = async (id: number) => {
    try {
        const response = await apiService.getUser();
        const assets = response.data;
        asset.value = assets.find((a: any) => a.id === id) || null;
    } catch (error) {
        console.error('Error fetching items:', error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    const id = Number(route.params.id);
    if (!isNaN(id)) {
        fetchAsset(id);
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

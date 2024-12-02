<template>
    <div v-if="!isLoading" class="container-fluid">
        <div class="row">
            <div class="col-md-4" v-if="!isNewCustomerInfoVisible">
                <div class="section center">
                    <div class="top">
                        <p class="header-text">ข้อมูลลูกค้า</p>
                    </div>
                    <div class="bottom">
                        <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                            <div class="message-box fix">{{ item.label }}</div>
                            <div class="message-box">{{ asset?.[item.key] }}</div>
                        </div>
                        <div class="info">
                            <div class="message-box fix">หมายเลขโทรศัพท์มือถือใหม่</div>
                            <input v-model="newPhoneNumber" class="message-box message-box-text form-control"
                                type="text" @input="validatePhoneNumber">
                        </div>
                        <div class="custom-dialog-footer">
                            <button class="custom-button" :disabled="!isPhoneNumberValid"
                                @click="saveNewPhoneNumber">ยืนยันหมายเลขโทรศัพท์มือถือใหม่
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4" v-if="SendOTQ">
                <div class="section center">
                    <div class="top">
                        <p class="header-text">ข้อมูลลูกค้า</p>
                    </div>
                    <div class="bottom">
                        <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                            <div class="message-box fix" v-if="item.key !== 'Birthday'">{{ item.label }}</div>
                            <div class="message-box" v-if="item.key !== 'Birthday'">{{ item.key === 'PhoneNumber' ?
                                newPhoneNumber : asset?.[item.key] }}</div>
                        </div>
                        <div class="custom-dialog-footer">
                            <button class="custom-button" @click="showOTQSection">ส่งรหัส OTP</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4" v-if="isOTQVisible">
                <div class="section center">
                    <div class="top">
                        <p class="header-text">ข้อมูลลูกค้า</p>
                    </div>
                    <div class="bottom">
                        <div v-for="(item, index) in leftInfo" :key="'left-' + index" class="info">
                            <div class="message-box fix" v-if="item.key !== 'Birthday'">{{ item.label }}</div>
                            <div class="message-box" v-if="item.key !== 'Birthday'">{{ item.key === 'PhoneNumber' ?
                                newPhoneNumber : asset?.[item.key] }}</div>
                        </div>
                        <div class="info">
                            <div class="message-box fix">OTQ Ref.</div>
                            <p class="message-box">{{ OTQRef }}</p>
                        </div>
                        <div class="info">
                            <div class="message-box fix">OTQ</div>
                            <input v-model="OTQNumber" class="message-box message-box-text form-control" type="text"
                                @input="validateOTQ">
                        </div>
                        <div class="custom-dialog-footer">
                            <button class="custom-button" :disabled="!isOTQValid" @click="confirmOTQ">
                                ยืนยัน
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4" v-if="!isNewCustomerInfoVisible">
                <div class="section center">
                    <div class="top">
                        <p class="header-text">ข้อมูลลูกค้าบนระบบ CBS</p>
                        <button class="custom-button Copy" @click="fetchCBSData">เรียกข้อมูล</button>
                    </div>
                    <div class="bottom">
                        <div v-for="(item, index) in centerTopInfo" :key="'center-top-' + index" class="info">
                            <div class="message-box fix">{{ item.label }}</div>
                            <div class="message-box">
                                <span v-if="isCBSDataVisible">{{ asset?.[item.key] }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="loading">
        <p>กำลังโหลดข้อมูล...</p>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { apiService } from '../Service/apiService';
import { defineEmits } from 'vue';
import { useStore } from 'vuex';


const route = useRoute();
const store = useStore();
const asset = ref<any>(null);
const isLoading = ref<boolean>(true);
const isCBSDataVisible = ref(false);
const isNewCustomerInfoVisible = ref(false);
const isOTQVisible = ref(false);
const SendOTQ = ref(false);

const newPhoneNumber = ref<string>('');
const OTQNumber = ref<string>('');
const OTQRef = ref<string>('123456');
const isPhoneNumberValid = ref<boolean>(false);
const isOTQValid = ref<boolean>(false);

// Events
const emit = defineEmits(['confirm']);

const leftInfo = [
    { label: 'เลขประจำตัว 13 หลัก', key: 'id13' },
    { label: 'เลขทะเบียนลูกค้า', key: 'RegistrationNumber' },
    { label: 'ชื่อ', key: 'FirstName' },
    { label: 'นามสกุล', key: 'LastName' },
    { label: 'วันเกิด', key: 'Birthday' },
    { label: 'หมายเลขโทรศัพท์มือถือ', key: 'PhoneNumber' },
];

const centerTopInfo = [
    { label: 'เลขประจำตัว 13 หลัก', key: 'id13' },
    { label: 'เลขทะเบียนลูกค้า', key: 'RegistrationNumber' },
    { label: 'ชื่อ', key: 'FirstName' },
    { label: 'นามสกุล', key: 'LastName' },
    { label: 'วันเกิด', key: 'Birthday' },
    { label: 'หมายเลขโทรศัพท์มือถือ', key: 'PhoneNumber' },
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

const fetchCBSData = () => {
    isCBSDataVisible.value = true;
};

const validatePhoneNumber = () => {
    const phoneNumber = newPhoneNumber.value;
    isPhoneNumberValid.value = /^[0-9]*$/.test(phoneNumber);
};

const validateOTQ = () => {
    const otq = OTQNumber.value;
    isOTQValid.value = otq === OTQRef.value;
};

const saveNewPhoneNumber = () => {
    if (isPhoneNumberValid.value) {
        isNewCustomerInfoVisible.value = true;
        isCBSDataVisible.value = false;
        SendOTQ.value = true;
    }
};

const showOTQSection = () => {
    SendOTQ.value = false;
    isOTQVisible.value = true;
};

const confirmOTQ = () => {
    if (isOTQValid.value) {
        isOTQVisible.value = false;
        emit('confirm', 'Changephone', newPhoneNumber.value);
    }
};

// Lifecycle Hooks
onMounted(() => {
    const id = Number(route.params.id);
    if (!isNaN(id)) {
        fetchAsset(id);
    }
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'ข้อมูลลูกค้า', path: '/Customer', icon: 'pi pi-users' },
        { name: 'รายละเอียด', path: '/user/' + id, icon: '' },
        { name: 'เปลี่ยนเบอร์โทรศัพ', path: '/user' + id, icon: '' },
    ]);
});
</script>


<style scoped lang="scss">
@import "~bootstrap/scss/bootstrap";

.container-fluid {
    padding: 0;
    margin-top: 1rem;
}

.center {
    gap: 0px;
}

.top {
    border-radius:0px;
}

.bottom {
    border-radius:0px 0px 15px 15px;
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
    min-height: 40px;
    display: flex;
    align-items: center;
}

.message-box-text {
    background-color: #ffffff !important;
}

.fix {
    background-color: #ffffff00;
    border: none;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #ffffff;
}

.custom-dialog-footer {
    display: flex;
    justify-content: center;
    padding: 10px;
}

.custom-button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background-color: #1e22aa;
    color: white;
    width: 75%;
}

.Copy {
    border-radius: 15px;
    background-color: #3f567a;
    width: auto;
}

.header-text {
    color: #0e14aa;
    margin-left: 10px;
}
</style>

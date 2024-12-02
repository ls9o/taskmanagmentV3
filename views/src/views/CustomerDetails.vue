<template>
    <SubMenu @navigate="handleNavigation" :status="user?.CustomerStatus" :isChangephoneVisible="changephone" />
    <Succeed v-if="showSucceed" @close="Close" :message="message" />
    <CustomDialog v-if="showUnlockDialog" :visible="showUnlockDialog" @confirm="confirmAction" />
    <RemoveRightsDialog v-if="RemoveRight" :visible="RemoveRight" @confirm="confirmAction" />

    <div class="container-fluid">
        <div v-if="!isLoading">
            <CustomerInfo v-if="customerinfo" :user="user" @refreshCustomerInfo="fetchData" />
            <Changephone v-if="changephone" @confirm="confirmAction" />
        </div>
        <Loading v-else />
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, defineEmits, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';

import SubMenu from '@/components/SubMenu.vue';
import Succeed from '@/components/Succeed_component.vue';
import CustomDialog from '@/components/CustomDialog.vue';
import CustomerInfo from '@/components/CustomerInfo.vue';
import Changephone from '@/components/Changephone_components.vue';
import RemoveRightsDialog from '@/components/RemoveRightsDialog.vue';

const route = useRoute();
const router = useRouter();
const store = useStore();

const user = ref<any>(null);
const isLoading = ref<boolean>(true);
const showSucceed = ref<boolean>(false);
const customerinfo = ref<boolean>(true);
const showUnlockDialog = ref<boolean>(false);
const RemoveRight = ref<boolean>(false);
const changephone = ref<boolean>(false);
const emit = defineEmits(['refreshCustomerInfo']);
const userStorage = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());

let message = '';

const fetchData = async () => {
    resetStates();
    const id = Number(route.params.id);
    if (!isNaN(id)) {
        try {
            const response = await apiService.getUser();
            user.value = response.data.find((a: any) => a.id === id) || null;
        } catch (error) {
            console.error('Error fetching items:', error);
        } finally {
            isLoading.value = false;
        }
    }
};

const resetStates = () => {
    user.value = null;
    isLoading.value = true;
    showSucceed.value = false;
    customerinfo.value = true;
    showUnlockDialog.value = false;
    RemoveRight.value = false;
    changephone.value = false;
    message = '';
};
const handleNavigation = (path: string) => {
    switch (path) {
        case '/back':
            router.push(`/Customer`);
            break;
        case '/unlock':
            showUnlockDialog.value = true;
            break;
        case '/Change-phone':
            changephone.value = !changephone.value;
            customerinfo.value = !changephone.value;
            break;
        case '/Cancel-service':
            RemoveRight.value = true;
            break;
    }
};

const confirmAction = async (reason: string, comment: string | number) => {
    const id = Number(route.params.id);
    const item = { CustomerStatus: "" };
    const log = createLogEntry((comment));
    if (reason === 'close') {
        showUnlockDialog.value = false;
        RemoveRight.value =false;
    }
    else if (reason === 'Remove') {
        item.CustomerStatus = "ยกเลิกบริการ";
        await updateUserStatus(id, item, log);
    } 
    else if (reason === 'unlock') {
        item.CustomerStatus = "พร้อมใช้งาน";
        log.description = "ปลดล็อก/ปลดบล็อก";
        await updateUserStatus(id, item, log);
    }
    else if (reason === 'Changephone') {
        log.description = "เปลี่ยนเบอร์โทรศัพท์มือถือ";
        updateUserPhone(id, comment, log)
    }

    updateBreadcrumbs();
};
const createLogEntry = (comment: string | number) => ({
    id13: user.value.id13,
    operatorBy: userStorage.value.employeeID,
    description: comment,
    EmployeeTerm: userStorage.value.EmployeeTerm
});

const updateUserStatus = async (id: number, item: any, log: object) => {
    try {
        await apiService.putUser_change_status(id, item);
        await apiService.postLog(log);
        fetchData();
        message = item.CustomerStatus === "ยกเลิกบริการ" ? "ยกเลิกบริการสำเร็จ" : "ปลดล็อก/ปลดบล็อกสำเร็จ";
        showSucceed.value = true;
    } catch (error) {
        console.error("Failed to update user:", error);
    }
};
const Close = () => {
    showSucceed.value = false;
};

const updateUserPhone = async (id: number, phone: string | number, log: object) => {
    try {
        await apiService.putUser_change_status(id, { PhoneNumber: phone });
        await apiService.postLog(log);
        fetchData();
        changephone.value = false;
        customerinfo.value = true;
        message = "เปลี่ยนเบอร์โทรศัพท์มือถือสำเร็จ";
        showSucceed.value = true;
        updateBreadcrumbs();
    } catch (error) {
        console.error("Failed to update user:", error);
    }
};
const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'ข้อมูลลูกค้า', path: '/Customer', icon: 'pi pi-users' },
        { name: 'รายละเอียด', path: '/Customer', icon: '' },
    ]);
};
const getUserFromLocalStorage = () => {
    const user = localStorage.getItem("user");
    if (user) {
        try {
            return JSON.parse(user);
        } catch (e) {
            console.error("Error parsing user data from localStorage:", e);
            return null;
        }
    }
    return null;
};

watch(() => route.query.reload, () => {
    fetchData();
});

// Fetch data on mounted
onMounted(() => {
    fetchData();
    updateBreadcrumbs();
});
</script>

<style scoped lang="scss">

</style>

<template>
    <SubMenu @navigate="handleNavigation" :status="Employeedata?.CustomerStatus" :isChangephoneVisible="false" />
    <Succeed v-if="showSucceed" @close="Close" :message="message" />
    <RemoveRightsDialog v-if="RemoveRight" :visible="RemoveRight" @confirm="confirmAction" />

    <div class="container-fluid">
        <div v-if="!isLoading">
            <EmployeeInfo v-if="employeeinfo && status !== 'add'" :Employeedata="Employeedata" />
            <EmployeeEdit v-if="employeeedit || status === 'add'" :Employeedata="Employeedata" @confirm="confirmAction" />
        </div>
        <Loading v-else />
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiService } from '../Service/apiService';
import { useStore } from 'vuex';

import SubMenu from '@/components/SubMenu.vue';
import Succeed from '@/components/Succeed_component.vue';
import EmployeeInfo from '@/components/EmployeeInfo.vue';
import EmployeeEdit from '../components/EmployeeEdit.vue';
import RemoveRightsDialog from '@/components/RemoveRightsDialog.vue';

const route = useRoute();
const router = useRouter();
const store = useStore();

const Employeedata = ref<any>(null);
const isLoading = ref<boolean>(true);
const showSucceed = ref<boolean>(false);
const employeeinfo = ref<boolean>(true);
const employeeedit = ref<boolean>(false);
const status = ref<string | null>(null);
const RemoveRight = ref<boolean>(false);
const hasRemoved = ref<boolean>(false);
const userStorage = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());

let message = '';

const createLogEntry = (comment: string | number, newEmployeeID: string) => ({
    employeeID: Employeedata.value?.employeeID || newEmployeeID,
    operatorBy: userStorage.value.employeeID,
    description: comment,
    EmployeeTerm: userStorage.value.EmployeeTerm
});

const fetchData = async () => {
    Employeedata.value = null;
    isLoading.value = true;
    showSucceed.value = false;
    message = '';

    const id = Number(route.params.id);
    if (!isNaN(id)) {
        try {
            const response = await apiService.getEmployee();
            const Employeedatas = response.data;
            Employeedata.value = Employeedatas.find((a: any) => a.id === id) || null;
            if (!Employeedata.value) {
                message = 'ไม่พบข้อมูล';
            }
        } catch (error) {
            console.error('Error fetching items:', error);
            message = 'เกิดข้อผิดพลาดในการโหลดข้อมูล';
        } finally {
            isLoading.value = false;
        }
    }
};

const handleNavigation = (path: string) => {
    switch (path) {
        case '/back':
            router.push(`/Options`);
            break;
        case '/edit':
            employeeinfo.value = false;
            employeeedit.value = true;
            break;
        case '/delete':
            RemoveRight.value = true;
            break;
    }
};

const Close = () => {
    showSucceed.value = false;
};

const confirmAction = async (reason: string, data: any, comment: string | number) => {
    const Id = Number(route.params.id);
    const employeeIDToLog = data && data.employeeID ? data.employeeID : '';
    const log = createLogEntry(comment, employeeIDToLog);
    try {
        if (reason === 'close') {
            RemoveRight.value = false;
        }
        else if (reason === 'Remove') {
            await apiService.updataEmployee(Id, { EmployeeStatus: "ลบสิทธิ์การทำงาน" });
            await apiService.postLog(log);
            RemoveRight.value = false;
            message = "ลบสิทธิ์การใช้งานสำเร็จ";
            showSucceed.value = true;
        }
        else if (reason === "add") {
            if (data) {
                const response = await apiService.createEmployee(data);

                const newID = response.data.id;
                log.description = 'เพิ่มสิทธิ์การใช้งาน';
                await apiService.postLog(log);

                message = "เพิ่มสิทธิ์การใช้งานสำเร็จ";
                showSucceed.value = true;
                status.value = "";
                router.push({ path: `/employee/${newID}` });
            }
        }
        else if (reason === "save") {
            if (data) {
                await apiService.updataEmployee(Id, data);

                log.description = 'แก้ไขข้อมูลพนักงาน';
                await apiService.postLog(log);

                message = "แก้ไขข้อมูลพนักงานสำเร็จ";
                showSucceed.value = true;
            }
        }
        fetchData();
    } catch (error) {
        console.error('เกิดข้อผิดพลาดในการบันทึกข้อมูล:', error);
    }

    employeeinfo.value = true;
    employeeedit.value = false;
    updateBreadcrumbs();
};

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

watch(() => route.query.status, (newStatus) => {
    status.value = Array.isArray(newStatus) ? newStatus[0] || null : newStatus;

    if (status.value === 'Remove' && !hasRemoved.value) {
        message = "ลบสิทธิ์การใช้งานสำเร็จ";
        showSucceed.value = true;
        hasRemoved.value = true;
    }
    fetchData();
}, { immediate: true });

onMounted(() => {
    fetchData();
    updateBreadcrumbs();
});

const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'ตั้งค่า', path: '/Options', icon: 'pi pi-cog' },
        { name: 'รายละเอียด', path: '/Optionsด', icon: '' },
    ]);
};
</script>

<style scoped lang="scss">
@import "~bootstrap/scss/bootstrap";

.left,
.right {
    padding: 10px;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.center {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.top,
.bottom {
    background-color: #ffffff;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.message-box {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 5px;
    background-color: #e9ecef;
    flex: 1;
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

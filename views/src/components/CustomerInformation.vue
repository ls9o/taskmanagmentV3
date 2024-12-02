<template>
    <RemoveRightsDialog v-if="showUnlockDialog" :visible="showUnlockDialog" @confirm="confirm" />
    <div class="table-container">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th v-for="header in currentHeaders" :key="header.key" @click="sort(header.key)" :class="{
                        'sorted-asc': sortKey === header.key && sortOrder === 'asc',
                        'sorted-desc': sortKey === header.key && sortOrder === 'desc',
                    }">
                        <div class="d-flex justify-content-center align-items-center">
                            {{ header.text }}
                            <div>
                                <span class="triangle-up"></span><span class="triangle-down"></span>
                            </div>
                        </div>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="tr" v-for="user in sortedItems" :key="user.id"
                    @click="goToDetails(user.id, user.employeeID)">
                    <td>
                        <i v-if="showDeleteIcon" class="pi pi-trash"></i>
                        {{ formatUserData(user, currentHeaders[0].key) }}
                    </td>
                    <td v-for="header in currentHeaders.slice(1)" :key="header.key">
                        {{ formatUserData(user, header.key) }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch, defineProps, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from 'vuex';
import { apiService } from "../Service/apiService";
import RemoveRightsDialog from "./RemoveRightsDialog.vue";

const router = useRouter();
const route = useRoute();
const store = useStore();

const props = defineProps<{
    headers: any[];
    dataApi: any;  // props ที่รับข้อมูล
    showDeleteIcon: boolean;
}>();

const users = ref<Record<string, any>[]>(props.dataApi);  // ใช้ dataApi ที่ได้รับจาก props
const sortKey = ref<string | null>(null);
const sortOrder = ref<"asc" | "desc" | "none">("none");
const currentHeaders = ref(props.headers);
const showUnlockDialog = ref<boolean>(false);
const userStorage = computed(() => store.state.storeLogin.user || getUserFromLocalStorage());

let ID: number;
let employeeIDToLog: string;

const sortedItems = computed(() => {
    if (sortOrder.value === "none" || !sortKey.value) {
        return users.value;
    }

    return [...users.value].sort((a, b) => {
        const key = sortKey.value as string;
        const valueA = a[key];
        const valueB = b[key];

        return sortOrder.value === "asc" ? (valueA > valueB ? 1 : -1) : (valueA < valueB ? 1 : -1);
    });
});

function sort(key: string) {
    if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === "asc" ? "desc" : (sortOrder.value === "desc" ? "none" : "asc");
    } else {
        sortKey.value = key;
        sortOrder.value = "asc";
    }
}

function goToDetails(id: number, employeeID: string) {
    ID = id;
    employeeIDToLog = employeeID;
    const path = route.path;
    if (props.showDeleteIcon) {
        showUnlockDialog.value = true;
        return;
    }
    const userPath = path === "/Customer" ? `/user/${id}` : `/employee/${id}`;
    router.push({ path: userPath, query: path === "/Options" ? { status: '' } : undefined });
}

const createLogEntry = (id: string, comment: string | number) => ({
    employeeID: id,
    operatorBy: userStorage.value.employeeID,
    description: comment,
    EmployeeTerm: userStorage.value.EmployeeTerm
});

const confirm = async (reason: string, comment: any) => {
    showUnlockDialog.value = false;
    if (reason === 'Remove') {
        const log = createLogEntry(employeeIDToLog, comment);
        try {
            await apiService.postLog(log);
        } catch (error) {
            console.error('เกิดข้อผิดพลาดในการบันทึกข้อมูล:', error);
        }
        router.push({ path: `/employee/${ID}`, query: { status: 'Remove' } });
    }
};

const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 19).replace("T", " "); // YYYY-MM-DD HH:MM:SS
};

const formatUserData = (user: any, key: string) => {
    // if (key === 'DateModified') { // replace with actual field that contains the timestamp
    //     return formatDateTime(user[key]);
    // }
    return user[key];
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

watch(
    () => route.path,
    (newPath) => {
        // Reload users only if the route path changes
        if (newPath) {
            users.value = props.dataApi; // Refresh users from props when the route changes
        }
    }
);

watch(
    () => props.headers,
    (newHeaders) => {
        currentHeaders.value = newHeaders;
    },
    { immediate: true }
);

watch(
    () => [ props.showDeleteIcon],
    () => {
        users.value = props.dataApi;
    }
);
</script>


<style lang="scss" scoped></style>

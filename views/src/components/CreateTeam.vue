<template>
    <div class="container-xl">
        <h1 class="text-center mb-4">{{ isEditMode ? 'Edit Team' : 'Create Team' }}</h1>

        <div v-if="loading">
            <p>กำลังโหลด...</p>
        </div>

        <form v-if="!loading" @submit.prevent="confirmTeamInfo">
            <div>
                <div class="row">
                    <!-- ชื่อทีม -->
                    <div class="col-12 mb-5">
                        <label class="form-label">ชื่อทีม: <span class="text-danger">*</span></label>
                        <input class="form-control p-3" type="text" v-model="teamInfo.teamname" required />
                    </div>

                    <!-- ผู้ใช้ในทีม -->
                    <div class="col-12 mb-5">
                        <label class="form-label">ผู้ใช้ในทีม:</label>
                        <MultiSelect v-model="selectedUsers" :options="users" optionLabel="username" optionValue="id"
                            :maxSelectedLabels="3" filter placeholder="เลือกผู้ใช้" class="w-full" />
                    </div>
                </div>

                <div class="mb-3 text-end">
                    <button type="submit" class="btn btn-success button-right">ยืนยัน</button>
                    <div class="mt-3"></div>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../Service/apiService';
import MultiSelect from 'primevue/multiselect';
import { useStore } from 'vuex';

const router = useRouter();
const loading = ref(true);
const isEditMode = ref(false);
const selectedUsers = ref<string[]>([]);
const teamInfo = ref<{ teamname: string }>({
    teamname: '',
});
const users = ref([]);

const store = useStore();
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

const confirmTeamInfo = async () => {
    // ตรวจสอบว่ากรอกชื่อทีมและเลือกผู้ใช้ในทีม
    if (!teamInfo.value.teamname && selectedUsers.value.length === 0) {
        alert('กรุณากรอกชื่อทีมและเลือกผู้ใช้ในทีม');
        return;
    }

    // กรณีกรอกแค่ชื่อทีมแต่ไม่ได้เลือกผู้ใช้
    if (!teamInfo.value.teamname) {
        alert('กรุณากรอกชื่อทีม');
        return;
    }

    // กรณีเลือกผู้ใช้ในทีมแต่ไม่ได้กรอกชื่อทีม
    if (selectedUsers.value.length === 0) {
        alert('กรุณาเลือกผู้ใช้ในทีม');
        return;
    }

    // ข้อมูลทีมที่ส่งไปยัง API
    const teamData = {
        teamname: teamInfo.value.teamname,
        user: Object.fromEntries(selectedUsers.value.map(userId => [userId, userId])), // จัดการข้อมูล user
    };

    try {
        await apiService.postTeam(teamData);
        alert('บันทึกข้อมูลทีมสำเร็จ');

        // นำทางกลับไปยังหน้า CreateTeam
        router.push('/CreateTeam');
    } catch (error) {
        console.error('เกิดข้อผิดพลาดในการบันทึกข้อมูลทีม:', error);
        alert('เกิดข้อผิดพลาดในการบันทึกข้อมูลทีม');
    }
};


onMounted(async () => {
    try {
        const response = await apiService.getUser();
        users.value = response.data.map(user => ({
            id: user.usernamecode,
            username: user.username,
        }));
    } catch (error) {
        console.error("Error loading user data:", error);
        alert('เกิดข้อผิดพลาดในการโหลดข้อมูลผู้ใช้');
    } finally {
        loading.value = false; // ปิดสถานะการโหลด
    }
});
</script>

<style scoped>
.form-control,
.p-multiselect {
    width: 100% !important;
}
</style>

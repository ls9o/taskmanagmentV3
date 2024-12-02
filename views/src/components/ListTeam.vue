<template>
    <div>
        <h1>List of Teams</h1>
        <div class="table-container">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Team Name</th>
                        <th>Users</th>
                        <th>delete</th> <!-- คอลัมน์ใหม่สำหรับลบ -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="team in teams" :key="team.id">
                        <td>{{ team.teamname }}</td>
                        <td>{{ formatUsers(team.user) }}</td>
                        <td>
                            <button @click="handleDelete(team.id)" class="btn btn-danger">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { apiService } from '../Service/apiService';

// ข้อมูลทีม
const teams = ref([]);

// ดึงข้อมูลทีมจาก API
const fetchTeams = async () => {
    try {
        const response = await apiService.getTeams();
        teams.value = response.data;
    } catch (error) {
        console.error('Error fetching teams:', error);
    }
};

// ฟังก์ชันสำหรับจัดรูปแบบข้อมูลผู้ใช้
const formatUsers = (users: Record<string, string>) => {
    return Object.entries(users)
        .map(([key, value]) => `${value}`)
        .join(', ');
};

// ฟังก์ชันสำหรับลบทีม
const handleDelete = async (teamID: number) => {
    try {
        await apiService.deleteTeams(teamID); // เรียก API เพื่อลบทีม
        teams.value = teams.value.filter(team => team.id !== teamID); // อัปเดตข้อมูลทีมหลังจากลบ
        console.log('Team deleted successfully');
    } catch (error) {
        console.error('Error deleting team:', error);
    }
};

onMounted(fetchTeams);
</script>

<style>
.table-container {
    margin: 20px auto;
    max-width: 800px;
}

.table {
    width: 100%;
    border-collapse: collapse;
}

.table th,
.table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

.table-hover tr:hover {
    background-color: #f5f5f5;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
}

.btn-danger:hover {
    background-color: #c82333;
}
</style>

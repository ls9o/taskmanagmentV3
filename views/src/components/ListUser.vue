<template>
    <div>
        <h1>List of Users</h1>
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
                                    <!-- Icon for sorting -->
                                    <span v-if="sortKey === header.key && sortOrder === 'asc'"
                                        class="triangle-up"></span>
                                    <span v-if="sortKey === header.key && sortOrder === 'desc'"
                                        class="triangle-down"></span>
                                </div>
                            </div>
                        </th>
                        <th>Delete</th> <!-- เพิ่มคอลัมน์ Delete -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in sortedItems" :key="user.id">
                        <td>
                            {{ formatUserData(user, currentHeaders[0].key) }}
                        </td>
                        <td v-for="header in currentHeaders.slice(1)" :key="header.key">
                            {{ formatUserData(user, header.key) }}
                        </td>
                        <td>
                            <button @click="handleDelete(user.id)" class="btn btn-danger">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { apiService } from '../Service/apiService';

interface User {
    id: number;
    username: string;
    usernamecode: string;
    firstName: string;
    lastName: string;
    mail: string;
}

const users = ref<User[]>([]);
const sortKey = ref('');
const sortOrder = ref('asc');

// หัวข้อของตารางที่จะแสดง
const currentHeaders = ref([
    { key: 'username', text: 'Username' },
    { key: 'firstName', text: 'First Name' },
    { key: 'lastName', text: 'Last Name' },
    { key: 'mail', text: 'Email' },
]);

// ดึงข้อมูลผู้ใช้จาก API
const fetchUsers = async () => {
    try {
        const response = await apiService.getUser();
        users.value = response.data;
        console.log(response);
        
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};

// จัดการการเรียงลำดับข้อมูล
const sort = (key: string) => {
    if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortKey.value = key;
        sortOrder.value = 'asc';
    }
};

// ฟังก์ชันจัดการการเรียงข้อมูล
const sortedItems = computed(() => {
    return [...users.value].sort((a, b) => {
        const aValue = a[sortKey.value] ? String(a[sortKey.value]) : '';
        const bValue = b[sortKey.value] ? String(b[sortKey.value]) : '';
        const result = aValue.localeCompare(bValue);
        return sortOrder.value === 'asc' ? result : -result;
    });
});

// ฟังก์ชันแปลงข้อมูลผู้ใช้
const formatUserData = (user: User, key: string) => {
    return user[key as keyof User];
};

// ฟังก์ชันลบผู้ใช้
const handleDelete = async (userID: number) => {
    console.log('Deleting user with ID:', userID); // ตรวจสอบค่า userID
    try {
        await apiService.deleteUser(userID); // เรียก API เพื่อลบผู้ใช้
        users.value = users.value.filter(user => user.id !== userID); // อัพเดตข้อมูลที่แสดงหลังจากลบ
        console.log('User deleted successfully');
    } catch (error) {
        console.error('Error deleting user:', error);
    }
};


onMounted(fetchUsers);
</script>

<style>
.table-container {
    margin: 20px auto;
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

.tr:hover {
    background-color: #f5f5f5;
}

.sorted-asc .triangle-up {
    border-bottom: 6px solid black;
}

.sorted-desc .triangle-down {
    border-top: 6px solid black;
}

.triangle-up,
.triangle-down {
    display: inline-block;
    width: 0;
    height: 0;
    margin-left: 8px;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
}

.triangle-up {
    border-bottom: 6px solid lightgray;
}

.triangle-down {
    border-top: 6px solid lightgray;
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
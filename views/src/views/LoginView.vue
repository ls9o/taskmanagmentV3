<template>
    <div class="container">
        <!-- แสดงรูปภาพตาม path -->
        <div class="image-container">
            <img :src="require('@/assets/images/logo/logo.png')" alt="รูปภาพ" />
        </div>
        <!-- ฟอร์มเข้าสู่ระบบ -->
        <form class="login-form" @submit.prevent="ChackLogin">
            <div class="form-group">
                <small class="welcome-text">ยินดีต้อนรับ</small>
                <small class="connect-text">SME D Connect Back Office</small>
                <small class="please-text">กรุณาระบุรหัสผู้ใช้งานและรหัสผ่านเพื่อเริ่มต้นการใช้งาน</small>
                <small id="emailHelp" class="form-text text-muted">กรุณาใส่ login เดียวกันกับ internet และ outlook
                    เพื่อเข้าสู่ระบบ</small>

                <input type="text" v-model="getlogin.ID" class="form-control" placeholder="Login (Outlook)">
            </div>
            <div class="form-group">
                <input type="password" v-model="getlogin.Password" class="form-control" placeholder="Password">
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>

    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // นำเข้า useRouter
import { apiService } from '../Service/apiService';
const imagePath = ref('../assets/images/logo@2x.png');

interface User {
    id: number;
    userID: string;
    password: string;
    username: string;
    email: string;
    phone: string;
    Identification_number: string;
    Contract_Numbers: string;
    status: string;
}

const users = ref<User[]>([]);
const getlogin = ref({
    ID: '',
    Password: '',
});

const router = useRouter(); // สร้าง router instance

async function ChackLogin() {
    try {
        const response = await apiService.getUser();
        users.value = response.data;

        // ตรวจสอบว่ามีผู้ใช้ที่ตรงกับข้อมูลหรือไม่
        const user = users.value.find(user =>
            user.userID === getlogin.value.ID && user.password === getlogin.value.Password
        );

        if (user) {
            // ถ้าตรง ให้ไปที่หน้าอื่น
            router.push('/'); // เปลี่ยนเส้นทางไปที่หน้า 'next-page'
        } else {
            // ถ้าไม่ตรง แสดงข้อความแสดงข้อผิดพลาด
            alert('Invalid login credentials');
        }
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}
</script>


<style scoped lang="scss">
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 20px;
}

.image-container {
    margin-bottom: 20px;
}

.image-container img {
    max-width: 100%;
    height: auto;
}

.text-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
}

.welcome-text,
.connect-text,
.please-text {
    margin: 5px 0;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 300px; // ปรับขนาดของฟอร์มตามต้องการ
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.form-control {
    width: 100%; // ใช้ความกว้างเต็มของฟอร์ม
}

.btn {
    width: 100%; // ให้ปุ่มมีความกว้างเต็ม
    padding: 10px; // ปรับขนาดปุ่ม
    border-radius: 8px; // ใช้ขอบมน
}

.btn-primary {
    background-color: #007bff; // สีพื้นหลังปุ่ม
    color: #fff; // สีข้อความปุ่ม
    border: none; // ไม่มีเส้นขอบ
}

.btn-primary:hover {
    background-color: #0056b3; // สีพื้นหลังปุ่มเมื่อ hover
}
</style>

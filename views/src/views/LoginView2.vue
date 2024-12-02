<template>
    <div class="content-wrapper" v-if="!isLoggedIn">
        <div class="image-container">
            <img :src="require('@/assets/images/logo/bg_project@2x.png')" />
        </div>

        <div class="text-container">
            <form class="login-form" @submit.prevent="checkLogin">
                <div class="form-group">
                    <h3 class="welcome-text">ยินดีต้อนรับ</h3>
                    <h5 class="connect-text">SME D Connect Back Office</h5>
                    <h5 class="please-text">กรุณาระบุรหัสผู้ใช้งานและรหัสผ่านเพื่อเริ่มต้นการใช้งาน</h5>
                </div>
                <div class="form-group mt-3">
                    <label>รหัสผู้ใช้งาน</label>
                    <input type="text" v-model="getLogin.id" class="form-control" placeholder="Login (Outlook)" required>
                    <label>รหัสผ่าน</label>
                    <input type="password" v-model="getLogin.password" class="form-control" placeholder="Password" required>
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { apiService } from '@/Service/apiService';


const getLogin = ref({
    id: 'test001',
    password: '123456',
});
const router = useRouter();
const store = useStore(); // ใช้งาน Vuex store

// ตรวจสอบสถานะการล็อกอิน
const isLoggedIn = computed(() => store.state.isLoggedIn);

async function checkLogin() {
    try {
        const response = await apiService.login({
            username: getLogin.value.id,
            password: getLogin.value.password
        });

        if (response && response.data) {
            await store.dispatch('storeLogin/login', { username: getLogin.value.id, password: getLogin.value.password });

            // ถ้าผู้ใช้ล็อกอินสำเร็จให้ส่งไปหน้าแรก
            router.push('/'); 
        } else {
            alert('Invalid login credentials');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed, please try again.');
    }
}
</script>

<style scoped lang="scss">
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 0;
    margin: 0;
}

.content-wrapper {
    display: grid;
    grid-template-columns: 60% 40%;
    height: 100vh;
    width: 100vw;

}

.image-container {
    background-color: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    box-shadow: 12px 2px 9px 1px rgb(15 19 33 / 37%);
}

.text-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.image-container img {
    height: 100vh;
    width: 100vw;
    object-fit: cover;
}


.welcome-text,
.connect-text,
.please-text {
    color: #3d567a;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 300px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.form-control {
    width: 100%;
}

.btn {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
}

.btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.form-group:first-of-type {
    margin-bottom: 0;
    gap: 0px;
}

.form-group:nth-of-type(2) {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>

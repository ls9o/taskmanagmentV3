<template>
    <div class="container-xl">
        <h1>Create User</h1>
        <form @submit.prevent="createUser">
            <div>
                <label for="username">Username <span class="text-danger">*</span> </label>
                <input v-model="user.username" id="username" type="text" required />
            </div>

            <div>
                <label for="usernamecode">Username Code <span class="text-danger">*</span> </label>
                <input v-model="user.usernamecode" id="usernamecode" type="text" required />
            </div>

            <div>
                <label for="password">Password <span class="text-danger">*</span> </label>
                <input v-model="user.password" id="password" type="password" required />
            </div>

            <div>
                <label for="firstName">First Name <span class="text-danger">*</span> </label>
                <input v-model="user.firstName" id="firstName" type="text" required />
            </div>

            <div>
                <label for="lastName">Last Name <span class="text-danger">*</span> </label>
                <input v-model="user.lastName" id="lastName" type="text" required />
            </div>

            <div>
                <label for="neckname">Nickname </label>
                <input v-model="user.neckname" id="neckname" type="text" />
            </div>

            <div>
                <label for="mail">Email</label>
                <input v-model="user.mail" id="mail" type="email" />
            </div>

            <div>
                <label for="phoneNumber">Phone Number</label>
                <input v-model="user.phoneNumber" id="phoneNumber" type="text" />
            </div>

            <div>
                <label for="internal_contact_number">Internal Contact Number</label>
                <input v-model="user.internal_contact_number" id="internal_contact_number" type="text" />
            </div>

            <div>
                <label for="BranchDepartment">Branch Department</label>
                <select v-model="user.BranchDepartment" id="BranchDepartment">
                    <option value="01">01</option>
                    <option value="02">02</option>
                    <option value="03">03</option>
                </select>
            </div>

            <div>
                <label for="jobposition">Job Position</label>
                <select v-model="user.jobposition" id="jobposition">
                    <option value="01">01</option>
                    <option value="02">02</option>
                    <option value="03">03</option>
                </select>
            </div>

            <div>
                <label for="Branch">Branch</label>
                <select v-model="user.Branch" id="Branch">
                    <option value="01">01</option>
                    <option value="02">02</option>
                </select>
            </div>

            <div>
                <label for="level">Level</label>
                <select v-model="user.level" id="level">
                    <option value="01">01</option>
                    <option value="02">02</option>
                </select>
            </div>

            <div>
                <label for="LINEID">LINE ID</label>
                <input v-model="user.LINEID" id="LINEID" type="text" />
            </div>

            <button type="submit" class="btn btn-success">Create User</button>
        </form>
        <p v-if="errorMessage" style="color:red;">{{ errorMessage }}</p>
    </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { apiService } from '../Service/apiService'; // เรียกใช้ apiService ที่คุณสร้าง

interface User {
    username: string;
    usernamecode: string;
    password: string;
    firstName: string;
    lastName: string;
    neckname?: string;
    mail?: string;
    phoneNumber?: string;
    internal_contact_number?: string; // เพิ่มฟิลด์นี้
    BranchDepartment: string;
    jobposition: string;
    Branch: string;
    level: string;
    LINEID?: string;
}

const user = reactive<User>({
    username: '',
    usernamecode: '',
    password: '',
    firstName: '',
    lastName: '',
    neckname: '',
    mail: '',
    phoneNumber: '',
    internal_contact_number: '', // ฟิลด์ใหม่
    BranchDepartment: '03',
    jobposition: '03',
    Branch: '02',
    level: '02',
    LINEID: ''
});

const errorMessage = ref<string | null>(null); // เก็บข้อผิดพลาด

const createUser = async () => {
    errorMessage.value = null; // เริ่มต้นด้วยการลบข้อความ error ก่อน
    const usernameMaxLength = 10;
    const passwordMaxLength = 10;
    const usernamecodeMaxLength = 10;
    const phoneNumberMaxLength = 10;
    const contactNumberMaxLength = 10;
    const emailMaxLength = 50;
    
    // ตรวจสอบความถูกต้องของฟิลด์ที่บังคับต้องกรอก
    if (!user.username || !user.usernamecode || !user.password || !user.firstName || !user.lastName) {
        errorMessage.value = "กรุณากรอกข้อมูลในฟิลด์ที่จำเป็นให้ครบถ้วน.";
        return;
    }

    // ตรวจสอบความยาวของฟิลด์
    if (user.username.length > usernameMaxLength) {
        errorMessage.value = `Username ควรกรอกไม่เกิน ${usernameMaxLength} ตัวอักษร.`;
        return;
    }

    if (user.usernamecode.length > usernamecodeMaxLength) {
        errorMessage.value = `Username ควรกรอกไม่เกิน ${usernamecodeMaxLength} ตัวอักษร.`;
        return;
    }

    if (user.password.length > passwordMaxLength) {
        errorMessage.value = `Password ควรกรอกไม่เกิน ${passwordMaxLength} ตัวอักษร.`;
        return;
    }

    if (user.phoneNumber && user.phoneNumber.length > phoneNumberMaxLength) {
        errorMessage.value = `Phone number ควรกรอกไม่เกิน ${phoneNumberMaxLength} ตัวอักษร.`;
        return;
    }

    if (user.internal_contact_number && user.internal_contact_number.length > contactNumberMaxLength) {
        errorMessage.value = `Internal contact number ควรกรอกไม่เกิน ${contactNumberMaxLength} ตัวอักษร.`;
        return;
    }

    if (user.mail && user.mail.length > emailMaxLength) {
        errorMessage.value = `Email ควรกรอกไม่เกิน ${emailMaxLength} ตัวอักษร.`;
        return;
    }

    try {
        // ส่งข้อมูลไปยัง API เพื่อสร้าง user
        const response = await apiService.createItem({
            ...user,
            is_active: true,
        });
        alert('User created successfully');
        resetForm();
    } catch (error: any) {
        errorMessage.value = error.response?.data?.message || 'เกิดข้อผิดพลาดในการสร้างผู้ใช้';
        console.error('Error creating user:', error);
    }
};


// ฟังก์ชันรีเซ็ตฟอร์ม
const resetForm = () => {
    user.username = '';
    user.usernamecode = '';
    user.password = '';
    user.firstName = '';
    user.lastName = '';
    user.neckname = '';
    user.mail = '';
    user.phoneNumber = '';
    user.internal_contact_number = ''; // ฟิลด์ใหม่
    user.BranchDepartment = '03';
    user.jobposition = '03';
    user.Branch = '02';
    user.level = '02';
    user.LINEID = '';
    errorMessage.value = null; // รีเซ็ต error message ด้วย
};
</script>

<style scoped>
/* สไตล์ตามที่ต้องการ */
.container-xl {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}
form div {
    margin-bottom: 10px;
}
label {
    display: block;
    margin-bottom: 5px;
}
input, select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}
button {
    margin-top: 20px;
}
</style>

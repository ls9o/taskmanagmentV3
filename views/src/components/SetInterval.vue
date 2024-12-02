<template>
    <div class="SetInterval">
        วันที่ :{{ formattedDate }} {{ formattedTime }} | เวอร์ชัน : 0000
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';

const currentTime = ref(new Date());

// ฟังก์ชันที่ใช้แปลงเวลาให้เป็นรูปแบบของเวลาไทย
const formatThaiTime = (date: Date) => {
    const options: Intl.DateTimeFormatOptions = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // ใช้เวลาแบบ 24 ชั่วโมง
        timeZone: 'Asia/Bangkok',
    };
    return date.toLocaleTimeString('th-TH', options);
};

// ฟังก์ชันที่ใช้แปลงวันที่เป็น ปี-เดือน-วัน (ค.ศ.)
const formatThaiDate = (date: Date) => {
    const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'Asia/Bangkok',
    };
    return date.toLocaleDateString('en-CA', options); // รูปแบบ: YYYY-MM-DD (ค.ศ.)
};

// สร้างตัวแปรสำหรับเก็บเวลาที่ถูกฟอร์แมตแล้ว
const formattedTime = ref(formatThaiTime(currentTime.value));
const formattedDate = ref(formatThaiDate(currentTime.value));

// ฟังก์ชันสำหรับอัปเดตเวลาและวันที่
const updateTime = () => {
    currentTime.value = new Date();
    formattedTime.value = formatThaiTime(currentTime.value);
    formattedDate.value = formatThaiDate(currentTime.value);
};

// ใช้ number แทน Number
let intervalId: number | null = null;

onMounted(() => {
    // เริ่มการอัปเดตเวลาและวันที่ในทุก ๆ วินาที
    intervalId = window.setInterval(updateTime, 1000);
});

onUnmounted(() => {
    // ยกเลิกการอัปเดตเวลาเมื่อคอมโพเนนต์ถูกทำลาย
    if (intervalId !== null) clearInterval(intervalId);
});
</script>

<style scoped>

</style>

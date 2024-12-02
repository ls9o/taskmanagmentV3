<template>
    <header class="header-container d-flex justify-content-between align-items-center">
        <div class="menu-container d-flex justify-content-center flex-grow-1">
            <nav>
                <ul class="navbar-nav d-flex flex-row">
                    <li v-for="(button, index) in activeButtonList" :key="index" class="nav-item">
                        <button @click="handleClick(button.path)"
                            :class="{ 'font-weight-bold': button.key === 'Change-phone' && isChangephoneButton, }"
                            :disabled="(isChangephoneButton && button.key !== 'Change-phone') || isDisabled(button.key)">
                            {{ button.label }}
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    </header>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, computed } from "vue";
import { useRoute } from 'vue-router';

const emit = defineEmits<{
    (event: "navigate", path: string): void;
}>();

const route = useRoute();
const props = defineProps<{
    status: string;
    isChangephoneVisible: boolean;
}>();

const buttonListUser = [
    { path: "/back", label: "ย้อนกลับ", key: "back" },
    { path: "/Change-phone", label: "เปลี่ยนเบอร์มือถือ", key: "Change-phone" },
    { path: "/unlock", label: "ปลดล็อก/ปลดบล็อก", key: "unlock" },
    { path: "/Cancel-service", label: "ยกเลิกบริการ", key: "Cancel-service" },
    { path: "/documents", label: "ส่งเอกสารอัตโนมัติ", key: "documents" },
];

const buttonListEmployee = [
    { path: "/back", label: "ย้อนกลับ", key: "back" },
    { path: "/edit", label: "แก้ไขข้อมูลพนักงาน", key: "edit" },
    { path: "/delete", label: "ลบสิทธิ์การใช้งาน", key: "delete" },
];
const buttonListEmployee2 = [
    { path: "/add", label: "เพิ่มสิทธิ์การทำงาน", key: "add" },
    { path: "/delete", label: "ลบสิทธิ์การทำงาน", key: "delete" },
];

const handleClick = (path: string) => {
    emit("navigate", path);
};

const isChangephoneButton = computed(() => props.isChangephoneVisible);

const isDisabled = (buttonKey: string) => {
    const status = props.status;

    if (status === "ยกเลิกใช้งาน") {
        return buttonKey !== "back";
    } else if (status === "ล็อก") {
        return buttonKey !== "back" && buttonKey !== "unlock";
    }
    return false;
};

const activeButtonList = computed(() => {
    if (route.path.startsWith('/employee') && route.query.status === 'add') {
        return buttonListEmployee2;
    } else 
    if (route.path.startsWith('/employee')) {
        return buttonListEmployee;
    } else if (route.path.startsWith('/user')) {
        return buttonListUser;
    }
    return [];
});
</script>

<style scoped>
.header-container {
    z-index: 0;
}

</style>

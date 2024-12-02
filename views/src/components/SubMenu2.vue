<template>
    <header class="header-container d-flex justify-content-between align-items-center">
        <div class="menu-container d-flex justify-content-center flex-grow-1" >
            <nav :style="{ marginRight: isCollapsed ? '-15%' : '-35%' }">
                <ul class="navbar-nav d-flex flex-row">
                    <li v-for="(button, index) in buttonList" :key="index" class="nav-item">
                        <button @click="handleClick(button.path)" :class="{
                            'font-weight-bold': button.key === 'Change-phone' && isChangephoneButton,
                        }" :disabled="(isChangephoneButton && button.key !== 'Change-phone') || isDisabled(button.key)">
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

const emit = defineEmits<{
    (event: "navigate", path: string): void;
}>();

const props = defineProps<{
    isCollapsed : boolean
}>();

const buttonList = [
    { path: "/add", label: "เพิ่มสิทธิ์การทำงาน", key: "add" },
    { path: "/delete", label: "ลบสิทธิ์การทำงาน", key: "delete" },
];

const handleClick = (path: string) => {
    emit("navigate", path);
};

const isChangephoneButton = "";

const isDisabled = (buttonKey: string) => {
    return false;
};
</script>

<style lang="scss" scoped>
.header-container {
//     height: 50px;
//     width: 100%;
    position: absolute; 
//     top: 0; 
//     border-bottom: 1px solid #dee2e6;
//     color: #194a94;
//     background-color: #ffffff;
    z-index: 0;

//     .menu-container {
//         display: flex;
//         justify-content: center;
//         flex-grow: 1;
    }

//     nav {
//         ul {
//             list-style: none;
//             padding: 0;
//             margin: 0;
//             display: flex;
//             gap: 10px;
            
//             li{
//                 border-bottom: none;
//             }
//         }
//     }

//     .nav-item {
//         button {
//             border: none;
//             background: transparent;
//             cursor: pointer;
//             position: relative;
//             transition: color 0.3s ease;
//             background-color: transparent;
//         }
//     }
// }

// .font-weight-bold {
//     font-weight: bold;
// }
</style>

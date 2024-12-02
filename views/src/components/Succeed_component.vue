<template>
    <div class="message-box">
        <span class="message ">{{ message }}</span>
        <button @click="closeMessage" class="close-btn">
            <i class="pi pi-times"></i>
        </button>
    </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps<{ message: string }>();

const emit = defineEmits<{
    (event: 'close'): void;
}>();

const closeMessage = () => {
    emit('close');
};
</script>

<style scoped lang="scss">
@import "~bootstrap/scss/bootstrap";

.message {

    padding-left: 1rem;
}


.message-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    margin-left: 1rem;
    margin-right: 1rem;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    background-color: #00cfd1 !important;
    color: white !important;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
}
</style>
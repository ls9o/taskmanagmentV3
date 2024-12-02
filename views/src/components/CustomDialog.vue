<template>
    <div v-if="visible" class="custom-dialog-overlay">
        <div class="custom-dialog-content">
            <div class="custom-dialog-header">
                <h3 class="header">ปลดล็อก/ปลดบล็อก</h3>
                <button class="custom-dialog-close" @click="closeDialog">
                    <i class="pi pi-times"></i>
                </button>
            </div>
            <div class="custom-dialog-body">
                <p>ยืนยันปลดล็อก/ปลดบล็อก?</p>
            </div>
            <div class="custom-dialog-footer">
                <button class="custom-button confirm" @click="confirm">ยืนยัน</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, defineProps, defineEmits } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
const store = useStore();
const route = useRoute();

const props = defineProps<{
    visible: boolean;
}>();
const emit = defineEmits(['update:visible', 'confirm']);

const closeDialog = () => {
    emit('confirm', 'close');
};
const confirm = () => {
    emit('confirm', "unlock");
};

onMounted(() => {
    const id = Number(route.params.id);

    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'ตั้งค่า', path: '/Options', icon: 'pi pi-cog' },
        { name: 'รายละเอียด', path: '/user/' + id, icon: '' },
        { name: 'ปลดล็อก/ปลดบล็อก', path: '/user/' + id, icon: '' },
    ]);


});
</script>

<style scoped lang="scss">
// .header {
//     position: absolute;
//     top: 2rem;
// }

.custom-dialog-overlay {
z-index: 2;
}

</style>

<template>
    <div v-if="visible" class="custom-dialog-overlay">
        <div class="custom-dialog-content">
            <div class="custom-dialog-header">
                <h3 class="header">ลบสิทธิ์การทำงาน</h3>
                <button class="custom-dialog-close" @click="closeDialog">
                    <i class="pi pi-times"></i>
                </button>
            </div>
            <div class="custom-dialog-body">
                <p>ระบุเหตุผลในการลบสิทธิ์การใช้งาน</p>
                <textarea class="form-control" id="reasonTextarea" rows="3" v-model="reason"></textarea>
            </div>
            <div class="custom-dialog-footer">
                <button class="custom-button confirm" @click="confirmRemove">Confirm</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { slotsToElements } from 'bootstrap-vue-3/dist/composables';
import { onMounted, defineProps, defineEmits, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
const store = useStore();
const route = useRoute();
const emit = defineEmits(['update:visible', 'confirm']);

const reason = ref(''); // ตัวแปรสำหรับเก็บเหตุผล

const props = defineProps<{
    visible: boolean;
}>();

const closeDialog = () => {
    emit('confirm', 'close');
};

const confirmRemove = () => {
    emit('confirm', "Remove", reason.value, reason.value);
};

onMounted(() => {
    const id = Number(route.params.id);
    const path = route.path
    const basePath = path.split('/').slice(0, 2).join('/');
    if (basePath == '/user') {
        store.dispatch('breadcrumbs/updateBreadcrumbs', [
            { name: 'Home', path: '/', icon: 'pi pi-home' },
            { name: 'ข้อมูลลูกค้า', path: '/Customer', icon: 'pi pi-users' },
            { name: 'รายละเอียด', path: '/employee/' + id, icon: '' },
            { name: 'ยกเลิกบริการ', path: '/employee/' + id, icon: '' },
        ]);
    }
    else if (basePath == '/Options') {
        store.dispatch('breadcrumbs/updateBreadcrumbs', [
            { name: 'Home', path: '/', icon: 'pi pi-home' },
            { name: 'ตั้งค่า', path: '/Options', icon: 'pi pi-cog' },
            { name: 'รายละเอียด', path: '/employee/' + id, icon: '' },
            { name: 'ลบสิทธิ์การใช้งาน', path: '/employee/' + id, icon: '' },
        ]);
    }

});
</script>

<style scoped lang="scss">
.form-control {
    width: 93%;
}

.custom-dialog-body {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>

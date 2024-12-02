<template>
    <div>
        <Button label="จัดการเมนู" icon="pi pi-cog" @click="showMenuDialog" />

        <!-- Dialog สำหรับจัดการเมนู -->
        <Dialog header="จัดการเมนู" :visible="visible" @hide="onHide" modal :closable="false">
            <div class="dialog-content">
                <!-- ชื่อเมนู -->
                <div class="field">
                    <FloatLabel>
                        <InputText id="menuName" v-model="menuName" />
                        <label for="menuName">ชื่อเมนู</label>
                    </FloatLabel>
                </div>
                <div class="field">
                    <FloatLabel>
                        <InputText id="menuUrl" v-model="url" />
                        <label for="menuUrl">Url</label>
                    </FloatLabel>
                </div>

                <!-- เลือกระบบ -->
                <div class="field menu-group">
                    <FloatLabel>
                        <Dropdown v-model="selectedSystem" :options="systems" optionLabel="name" placeholder="เลือกระบบ"
                            class="custom-dropdown" />
                        <label>เลือกระบบ</label>
                    </FloatLabel>
                    <Button label="" :icon="selectedIcon ? selectedIcon.icon : 'pi pi-image'" @click="showIconDialog" />
                </div>

                <!-- Dialog สำหรับเลือกไอคอน -->
                <Dialog header="เลือกไอคอน" :visible="iconDialogVisible" @hide="onIconDialogHide" modal
                    :closable="false">
                    <div class="dialog-content">
                        <div class="icon-grid">
                            <div v-for="(icon, index) in icons" :key="index" class="icon-grid-item" @click="selectIcon(icon)">
                                <div class="icon-container">
                                    <i :class="icon.icon" class="calendar-icon"></i>
                                </div>
                            </div>
                        </div>
                        <div class="field-button">
                            <Button label="Close" icon="pi pi-times" @click="showIconDialog" />
                        </div>
                    </div>
                </Dialog>

                <!-- เมนูย่อย -->
                <div class="field-radios">
                    <h5>เมนูมีเมนูย่อยไหม?</h5>
                    <RadioButton v-model="hasSubmenu" :value="true" label="มีเมนูย่อย" class="mr-2" />มีเมนูย่อย
                    <RadioButton v-model="hasSubmenu" :value="false" label="ไม่มีเมนูย่อย" />ไม่มีเมนูย่อย
                </div>

                <!-- ถ้ามีเมนูย่อย -->
                <div v-if="hasSubmenu">
                    <div v-for="(submenu, index) in submenus" :key="index" class="menu-group">
                        <div class="submenu-item">
                            <FloatLabel>
                                <InputText v-model="submenu.name" placeholder="ชื่อเมนูย่อย" />
                                <label>ชื่อเมนูย่อย</label>
                            </FloatLabel>
                        </div>
                        <div class="submenu-item">
                            <FloatLabel>
                                <InputText v-model="submenu.url" placeholder="Url" />
                                <label>Url</label>
                            </FloatLabel>
                        </div>
                        <div class="submenu-item">
                            <FloatLabel>
                                <Dropdown v-model="submenu.selectedSystem" :options="systems" optionLabel="name"
                                    placeholder="เลือกระบบ" class="custom-dropdown" />
                                <label>เลือกระบบที่ใช้</label>
                            </FloatLabel>
                        </div>
                        <Button label="ลบเมนูย่อย" icon="pi pi-times" class="p-button-danger"
                            @click="removeSubmenu(index)" />
                    </div>
                    <Button label="เพิ่มเมนูย่อย" icon="pi pi-plus" class="p-button-success mt-2" @click="addSubmenu" />
                </div>

                <!-- ปุ่มบันทึก -->
                <div class="field-button d-flex justify-content-between align-items-center">
                    <Button label="บันทึก" icon="pi pi-check" @click="saveMenu" />
                    <Button label="Close" icon="pi pi-times" @click="onHide" />
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import RadioButton from 'primevue/radiobutton';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import FloatLabel from 'primevue/floatlabel';

interface Icon {
    name: string;
    icon: string;
}

const visible = ref(false); // สถานะ Dialog สำหรับจัดการเมนู
const iconDialogVisible = ref(false); // สถานะ Dialog สำหรับเลือกไอคอน
const menuName = ref('');
const url = ref('');

const hasSubmenu = ref(false);
const submenus = ref<{ name: string; url: string; selectedSystem?: string | undefined }[]>([]);
const systems = [
    { name: 'ระบบ 1', value: 'system1' },
    { name: 'ระบบ 2', value: 'system2' },
];

// กำหนดไอคอน
const icons: Icon[] = [
    { name: 'Home', icon: 'pi pi-home' },
    { name: 'Settings', icon: 'pi pi-cog' },
    { name: 'User', icon: 'pi pi-user' },
    { name: 'Calendar', icon: 'pi pi-calendar' },
    { name: 'Chart', icon: 'pi pi-chart-line' },
    { name: 'Cloud', icon: 'pi pi-cloud' },
    { name: 'Search', icon: 'pi pi-search' },
    { name: 'Envelope', icon: 'pi pi-envelope' },
    { name: 'Bell', icon: 'pi pi-bell' },
];

const selectedSystem = ref<string | undefined>(undefined);
const selectedIcon = ref<Icon | null>(null); // ไอคอนที่เลือก

const selectIcon = (icon: Icon) => {
    selectedIcon.value = icon; // เก็บไอคอนที่เลือก
    iconDialogVisible.value = false; // ปิด Dialog หลังเลือกไอคอน
};

const showIconDialog = () => {
    iconDialogVisible.value = !iconDialogVisible.value; // เปิด Dialog
};

const showMenuDialog = () => {
    visible.value = true; // เปิด Dialog สำหรับจัดการเมนู
};

const addSubmenu = () => {
    submenus.value.push({ name: '', url: '', selectedSystem: undefined });
};

const removeSubmenu = (index: number) => {
    submenus.value.splice(index, 1);
};

const saveMenu = () => {
    console.log({
        menuName: menuName.value,
        url: url.value,
        hasSubmenu: hasSubmenu.value,
        submenus: submenus.value,
        selectedSystem: selectedSystem.value,
        selectedIcon: selectedIcon.value,
    });
};

const onHide = () => {
    visible.value = false; // ปิด Dialog เมนู
};

const onIconDialogHide = () => {
    iconDialogVisible.value = false; // ปิด Dialog เลือกไอคอน
};
</script>

<style scoped>
.dialog-content {
    padding: 1rem;
}

.field {
    margin-bottom: 1.5rem;
}

.field-radios {
    align-items: center;
    margin-bottom: 1.5rem;
}

.menu-group {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.submenu-item {
    flex: 1;
}

.field-button {
    margin-top: 2rem;
    text-align: right;
}

.icon-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    /* ระยะห่างระหว่างไอคอน */
}

.icon-grid-item {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.icon-grid-item:hover {
    background-color: #f0f0f0;
    /* สีพื้นหลังเมื่อโฮเวอร์ */
}

.icon-container {
    font-size: 2rem;
    /* ขนาดไอคอน */
}

.field-button .p-button-danger {
    margin-left: 10px;
    /* ระยะห่าง */
}
</style>

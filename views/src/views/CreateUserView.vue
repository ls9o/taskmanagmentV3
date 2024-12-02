<template>
    <div class="tabs-container">
        <nav>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">
                <button @click="showComponent('createUser')" :class="{ 'active': activeComponent === 'createUser' }"
                    class="nav-link" id="nav-createUser-tab" data-bs-toggle="tab" data-bs-target="#nav-createUser"
                    type="button" role="tab" aria-controls="nav-createUser" aria-selected="true">
                    Create User
                </button>
                <button @click="showComponent('listUser')" :class="{ 'active': activeComponent === 'listUser' }"
                    class="nav-link" id="nav-listUser-tab" data-bs-toggle="tab" data-bs-target="#nav-listUser"
                    type="button" role="tab" aria-controls="nav-listUser" aria-selected="false">
                    List User
                </button>
            </div>
        </nav>

        <div class="tab-content">
            <CreateUser v-if="activeComponent === 'createUser'" />
            <list-user v-if="activeComponent === 'listUser'" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import CreateUser from '../components/CreateUser.vue'
import ListUser from '../components/ListUser.vue';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const activeComponent = ref('createUser');
onMounted(async () => {
    updateBreadcrumbs();
});

function showComponent(component) {
    activeComponent.value = component;
}

const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'Create User & List User', path: '/Options', icon: 'pi pi-user' },
    ]);
};
</script>

<style lang="scss" scoped>
.tabs {
    display: flex;
    border-bottom: 2px solid #ccc;
}

.tabs button {
    background-color: transparent;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tabs button.active {
    border-bottom: 2px solid #007bff;
    color: #007bff;
}

.tabs button:hover {
    color: #0056b3;
}

.tab-content {
    padding: 20px;
    // border: 1px solid #ccc;
}

.nav-link {
    background-color: rgb(233, 233, 233);
    color: rgb(0, 0, 0);
    border-bottom-color: rgb(222, 226, 230);
}

.nav-link.active {
    background-color: rgb(245, 246, 250);
    color: rgb(0, 0, 0);
    border-bottom-color: rgb(245, 246, 250);
}
</style>
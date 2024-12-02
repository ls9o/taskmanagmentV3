<template>
    <div class="tabs-container">
        <nav>
            <div class="nav nav-tabs" id="nav-tab" role="tablist">
                <button @click="showComponent('createTeam')" :class="{ 'active': activeComponent === 'createTeam' }"
                    class="nav-link" id="nav-createTeam-tab" data-bs-toggle="tab" data-bs-target="#nav-createTeam"
                    type="button" role="tab" aria-controls="nav-createTeam" aria-selected="true">
                    Create Team
                </button>
                <button @click="showComponent('listTeam')" :class="{ 'active': activeComponent === 'listTeam' }"
                    class="nav-link" id="nav-listTeam-tab" data-bs-toggle="tab" data-bs-target="#nav-listTeam"
                    type="button" role="tab" aria-controls="nav-listTeam" aria-selected="false">
                    List Team
                </button>
            </div>
        </nav>

        <div class="tab-content">
            <CreateTeam v-if="activeComponent === 'createTeam'" />
            <ListTeam v-if="activeComponent === 'listTeam'" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import CreateTeam from '../components/CreateTeam.vue'
import ListTeam from '../components/ListTeam.vue';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const activeComponent = ref('createTeam');

function showComponent(component: string) {
    activeComponent.value = component;
}

onMounted(async () => {
    updateBreadcrumbs();
});

const updateBreadcrumbs = () => {
    store.dispatch('breadcrumbs/updateBreadcrumbs', [
        { name: 'Home', path: '/', icon: 'pi pi-home' },
        { name: 'Create Team & List Team', path: '/Options', icon: 'pi pi-users' },
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
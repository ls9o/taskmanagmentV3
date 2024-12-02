<template>
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li v-for="(breadcrumb, index) in breadcrumbs" :key="index" class="breadcrumb-item"
                :class="{ active: index === breadcrumbs.length - 1 }">
                <span v-if="breadcrumb.icon" class="breadcrumb-icon">
                    <i :class="breadcrumb.icon"></i>
                </span>
                <!-- <router-link v-if="index !== breadcrumbs.length - 1" :to="breadcrumb.path" @click="handleClick(breadcrumb.path)"> -->
                    <router-link v-if="index !== breadcrumbs.length - 1" :to="{ path: breadcrumb.path, query: { reload: Date.now() } }" @click="handleClick(breadcrumb.path)">

                    {{ breadcrumb.name }}
                </router-link>
                <span v-else>{{ breadcrumb.name }}</span>
            </li>
        </ol>
    </nav>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

// ใช้ getter จาก Vuex store
const breadcrumbs = computed(() => store.getters['breadcrumbs/breadcrumbs']);

function handleClick(path: string) {
    store.dispatch('removeToPath', path);
}
</script>

<style lang="scss" scoped>
.breadcrumb{
    background-color: #f5f6fa;
    margin-bottom: 0;
    padding-left:20px ;
}
</style>

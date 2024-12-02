<template>
  <div class="page-layout-search">
    <div :class="['resizable-container', { 'collapsed': isCollapsed }]">
      <div v-if="!isCollapsed" class="content">
        <div class="form-group">
          <!-- ใช้ head ใน label หากมีอยู่ -->
          <label for="textInput">{{ options[options.length - 1]?.head || 'ค้นหา' }}</label>
          <input type="text" id="textInput" v-model="textInput" class="form-control" />
        </div>
        <div v-for="(optionGroup, index) in options.slice(0, options.length - 1)" :key="index" class="form-group">
          <label :for="'selectInput' + index">{{ optionGroup.label }}</label>
          <select :id="'selectInput' + index" v-model="selectedOptions[index]" class="form-control">
            <option value="" disabled>---เลือก{{ optionGroup.label }}---</option>
            <option v-for="option in optionGroup.options" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
        <button type="button" class="btn btn-primary" @click="triggerSearch">ค้นหา</button>
      </div>
      <button class="btn btn-toggle" @click="toggleCollapse">
        <i :class="isCollapsed ? 'pi pi-plus' : 'pi pi-minus'"></i>
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineEmits, defineProps } from 'vue';

const props = defineProps<{
  options: Array<{ 
    head?: string; 
    label: string; 
    show?: string; 
    options: { value: string; text: string }[]; 
  }>;
  isCollapsed: boolean;
}>();

const emit = defineEmits<{
  (e: 'search', params: any): void;
  (e: 'toggleCollapse', collapsed: boolean): void;
}>()

const textInput = ref('');
const selectedOptions = ref<string[]>([]);

function toggleCollapse() {
  emit('toggleCollapse', !props.isCollapsed);
}

function triggerSearch() {
  const searchParams = {
    textInput: textInput.value,
    selectedOptions: selectedOptions.value,
  };
  emit('search', searchParams);
}

watch(
  () => props.options,
  (newOptions) => {
    if (newOptions.length > 0) {
      selectedOptions.value = newOptions.slice(0, newOptions.length - 1).map(optionGroup => optionGroup.options[0]?.value || '');
    }
  },
  { immediate: true }
);
</script>

<style lang="scss" scoped>
/* คุณสามารถใส่สไตล์ที่นี่ได้ */
</style>

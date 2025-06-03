<!-- MultiSelectDropdown.vue -->
<template>
  <div class="dropdown-container">
    <!-- Dropdown Header -->
    <div class="dropdown-header" @click="toggleDropdown" :class="isOpen ? 'active' : ''">
      <div class="dropdown-selected typography-caption-lg-regular">
        <div v-if="selectedOptions.length" class="selected-options">
          <div class="option-chip typography-caption-lg-medium" v-for="(option, index) in selectedOptions" :key="index">
            {{ option }}
            <span class="option-chip-remove flex flex-center" @click.stop="removeOption(option)">
              <SvgIcon name="close-circle-fill" state="black" size="16" />
            </span>
          </div>
        </div>
        <span v-else>{{ placeholder }}</span>
      </div>
      <SvgIcon
        class="dropdown-icon"
        name="arrow-left"
        state="black"
        size="16"
        cursor="true"
        :class="{ 'dropdown-icon-open': isOpen }"
      />
    </div>

    <!-- Dropdown Menu -->
    <div class="dropdown-menu" v-if="isOpen">
      <div
        v-for="(option, index) in options"
        :key="index"
        class="dropdown-option typography-caption-lg-regular"
        :class="{
          'dropdown-option-selected': isOptionSelected(option),
          'dropdown-option-highlighted': option === highlightedOption
        }"
        @click.stop="toggleOption(option)"
      >
        <div class="option-content">
          <div v-if="showCheckbox" class="checkbox" :class="{ 'checkbox-selected': isOptionSelected(option) }">
            <div v-if="isOptionSelected(option)" class="checkbox-inner"></div>
          </div>
          <span>{{ option }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import SvgIcon from 'src/components/SvgIcon.vue';

const props = defineProps({
  options: {
    type: Array,
    required: true
  },
  modelValue: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'انتخاب کنید'
  },
  showCheckbox: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const selectedOptions = ref([...props.modelValue]);
const highlightedOption = ref(null);

// Watch for changes from parent
watch(() => props.modelValue, (newValue) => {
  selectedOptions.value = [...newValue];
});

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

function isOptionSelected(option) {
  return selectedOptions.value.includes(option);
}

function toggleOption(option) {
  if (isOptionSelected(option)) {
    removeOption(option);
  } else {
    addOption(option);
  }
}

function addOption(option) {
  if (!isOptionSelected(option)) {
    const newSelected = [...selectedOptions.value, option];
    selectedOptions.value = newSelected;
    emit('update:modelValue', newSelected);
  }
}

function removeOption(option) {
  const newSelected = selectedOptions.value.filter(item => item !== option);
  selectedOptions.value = newSelected;
  emit('update:modelValue', newSelected);
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  const dropdown = event.target.closest('.dropdown-container');
  if (!dropdown) {
    isOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.dropdown-container {
  position: relative;
  width: 100%;
}

.dropdown-header {
  background-color: var(--white-light-active, #F8F8F8);
  padding: 0.75rem 1rem; /* 12px 16px */
  border-radius: 0.5rem; /* 8px */
  min-height: 2.75rem; /* 44px */
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(130, 130, 130, 1);
  margin-bottom: 0.125rem; /* 2px */
}

.dropdown-header.active {
  background-color: white;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border: 1px solid var(--orange-primary);
}

.dropdown-icon {
  transform: rotate(270deg);
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.dropdown-icon-open {
  transform: rotate(90deg);
}

.dropdown-menu {
  position: static;
  top: calc(100% + 0.125rem); /* 2px */
  left: 0;
  right: 0;
  background: #FFFFFF;
  border-bottom-right-radius: 0.5rem;
  border-bottom-left-radius: 0.5rem;
  box-shadow: 0 0.25rem 1.125rem 0 rgba(47, 43, 61, 0.16); /* 4px 18px */
  z-index: 100;
  overflow-y: auto;
  padding: 0.5rem; /* 8px */
}

.dropdown-menu > * {
  margin-bottom: 0.125rem; /* 2px */
}

.dropdown-option {
  padding: 0.6875rem 1.25rem; /* 11px 20px */
  cursor: pointer;
  border-radius: 0.5rem; /* 8px */
  text-align: right;
  color: rgba(47, 43, 61, 0.9);
}

.dropdown-option-selected {
  background-color: rgba(255, 239, 229, 1);
  color: var(--orange-primary);
}

.dropdown-option-highlighted {
  background-color: rgba(255, 239, 229, 1);
  color: red;
}

.option-content {
  display: flex;
  align-items: center;
  direction: rtl;
}

.checkbox {
  width: 1rem; /* 16px */
  height: 1rem;
  border-radius: 50%;
  border: 1px solid #BDBDBD;
  margin-left: 0.5rem; /* 8px */
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-selected {
  border-color: var(--orange-primary);
}

.checkbox-inner {
  width: 0.5rem; /* 8px */
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--orange-primary);
}

.selected-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3125rem; /* 5px */
}

.option-chip {
  background-color: rgba(233, 241, 251, 1);
  color: var(--blue-custom);
  padding: 0.125rem 0.625rem; /* 2px 10px */
  border-radius: 0.25rem; /* 4px */
  display: flex;
  align-items: center;
}

.option-chip-remove {
  margin-right: 0.3125rem; /* 5px */
  font-size: 0.875rem; /* 14px */
  cursor: pointer;
}

.dropdown-selected {
  overflow: hidden;
  flex-grow: 1;
  display: flex;
  align-items: center;
}
</style>


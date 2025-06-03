<template>
  <div class="dropdown-container">
    <!-- Header -->
    <div class="dropdown-header" @click="toggleDropdown" :class="{ active: isOpen }">
      <div class="dropdown-selected typography-caption-lg-regular">
        <div v-if="isArrayModel && modelValue.length" class="selected-options">
          <div
            class="option-chip typography-caption-lg-medium"
            v-for="(option, index) in modelValue"
            :key="index"
          >
            {{ getLabel(option) }}
            <span class="option-chip-remove flex flex-center" @click.stop="removeOption(option)">
              <SvgIcon name="close-circle-fill" state="black" size="16" />
            </span>
          </div>
        </div>
        <div v-else-if="!isArrayModel && modelValue">
          {{ getLabel(modelValue) }}
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

    <!-- Options -->
    <div class="dropdown-menu" v-if="isOpen">
      <div
        v-for="(option, index) in options"
        :key="index"
        class="dropdown-option typography-caption-lg-regular"
        :class="{
          'dropdown-option-selected': isOptionSelected(option),
          'dropdown-option-highlighted': option.value === highlightedOption
        }"
        @click.stop="toggleOption(option)"
      >
        <div class="option-content">
          <div v-if="isArrayModel" class="checkbox" :class="{ 'checkbox-selected': isOptionSelected(option) }">
            <div v-if="isOptionSelected(option)" class="checkbox-inner"></div>
          </div>
          <span>{{ option.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import SvgIcon from 'src/components/SvgIcon.vue'

const props = defineProps({
  options: {
    type: Array,
    required: true // [{label, value}]
  },
  modelValue: {
    type: [String, Number, Array],
    default: ''
  },
  placeholder: {
    type: String,
    default: 'انتخاب کنید'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const highlightedOption = ref(null)

const isArrayModel = computed(() => Array.isArray(props.modelValue))

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function isOptionSelected(option) {
  return isArrayModel.value
    ? props.modelValue.includes(option.value)
    : props.modelValue === option.value
}

function toggleOption(option) {
  if (isArrayModel.value) {
    if (isOptionSelected(option)) {
      removeOption(option)
    } else {
      addOption(option)
    }
  } else {
    emit('update:modelValue', option.value)
    isOpen.value = false
  }
}

function addOption(option) {
  const newValue = [...props.modelValue, option.value]
  emit('update:modelValue', newValue)
}

function removeOption(option) {
  const newValue = props.modelValue.filter(val => val !== option.value)
  emit('update:modelValue', newValue)
}

function getLabel(value) {
  const found = props.options.find(opt => opt.value === value)
  return found?.label ?? value
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  const dropdown = event.target.closest('.dropdown-container')
  if (!dropdown) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dropdown-container {
  position: relative;
  width: 100%;
}

.dropdown-header {
  background-color: var(--white-light-active, #F8F8F8);
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  min-height: 2.75rem;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(130, 130, 130, 1);
  margin-bottom: 0.125rem;
  border: 1px solid transparent;
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
  background: #ffffff;
  border-bottom-right-radius: 0.5rem;
  border-bottom-left-radius: 0.5rem;
  box-shadow: 0 0.25rem 1.125rem 0 rgba(47, 43, 61, 0.16);
  z-index: 100;
  overflow-y: auto;
  padding: 0.5rem;
}

.dropdown-option {
  padding: 0.6875rem 1.25rem;
  cursor: pointer;
  border-radius: 0.5rem;
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
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  border: 1px solid #BDBDBD;
  margin-left: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-selected {
  border-color: var(--orange-primary);
}

.checkbox-inner {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--orange-primary);
}

.selected-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3125rem;
}

.option-chip {
  background-color: rgba(233, 241, 251, 1);
  color: var(--blue-custom);
  padding: 0.125rem 0.625rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
}

.option-chip-remove {
  margin-right: 0.3125rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.dropdown-selected {
  overflow: hidden;
  flex-grow: 1;
  display: flex;
  align-items: center;
}
</style>

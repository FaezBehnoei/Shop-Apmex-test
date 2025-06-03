<template>
  <div class="input-container">
    <div class="input-wrapper">
      <!-- Regular Input -->
      <input
        v-if="type === 'input'"
        type="text"
        class="form-input"
        v-model="internalValue"
        :id="inputId"
        ref="inputRef"
        @keydown.enter.prevent="focusNext"
        readonly
      />

      <!-- Custom Dropdown -->
      <div v-if="type === 'select'" class="dropdown-field">
        <div class="form-input dropdown-header" @click="isOpen = !isOpen">
          <span class="dropdown-placeholder">
            {{ value || placeholder }}
          </span>
          <SvgIcon
            class="dropdown-icon"
            name="arrow-left"
            state="black"
            size="16"
            cursor="true"
            :class="{ 'dropdown-icon-open': isOpen }"
          />
        </div>

        <div v-if="isOpen" class="dropdown-wrapper">
          <ul>
            <li
              v-for="option in options"
              :key="option"
              class="items-list typography-caption-lg-regular"
              @click="$emit('update:value', option); isOpen = false"
            >
              {{ option }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Floating Label -->
      <label :for="inputId" class="floating-label text-white-dark-hover typography-caption-lg-regular">{{ label }}</label>

      <!-- Edit Icon -->
      <button class="icon-btn" @click="openEditDialog(label)">
        <SvgIcon
        v-if="icon"
        class="edit-icon"
        name="edit-profile"
        state="colored"
        size="24"

      /></button>
    </div>
  </div>
    <EditDialogProfile
      v-model="showEditDialog"
      v-bind="dialogData"
      @updated="handleDialogUpdate"
    />

</template>

<script setup>
import { ref, watch } from 'vue'
import SvgIcon from '../SvgIcon.vue'
import EditDialogProfile from './editDialogProfile.vue';
import { englishToPersian } from 'src/composable/useNumberUtils';


const props = defineProps({
  type: {
    type: String,
    default: 'input', // 'input' or 'select'
    validator: value => ['input', 'select'].includes(value)
  },
  label: {
    type: String,
    default: 'نام و نام خانوادگی'
  },
  value: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'پریناز قاسمی پور'
  },
  inputId: {
    type: String,
    default: () => 'input-' + Math.random().toString(36).substr(2, 9)
  },
  options: {
    type: Array,
    default: () => []
  },
  icon: Boolean,
  modelValue: String,
})

const emit = defineEmits(['update:modelValue', 'focus-next','updated'])

function focusNext() {
  emit('focus-next')
}
function handleDialogUpdate() {
  emit('updated') // 👈 پاس بده به صفحه اصلی
}

const isOpen = ref(false)
const showEditDialog = ref(false)
const dialogData = ref({
  title: '',
  description: '',
  placeholder: '',
  inputType: '',
  submitLabel: ''
})

function openEditDialog(type) {
  if (type === 'شماره همراه') {
    dialogData.value = {
      title: 'تغییر شماره همراه',
      description: 'برای تغییر شماره همراه درخواست خود را ثبت کنید',
      placeholder: 'شماره همراه',
      inputType: 'tel',
      submitLabel: 'ثبت درخواست',
      field: 'phone_number'
    }
  } else if (type === 'رمز عبور') {
    dialogData.value = {
      title: 'تغییر رمز عبور',
      description: 'برای تغییر رمز عبور درخواست خود را ثبت کنید',
      placeholder: 'رمز عبور',
      inputType: 'password',
      submitLabel: 'ثبت رمز',
      field: 'password'
    }
  }
  showEditDialog.value = true
}


const internalValue = ref(props.modelValue)

watch(() => props.modelValue, val => internalValue.value = val)
watch(internalValue, val => emit('update:modelValue', englishToPersian(val)))

</script>

<style scoped>
.input-container {
  width: 100%;
}

.input-wrapper {
  position: relative;
  margin: 2rem 0;
}

.form-input {
  width: 100%;
  padding: 0.75rem 0.5rem 0.75rem 0.5rem; /* فضا برای آیکون چپ */
  border: 1px solid var(--white-normal);
  border-radius: 0.5rem;
  transition: border-color 0.2s ease;
  outline: none;
  background-color: white;
  box-sizing: border-box;
  font-size: 0.875rem;
  font-family: inherit;
}

.form-input::placeholder {
  color: var(--white-dark-active);
  font-weight: 500;
  font-size: 0.875rem;
}

.floating-label {
  position: absolute;
  top: -8px;
  right: 0px;
  background-color: #fff;
  padding: 0 6px;
  pointer-events: none;
  transition: all 0.2s ease;
}

/* .form-input:focus + .floating-label {
  color: #007bff;
} */

.form-input:not(:placeholder-shown) + .floating-label {
  top: -8px;
  font-size: 12px;
}

.edit-icon {
  position: absolute;
  top: 50%;
  left: 0.5rem;
  transform: translateY(-50%);
}

/* Dropdown */
.dropdown-field {
  position: relative;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.dropdown-placeholder {
  color: #333;
  font-size: 0.875rem;
}

.dropdown-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%) rotate(270deg);
  transition: transform 0.2s ease;
}

.dropdown-icon-open {
  transform: translateY(-50%) rotate(90deg);
}

.dropdown-wrapper {
  position: absolute;
  top: 100%;
  right: 0;
  left: 0;
  background-color: #fff;
  border-radius: 0.5rem;
  padding: 0.5rem;
  box-shadow: 0 4px 18px rgba(47, 43, 61, 0.16);
  z-index: 10;
  margin-top: 4px;
  overflow-y: auto;
}


.items-list {
  padding: 2px 5px;
  margin-bottom: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.items-list:hover {
  background-color: #f2f2f2;
}
.icon-btn{
  display: block;
  outline: none;
  border: none;
  background-color: none;
}
</style>

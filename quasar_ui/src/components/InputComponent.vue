<template>
  <div
    dir="rtl"
    :class="[
      'my-input-wrapper',
      { 'is-error': isError, 'is-disable': disable },
      customClass,
      `my-input-wrapper-${size}`,
    ]"
  >
    <label v-if="label" class="my-input-label">{{ label }}</label>
    <div class="my-input-container">
      <input
        v-num-fa
        :type="type"
        :placeholder="placeholder"
        :disabled="disable"
        :readonly="readonly"
        :value="modelValue"
        @focus="handleFocus"
        @blur="validateOnBlur"
        @input="handleInput"
        :class="['my-input', {'hightLight-border' : highlight}, {'direction-ltr' : direction}]"
        ref="inputRef"
      />
      <SvgIcon
        v-if="icon"
        :name="icon"
        :state="state"
        :size="Iconsize"
        :custom-class-icon="customClassIcon"
        @pointerdown.prevent="handleClickIcon"
        class="my-input-icon"
      />
    </div>
    <p v-if="validationMessage && isError" class="my-input-error">
      {{ validationMessage }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import SvgIcon from './SvgIcon.vue'
import { validate } from '../utils/rules'

const props = defineProps({
  modelValue: String, // v-model
  label: String,
  placeholder: String,
  type: { type: String, default: 'text' },
  disable: Boolean,
  readonly: Boolean,
  error: Boolean,
  errorMessage: String,
  customClass: String,
  highlight: Boolean,
  direction: Boolean,
  size: { type: String, default: 'xl' },
  icon: String,
  state: String,
  Iconsize: String,
  customClassIcon: String,
  autoInput: Boolean,
  rules: { type: Array, default: () => [] },
  validateOnInput: { type: Boolean, default: false },
  formValues: { type: Object, default: () => ({}) },
  width: { type: String, default: '100%' }, // اضافه کردن prop برای عرض
})

const emit = defineEmits(['update:modelValue', 'clicked-icon', 'validation'])

const inputRef = ref('')
function focus(){
  inputRef.value?.focus()
}
defineExpose({
  focus
})

onMounted(() => {
  if(props.autoInput){
    inputRef.value?.focus()
  }
})

function handleClickIcon() {
  inputRef.value?.focus()
  emit('clicked-icon')
}

const validationMessage = ref('')
const isDirty = ref(false)
const internalError = ref(false)

const isError = computed(() => {
  return props.error || internalError.value
})

const validateField = () => {
  if (props.rules && props.rules.length) {
    const { valid, message } = validate(
      props.modelValue,
      props.rules,
      props.formValues
    )
    validationMessage.value = message
    internalError.value = !valid
    emit('validation', { valid, message })
    return valid
  }

  internalError.value = false
  validationMessage.value = ''
  return true
}

const handleFocus = () => {
}

const validateOnBlur = () => {
  isDirty.value = true
  validateField()
}

const handleInput = (event) => {
  const value = event.target.value
  emit('update:modelValue', value)

  if (isDirty.value && props.validateOnInput) {
    validateField()
  }
}

watch(
  () => props.errorMessage,
  (newValue) => {
    if (newValue) {
      validationMessage.value = newValue
      internalError.value = true
    } else {
      validateField()
    }
  }
)

watch(
  () => props.modelValue,
  () => {
    if (internalError.value || isDirty.value) {
      validateField()
    }
  }
)

watch(
  () => props.formValues,
  () => {
    if (isDirty.value) {
      validateField()
    }
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
.my-input-wrapper {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0.25rem; // 4px
}

.my-input-wrapper-xl {
  .my-input-label {
    font-weight: 400;
    font-size: 0.875rem; // 14px
    line-height: 1.375rem; // 22px
  }

  :deep(.my-input::placeholder) {
    font-weight: 400;
    font-size: 0.75rem; // 12px
    line-height: 1.125rem; // 18px
  }

  .my-input {
    height: 3rem; // 48px
    padding: 0.9375rem 0.5rem 0.9375rem 1rem;
  }
}

.my-input-wrapper-md {
  .my-input-label {
    font-weight: 400;
    font-size: 0.875rem;
    line-height: 1.375rem;
  }

  :deep(.my-input::placeholder) {
    font-weight: 400;
    font-size: 0.75rem;
    line-height: 1.125rem;
  }

  .my-input {
    height: 2.5rem; // 40px
    padding: 0.6875rem 0.5rem 0.6875rem 1rem;
  }
}

.my-input-wrapper-sm {
  .my-input-label {
    font-weight: 400;
    font-size: 0.75rem;
    line-height: 1.125rem;
  }

  :deep(.my-input::placeholder) {
    font-weight: 400;
    font-size: 0.625rem;
    line-height: 0.875rem;
  }

  .my-input {
    height: 2rem; // 32px
    padding: 0.4375rem 0.5rem 0.4375rem 1rem;
  }
}

.my-input-label {
  color: var(--grey-label);
}

.my-input-container {
  position: relative;
  display: flex;
  align-items: center;

  .my-input {
    width: 100%;
  }

  .my-input-icon {
    position: absolute;
    left: 1rem;
    cursor: pointer;
  }
}

.my-input {
  border-radius: 0.5rem;
  border: none;
  background-color: rgba(241, 241, 241, 1);
  gap: 0.625rem;

  &:hover {
    outline: none;
    border: 1px solid var(--orange-primary);
  }

  &:focus {
    outline: none;
  }
}

.is-error {
  .my-input {
    border: 1px solid red;
    font-weight: 400;
    font-size: 0.875rem;
    line-height: 1.375rem;
    color: var(--q-negative);
  }

  .my-input-error {
    color: rgba(255, 0, 0, 1);
    font-size: 0.75rem;
    margin-bottom: 0.0625rem; // 1px
  }
}

.is-disable {
  opacity: 0.6;
  pointer-events: none;
}

.my-input.hightLight-border {
  border: 1px solid var(--orange-primary);
}

.my-input.direction-ltr {
  text-align: left;
  direction: ltr;
  padding-left: 2.5rem; // 40px
}

@media (max-width: 768px) {
  .my-input-wrapper {
    gap: 0.25rem;
  }

  .my-input-wrapper-xl .my-input {
    height: 3.25rem; // 52px
  }

  .my-input-wrapper-md .my-input {
    height: 2.75rem; // 44px
  }

  .my-input-wrapper-sm .my-input {
    height: 2.25rem; // 36px
  }
}

@media (max-width: 480px) {
  .my-input-wrapper {
    gap: 0.125rem; // 2px
  }

  .my-input-wrapper-xl .my-input {
    height: 3rem;
  }

  .my-input-wrapper-md .my-input {
    height: 2.5rem;
  }

  .my-input-wrapper-sm .my-input {
    height: 2rem;
  }

  .my-input-label {
    font-size: 0.75rem;
  }

  .my-input-wrapper-xl :deep(.my-input::placeholder),
  .my-input-wrapper-md :deep(.my-input::placeholder) {
    font-size: 0.625rem;
  }

  .my-input-wrapper-sm :deep(.my-input::placeholder) {
    font-size: 0.5625rem;
  }
}
</style>


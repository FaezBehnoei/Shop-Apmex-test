<template>
  <div class="new-dropdown-container">
    <!-- Dropdown Header -->
    <div class="new-dropdown-header" @click="toggleDropdown" :class="{ open: isOpen }">
      <span class="typography-body-lg-medium text-black">
        {{ placeholder }}
      </span>
      <SvgIcon
        class="arrow-icon"
        name="arrow-left"
        state="black"
        size="16"
        :class="{ rotated: isOpen }"
      />
    </div>

    <!-- Dropdown List -->
    <div v-if="isOpen" class="new-dropdown-list scrollbar-offset">
      <div
        v-for="(option, index) in options"
        :key="index"
        class="dropdown-item typography-body-md-bold"
        @click.stop="toggleOption(option)"
      >
        <div
          class="check-wrapper"
          :class="{ selected: selectedModel.includes(option) }"
        >
          <SvgIcon
            v-if="selectedModel.includes(option)"
            name="check"
            state="black"
            size="16"
          />
        </div>
        <span class="q-mr-sm">{{ option }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SvgIcon from 'src/components/SvgIcon.vue'

const props = defineProps({
  options: Array,
  modelValue: Array,
  placeholder: String,
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selectedModel = ref([...props.modelValue])

watch(
  () => props.modelValue,
  (val) => {
    selectedModel.value = [...val]
  }
)

watch(selectedModel, (val) => {
  emit('update:modelValue', val)
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const toggleOption = (opt) => {
  const exists = selectedModel.value.includes(opt)
  selectedModel.value = exists
    ? selectedModel.value.filter((o) => o !== opt)
    : [...selectedModel.value, opt]
}
</script>

<style scoped>
.new-dropdown-container {
  width: 100%;
  position: relative;
}

.new-dropdown-header {
  background-color: rgba(247, 247, 247, 1);
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  min-height: 2.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border: 1px solid transparent;
}

.new-dropdown-header.open {
  background-color: rgba(247, 247, 247, 1);
  border-color: var(--orange-primary);
  margin-bottom: 0.4rem;
}

.arrow-icon {
  transition: transform 0.2s ease;
  transform: rotate(270deg);
}

.arrow-icon.rotated {
  transform: rotate(90deg);
}

.new-dropdown-list {
  background: rgba(247, 247, 247, 1);
  border-radius: 0.5rem;
  padding: 0.725rem;
  z-index: 99;
  border: 1px solid rgba(235, 235, 235, 1);
  max-height: 20vh;
  overflow-y: auto;
  scrollbar-width: 1px; /* hide in Firefox for custom */
  position: relative;
}

/* WebKit scrollbar styles (Chrome, Safari, Edge) */
.new-dropdown-list::-webkit-scrollbar {
  width: 6px;
  max-height: 3px !important;
}

.new-dropdown-list::-webkit-scrollbar-track {
  background: #e5e5e5;
  border-radius: 100px;
   margin: 8px 0;
}

.new-dropdown-list::-webkit-scrollbar-thumb {
  background-color: var(--orange-primary);
  border-radius: 999px;
  min-height: 10px;
  height: 10px; /* اگر بخوای همیشه ثابت باشه */
}

/* فاصله از بالا و پایین */
.new-dropdown-list::-webkit-scrollbar-track:vertical {
  margin-top: 8px;
  margin-bottom: 8px;
}



.dropdown-item {
  padding: 0.5rem 0.25rem;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.check-wrapper {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
  background-color: white;
  border: 1px solid black;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
  margin-left: 0.5rem;
}

.check-wrapper.selected {
  background-color: var(--orange-primary);
  border-color: var(--orange-primary);
}
</style>

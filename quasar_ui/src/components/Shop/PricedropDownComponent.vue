<!-- PriceFilterComponent.vue -->
<template>
  <div class="price-filter-container">
    <!-- "از" Field -->
    <div class="field-group q-mb-md">
      <div class="label typography-body-sm-regular text-dark text-right q-mb-xs">از</div>
      <InputComponent
        v-model="from"
        placeholder="۰"
        suffix="تومان"
        class="full-width"
      />
    </div>

    <!-- "تا" Field -->
    <div class="field-group q-mb-md">
      <div class="label typography-body-sm-regular text-dark text-right q-mb-xs">تا</div>
      <InputComponent
        v-model="to"
        placeholder="۰"
        suffix="تومان"
        class="full-width"
      />
    </div>

    <!-- Slider Range -->
    <div class="slider-wrapper q-mt-lg">
      <q-range
        v-model="range"
        :min="minValue"
        :max="maxValue"
        :step="stepValue"
        color="orange"
        track-color="#E5E5E5"
        label-always
        class="price-slider"
      />
      <div class="slider-labels flex justify-between q-mt-sm">
        <span class="typography-caption-md-regular text-black">گران‌ترین</span>
        <span class="typography-caption-md-regular text-black">ارزان‌ترین</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, toRefs } from 'vue'
import InputComponent from 'src/components/InputComponent.vue'

/**
 * Props:
 * - modelValueFrom  : initial "از" price (Number or String)
 * - modelValueTo    : initial "تا" price (Number or String)
 * - modelValueRange : initial slider range as [min, max]
 * - minValue        : minimum slider limit (Number)
 * - maxValue        : maximum slider limit (Number)
 * - stepValue       : slider step (Number)
 */
const props = defineProps({
  modelValueFrom: {
    type: [Number, String],
    default: ''
  },
  modelValueTo: {
    type: [Number, String],
    default: ''
  },
  modelValueRange: {
    type: Array,
    default: () => [0, 1000000000] // Example defaults
  },
  minValue: {
    type: Number,
    default: 0
  },
  maxValue: {
    type: Number,
    default: 1000000000
  },
  stepValue: {
    type: Number,
    default: 1000
  }
})

const emit = defineEmits([
  'update:modelValueFrom',
  'update:modelValueTo',
  'update:modelValueRange'
])

// Local reactive references
const { modelValueFrom, modelValueTo, modelValueRange } = toRefs(props)
const from = ref(modelValueFrom.value)
const to = ref(modelValueTo.value)
const range = ref([...modelValueRange.value])

// Whenever parent updates props, sync local refs
watch(modelValueFrom, val => {
  from.value = val
})
watch(modelValueTo, val => {
  to.value = val
})
watch(modelValueRange, val => {
  range.value = [...val]
})

// Emit changes upstream
watch(from, val => {
  emit('update:modelValueFrom', val)
})
watch(to, val => {
  emit('update:modelValueTo', val)
})
watch(range, val => {
  emit('update:modelValueRange', val)
})
</script>

<style scoped>
.price-filter-container {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: #fff;
}

/* Field group spacing */
.field-group {
  display: flex;
  flex-direction: column;
}

/* Label styling */
.label {
  /* font: 14px medium, dark color */
  color: rgba(47, 43, 61, 1);
}

/* Ensure InputComponent spans full width */
.full-width {
  width: 100%;
}

/* Slider wrapper */
.slider-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* Customize QRange track height lightly */
.price-slider .q-range__track {
  height: 4px;
  border-radius: 4px;
}

/* Customize thumb size */
.price-slider .q-range__thumb {
  width: 18px;
  height: 18px;
  margin-top: -7px; /* center thumb on track */
  background-color: #fff;
  border: 2px solid var(--orange-primary);
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}

/* When thumb is active (dragged), fill with orange */
.price-slider .q-range__thumb--focused {
  background-color: var(--orange-primary);
}

/* Slider labels beneath */
.slider-labels span {
  /* font: 14px regular, dark color */
  color: rgba(47, 43, 61, 1);
}

/* On mobile, make sure scrollable area doesn’t overflow */
.price-filter-container {
  max-height: 80vh;
  overflow-y: auto;
}
</style>

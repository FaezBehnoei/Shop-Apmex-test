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

const props = defineProps({
  modelValueFrom: { type: [Number, String], default: '' },
  modelValueTo: { type: [Number, String], default: '' },
  modelValueRange: { type: Array, default: () => [0, 1000000000] },
  minValue: { type: Number, default: 0 },
  maxValue: { type: Number, default: 1000000000 },
  stepValue: { type: Number, default: 1000 }
})

const emit = defineEmits([
  'update:modelValueFrom',
  'update:modelValueTo',
  'update:modelValueRange'
])

const { modelValueFrom, modelValueTo, modelValueRange } = toRefs(props)
const from = ref(modelValueFrom.value)
const to = ref(modelValueTo.value)
const range = ref([...modelValueRange.value])

watch(modelValueFrom, val => { from.value = val })
watch(modelValueTo, val => { to.value = val })
watch(modelValueRange, val => { range.value = [...val] })

watch(from, val => emit('update:modelValueFrom', val))
watch(to, val => emit('update:modelValueTo', val))
watch(range, val => emit('update:modelValueRange', val))
</script>

<style scoped>
.price-filter-container {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: #fff;
}

.field-group {
  display: flex;
  flex-direction: column;
}

.label {
  color: rgba(47, 43, 61, 1);
}

.full-width {
  width: 100%;
}

.slider-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.price-slider .q-range__track {
  height: 4px;
  border-radius: 4px;
}

.price-slider .q-range__thumb {
  width: 18px;
  height: 18px;
  margin-top: -7px;
  background-color: #fff;
  border: 2px solid var(--orange-primary);
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}

.price-slider .q-range__thumb--focused {
  background-color: var(--orange-primary);
}

.slider-labels span {
  color: rgba(47, 43, 61, 1);
}

.price-filter-container {
  max-height: 80vh;
  overflow-y: auto;
}
</style>

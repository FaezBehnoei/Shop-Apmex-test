<template>
  <div
    class="svg-icon-wrapper"
    :class="[customClassIcon, `svg-icon-${cursor}`]"
    :style="wrapperStyle"
    v-html="svgContent"
    @pointerdown.prevent="$emit('click', $event)"
  />
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  state: { type: String, default: 'black' },
  size: { type: String, default: '24' }, // برحسب px
  customClassIcon: { type: String, default: 'inherit-background' },
  cursor: String
})

const icons = import.meta.glob('/src/assets/icons/*.svg', { as: 'raw' })
const svgContent = ref('')

// فرض: base font-size = 16px → 1rem = 16px
const wrapperStyle = computed(() => {
  const px = parseFloat(props.size)
  const rem = px / 16
  return {
    width: `${rem}rem`,
    height: `${rem}rem`,
  }
})


watchEffect(async () => {
  const filename = `name=${props.name}, state=${props.state}, size=${props.size}px.svg`
  const path = `/src/assets/icons/${filename}`
  const loader = icons[path]

  if (!loader) {
    console.warn(`❌ آیکون پیدا نشد: ${path}`)
    svgContent.value = ''
    return
  }

  svgContent.value = await loader()
})
</script>

<style scoped>
.svg-icon-wrapper {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  color: inherit;
}

.svg-icon-wrapper> svg {
  width: 100%;
  height: 100%;
  display: block;
  color: inherit;
  fill: currentColor;
}
.svg-icon {
  color: inherit;
}
.svg-icon-true {
  cursor: pointer;
}
.inherit-background{
  background-color: transparent;
  color: transparent;
}

</style>

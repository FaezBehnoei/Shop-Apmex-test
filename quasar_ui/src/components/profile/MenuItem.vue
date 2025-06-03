<template>
  <div class="menu-item" @click="onClick">
      <div class="flex justify-between">
        <div class="q-ml-xs">
          <SvgIcon :name="icon" state="colored" size="24" />
          </div>
          <div class="menu-label typography-body-md-medium">
            {{ label }}
          </div>
      </div>
      <div>
        <SvgIcon name="arrow-left-profile" state="colored" size="24"/>
      </div>
  </div>
</template>

<script setup>
import SvgIcon from 'src/components/SvgIcon.vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  label: String,
  icon: String,
  route: String
})
const router = useRouter()

const emit = defineEmits(['click'])

function onClick() {
  emit('click')
  router.push(props.route)
}
</script>

<style scoped>
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 0;
  cursor: pointer;
}

.menu-label {
  color: #1A1A1A;
}
</style>

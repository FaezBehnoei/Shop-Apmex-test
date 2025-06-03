<template>
  <div class="q-px-md flex">
    <!-- title -->
    <p class="margin-title">کدام دارایی را قصد برداشت آن را دارید؟</p>

    <!-- content -->
    <div class="full-width">
      <div class="content-wrapper flex column flex-center">
        <div
          v-for="item in assets"
          :key="item.id"
          class="flex items-center justify-between bg-white-light-active colored-item cursor-pointer"
          :class="active === item.id ? 'colored-items' : ''"
          @click="active = item.id"
        >
          <!-- right side -->
          <div class="flex items-center">
            <div class="flex flex-center q-ml-sm">
              <SvgIcon :name="item.icon" state="black" size="32" />
            </div>
            <div class="typography-caption-lg-regular text-blue-custom q-mr-xs flex column">
              {{ item.name }}
              <span
                v-if="item.pricePerUnit"
                class="typography-caption-md-regular text-white-dark"
              >
                قیمت ۱ گرم: {{ item.pricePerUnit }}
              </span>
            </div>
          </div>

          <!-- left side -->
          <div class="flex q-gutter-x-sm">
            <div class="flex items-center q-gutter-x-xs">
              <span class="typography-caption-lg-regular text-blue-custom">{{ item.amount }}</span>
              <span class="typography-caption-md-regular text-white-dark hover-text-white-dark-hover text-left">{{ item.unit }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- button -->
      <div class="flex flex-center full-width">
        <ButtonComponent
          @click="handleMethod(active)"
          size="lg"
          label="برداشت"
          type="primary"
          class="custom-btn-withdraw"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetsStore } from 'src/stores/assetStore'

import SvgIcon from 'src/components/SvgIcon.vue'
import ButtonComponent from 'src/components/ButtonComponent.vue'

const router = useRouter()
const active = ref(null)

const store = useAssetsStore()
const assets = computed(() => store.assets)

onMounted(() => {
  store.fetchAssets()
})

function handleMethod(id) {
  const selectedMethod = assets.value.find(item => item.id === id)
  if (!selectedMethod) return

  const slug = selectedMethod.slug
  const route =`/account/${slug}`
  router.push(route)
}
</script>

<style scoped>
.content-wrapper {
  margin-bottom: 3.5rem;
}

.content-wrapper > div {
  margin-bottom: 0.75rem;
  width: 100%;
}

.colored-items {
  border: 1px solid rgba(102, 191, 161, 1);
}

.colored-item {
  border-radius: 0.5rem;
  padding: 0.625rem;
}

.margin-title {
  margin-bottom: 2rem;
}
</style>

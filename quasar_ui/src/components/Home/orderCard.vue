<template>
  <div class="order-card">
    <!-- Header -->
    <div class="order-header">
      <div class="order-id typography-caption-lg-medium text-grey-normal">
        شماره سفارش <span class="text-positive">{{ order.orderNumber }}</span>
      </div>
      <div class="badge typography-caption-md-regular">{{ order.status }}</div>
    </div>

    <!-- Divider -->
    <div class="divider q-mb-sm"></div>

    <!-- Content -->
    <div class="order-content">
      <!-- Image -->
      <div class="product-image">
        <img :src="order.image" alt="تصویر محصول" class="coin-img"/>
      </div>

      <!-- Info -->
      <div class="order-info">
        <div class="product-name typography-caption-md-bold text-grey-dark">{{ order.title }}</div>
        <div class="product-detail typography-caption-md-regular text-white-darker">عیار {{ order.karat }}</div>
        <div class="product-detail flex no-wrap items-center">
          <div class="flex items-center typography-caption-md-regular">
            <span class="icon q-ml-xs flex flex-center">
              <SvgIcon name="dashboard-location" state="black" size="16" />
            </span>
            {{ order.branch }}
          </div>
          <div class="flex items-center typography-caption-md-regular">
            <span class="q-ml-xs flex flex-center">
              <SvgIcon name="dashboard-clock" state="black" size="16" />
            </span>
            {{ order.date }}، ساعت {{ order.time }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import SvgIcon from '../SvgIcon.vue'

defineProps({
  order: {
    type: Object,
    required: true
  }
})

</script>

<style scoped>
.order-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0px 4px 16px 0 rgba(0, 0, 0, 0.16);
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 85vw;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  background-color: rgba(230, 244, 240, 1);
  color: black;
  padding: 0.5rem;
  border-radius: 0.5rem;
}


.order-number {
  color: #22A958;
  font-weight: bold;
}

.divider {
  height: 1px;
  background-color: #EEEEEE;
}

.order-content {
  display: flex;
  align-items: flex-start;
}

.order-info {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 8px;
}

.product-detail {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 4px;
}


.product-image{
background-color: rgba(219, 219, 219, 0.2);
  width: 4rem;
  height: 4rem;
   aspect-ratio: 1 / 1;
  border-radius: 0.5rem;
  margin-left: 0.5rem;
}
.coin-img{
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>

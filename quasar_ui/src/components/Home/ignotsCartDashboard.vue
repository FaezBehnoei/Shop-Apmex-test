<!-- Card.vue -->
<template>
  <div class="card">
    <div class="card-container">
      <div class="card-image-container">
        <img :src="imageUrl" :alt="title" class="card-image" />
      </div>
      <div class="card-title typography-caption-lg-regular">{{ title }}</div>
    </div>
  </div>
</template>

<script setup>

defineProps({
  imageUrl: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})
</script>


<style scoped>
.card {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 12px;
  width: 100%;
}

.card-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 4.5rem;
  height: 4.5rem;
  margin-bottom: 0.5rem;
  aspect-ratio: 1/1;
  background-color: var(--white-light-active);
  border-radius: 0.5rem;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.card-title {
  text-align: center;
}
</style>

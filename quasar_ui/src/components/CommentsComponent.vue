<template>
  <div class="main-container flex column">
    <!-- image & title  -->
     <div class="flex q-mb-sm">
      <img class="q-ml-sm" :src="image" :alt="title">
      <div class="flex column justify-center q-mr-xs">
        <span class="typography-body-lg-bold text-orange-primary">{{ title }}</span>
        <span class="typography-caption-lg-regular text-white-darker">{{ name }}</span>
      </div>
     </div>
    <!-- line  -->
    <div class="q-mb-sm">
      <hr>
    </div>
    <!-- text comment -->
     <div>
      <p class="typography-body-md-light comment-wrap q-mb-none">{{ comment }}</p>
     </div>
  </div>
</template>

<script setup>

defineProps({
  image: String,
  title:String,
  name:String,
  comment: String,
})

</script>

<style scoped>
.main-container{
  width: 358px;
  border-radius: 8px;
  border:1px solid rgba(212, 212, 212, 1);
  padding: 18px 16px;
}

.comment-wrap{
}
</style>

<!-- BannerAd.vue -->
<template>
  <div class="banner-container">
    <div class="banner-content">
      <h2 class="banner-title flex items-center typography-caption-md-bold">
        <span class="brand">
          <img class="q-pl-xs" src="/images/logoDashboardBanner.svg" alt="گلدیس">
        </span> خرید و فروش طلا با اطمینان کامل
      </h2>
      <p class="banner-subtitle typography-caption-md-regular">سرمایه‌گذاری · تضمین اصالت · بهترین قیمت</p>
      <button class="banner-button typography-caption-lg-regular">خرید</button>
    </div>
  </div>
</template>

<script setup>
// No props for now – can be added to make it dynamic later
</script>

<style scoped>
.banner-container {
  width: 100%;
  border-radius: 0.5rem;
  padding: 1rem;
  background-image: url('/images/bannerDashboard.png'); /* use your actual image path */
  background-size: cover;
  background-position: center;
  color: #000;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.banner-content {
  padding: 1rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.banner-title {
  margin-bottom: 0.25rem;
}

.brand {
  color: #D28E35; /* طلایی */
  font-weight: 900;
}

.banner-subtitle {
  margin-bottom: 1rem;
  color: black;
}

.banner-button {
  align-self: flex-start;
  padding: 0.4rem 2.25rem;
  font-size: 0.875rem;
  color: #C38E41;
  border: 1px solid #C38E41;
  background-color: transparent;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  background-color: #F9F3EC;
}

.banner-button:hover {
  background-color: #D28E35;
  color: white;
}
</style>

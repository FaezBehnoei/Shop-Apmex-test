<template>
  <div class="news-card">
    <!-- image -->
    <img :src="image" alt="news" class="news-image" />

    <!-- content -->
    <div class="news-content">
      <!-- title -->
      <div class="news-title typography-caption-lg-regular text-grey-darker">
        {{ title }}
      </div>

      <!-- meta -->
      <div class="news-meta flex justify-between items-center q-mt-sm">
        <span class="typography-caption-md-light text-white-dark">{{ source }}</span>
        <span class="typography-caption-md-light text-white-dark">{{ timeAgo }}</span>
      </div>

    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  source: { type: String, default: 'خبرآنلاین' },
  timeAgo: { type: String, default: '۱ ساعت پیش' },
  image: { type: String, default: '/images/sample-news.jpg' }
})
</script>

<style scoped>
.news-card {
  display: flex;
  width: 100%;
  gap: 0.75rem;
  padding-bottom: 0.75rem;
}
.news-card:not(:last-child) {
  border-bottom: 1px solid rgba(217, 217, 217, 1);
}

.news-card:last-child {
  border-bottom: none;
}

.news-image {
  border-radius: 4px;
  object-fit: cover;
  flex-shrink: 0;
}

.news-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.news-title {
  line-height: 1.4;
  max-height: 2.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-wrap: break-word;
  word-break: break-word;
  padding-left: 2rem;
}

.divider-line {
  margin-top: 0.5rem;
  height: 1px;
  background-color: #d9d9d9;
  width: 100%;
}
</style>

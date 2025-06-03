<!-- src/components/BackButton.vue -->
<template>
  <div class="back-button">
    <SvgIcon
      :name="iconName"
      :state="iconState"
      :size="iconSize"
      @click="handleBack"
      cursor="true"
      :class="customClass"
    />
  </div>
</template>

<script setup>
import { inject } from 'vue';
import { useRouter } from 'vue-router';
import SvgIcon from 'src/components/SvgIcon.vue';

// تزریق سرویس ناوبری
const navigationService = inject('navigationService');
const router = useRouter();

// تعریف پراپس با مقادیر پیش‌فرض
const props = defineProps({
  iconName: {
    type: String,
    default: 'arrow-left'
  },
  iconState: {
    type: String,
    default: 'black'
  },
  iconSize: {
    type: [String, Number],
    default: 24
  },
  defaultPath: {
    type: String,
    default: '/'
  },
  customClass: {
    type: String,
    default: ''
  },
  onBack: {
    type: Function,
    default: null
  }
});

/**
 * مدیریت رویداد کلیک برگشت
 */
const handleBack = () => {
  // اگر یک callback سفارشی تعریف شده، ابتدا آن را اجرا کنیم
  if (props.onBack) {
    const shouldContinue = props.onBack();
    // اگر callback مقدار false برگرداند، فرآیند برگشت را متوقف کنیم
    if (shouldContinue === false) {
      return;
    }
  }

  // استفاده از سرویس ناوبری برای برگشت
  navigationService.goBack(router, props.defaultPath);
};
</script>

<style scoped>
.back-button {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>

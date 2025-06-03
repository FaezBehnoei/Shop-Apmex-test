<template>
  <button
    :class="[
      'my-btn',
      `my-btn-${size}`,
      `my-btn-${type}`,
      customClass
    ]"
    :disabled="disable || loading"
    :type="htmlType"
    @click="$emit('click', $event)"
  >
    <q-spinner v-if="loading" color="white" size="20px" />
    <slot v-else>{{ label }}</slot>
  </button>
</template>


<script setup>
defineProps({
  label: String,
  type: { type: String, default: 'primary' }, // primary / secondary / ghost / danger
  size: { type: String, default: 'md', validator: v => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v) },
  htmlType: { type: String, default: 'button' },
  disable: Boolean,
  loading: Boolean,
  customClass: String
})
</script>

<style lang="scss" scoped>
.my-btn {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  font-family: var(--font-family);
  font-weight: 700;
  transition: 0.3s;
  border-radius: 0.5rem; // 8px
  cursor: pointer;
  border: none;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  width: 100%;

  // SIZE
  &-lg {
    font-weight: 500;
    height: 3rem; // 48px
    font-size: 0.875rem; // 14px
    line-height: 1.375rem; // 22px
  }

  &-md {
    height: 2.75rem; // 44px
    font-size: 1rem; // 16px
    line-height: 1.5rem; // 24px
  }

  &-sm {
    height: 2.5rem; // 40px
    font-size: 1rem; // 16px
    line-height: 1.5rem; // 24px
  }

  &-xs {
    height: 2.125rem; // 34px
    font-size: 0.75rem; // 12px
    line-height: 1.125rem; // 18px
    border-radius: 0.5rem; // 8px
  }

  // TYPE = VARIANT
  &-primary {
    background-color: var(--orange-primary);
    color: rgba(12, 38, 71, 1);
    border: none;

    &:hover {
      background-color: var(--grey-normal-hover);
    }

    &:active {
      background-color: var(--grey-normal-active);
    }

    &:disabled {
      background-color: var(--white-active);
      color: rgba(107, 107, 107, 1);
      cursor: not-allowed;
    }
  }

  &-stroke {
    background-color: transparent;
    border: 1px solid var(--orange-primary);
    color: var(--orange-primary);

    &:hover:not(:disabled) {
      border: 1px solid var(--grey-normal-hover);
    }

    &:active {
      border: 1px solid var(--grey-normal-active);
    }

    &:disabled {
      background-color: rgba(184, 184, 184, 1);
      color: var(--grey-normal);
      cursor: not-allowed;
      border-color: var(--q-grey-5);
    }
  }

  &-text {
    background-color: transparent;
    font-weight: 500;
    color: var(--grey-normal-active);
  }
}

// Mobile-specific padding
@media (max-width: 360px) {
  .my-btn {
    padding-inline: clamp(0.625rem, 20vw, 8.8125rem); // 10px → 141px
  }
}
</style>


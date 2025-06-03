<template>
  <div v-if="modalValue" class="modal-overlay flex row items-center justify-center">
    <div class="modal-content">
      <!-- Header -->
      <div class="header text-center">
        <span class="typography-body-md-bold text-grey-darker">{{ props.title }}</span>
      </div>

      <!-- Body -->
      <div class="body q-pb-sm text-center">

        <p class="typography-body-md-regular text-grey-darker">
          {{ props.bodyText }}
        </p>
      </div>

      <!-- Footer -->
      <div class=" q-pb-md">
        <ButtonComponent
          @click="closeModal"
          size="sm"
          label="متوجه شدم"
          type="primary"
          class="full-width custom-btn"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import ButtonComponent from 'components/ButtonComponent.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  modalValue: { type: Boolean, required: true },
  bodyText : {type : String, required: true},
  title: {type : String, required: true},
});
const emit = defineEmits(['update:modalValue']);
const router = useRouter()

function closeModal() {
  emit('update:modalValue', false);
  router.push('/account/wallet')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(0.125rem);
  z-index: 9999;
}

.modal-content {
  background-color: #fff;
  border-radius: 0.5rem;
  margin-inline: 1rem;
  overflow: hidden;
  padding-inline: 1.5rem;
}

.header {
  border-bottom: 1px solid #e6e6e6;
  padding: 0.7rem 1rem;
  margin-bottom: 0.5rem;
}
.custom-btn{
  font-size: 0.75rem;
  line-height: 1.125rem;
}

</style>

<template>
  <div v-if="modelValue" class="modal-overlay flex row items-center justify-center">
    <div class="modal-content">
      <!-- Header -->
      <div class="header q-mb-md flex flex-center">
        <button class="svg-btn" @click="emit('update:modelValue', false)">
          <SvgIcon name="close" state="black" size="24" class="close-icon"/>
        </button>
        <div class="full-width text-center">
         <span class="typography-body-md-bold text-grey-darker text-center">{{ title }}</span>
        </div>
      </div>

      <!-- Body -->
      <div class="body text-right">
        <p class="typography-body-md-regular text-grey-darker q-mb-md">
          {{ description }}
        </p>

        <InputComponent
          v-model="inputValue"
          :type="inputType"
          class="q-mb-md custom-input"
          :placeholder="placeholder"
        />
      </div>

      <!-- Footer -->
      <div class="q-pb-md">
        <ButtonComponent
          :disabled="!inputValue"
          @click="submit"
          size="lg"
          :label="submitLabel"
          type="primary"
          class="full-width custom-btn"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ButtonComponent from 'components/ButtonComponent.vue';
import SvgIcon from '../SvgIcon.vue';
import InputComponent from '../InputComponent.vue';
import { useProfileStore } from 'src/stores/profileStore';

const profileStore = useProfileStore()

 const props = defineProps({
  modelValue: { type: Boolean, required: true },
  title: { type: String, default: 'عنوان' },
  description: { type: String, default: 'توضیح' },
  placeholder: { type: String, default: '' },
  submitLabel: { type: String, default: 'تأیید' },
  inputType: { type: String, default: 'text' },
  field : String,
});

const emit = defineEmits(['update:modelValue', 'submit', 'updated']);
const inputValue = ref('');

async function submit() {
  if(props.field === 'phone_number'){
    profileStore.setProfileField('phone_number', inputValue.value);
    // Trigger a re-fetch to ensure UI updates
    await profileStore.submitProfileEditInfo();
    console.log('this is profileedits in editdialog page ',profileStore.profileEdits)
    emit('update:modelValue', false);
    emit('updated')
  } else if(props.field === 'password'){
    profileStore.setProfileField('password', inputValue.value);
    // Trigger a re-fetch to ensure UI updates
    await profileStore.submitProfileEditInfo();
    emit('update:modelValue', false);
    emit('updated')
  }
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
  padding: 0.1rem 1rem 1.5rem 1rem;
  width: 100%;
  max-width: 360px;
}

.header {
  margin-bottom: 1rem;
  position: relative;
  min-height: 3rem;
}
.close-icon{
  position: absolute;
  top: 50%;
  right: 0%;
  transform: translateY(-50%);
}

.custom-btn {
  font-size: 0.75rem;
  line-height: 1.125rem;
}
.body{
  margin-bottom: 1.5rem;
}
.custom-input{
  border: 1px solid var(--white-normal-active);
}
.svg-btn{
  border: none;
  outline: none;
  background-color: none;
}
</style>

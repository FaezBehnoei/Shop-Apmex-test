<template>
  <q-page >
    <div class="q-px-md">
      <!-- Branch Options -->
      <div class="branch-options">

          <!-- Option  -->
          <div v-for="address in userAddresses" :key="address.id" class="branch-option bg-white-light-hover q-mb-sm flex justify-between items-center" :class="{ selected : selectedBranch === address.id }">
            <div class="option-content flex">
            <div
              class="check-wrapper"
              :class="{ selected: selectedBranch === address.id }"
              @click="selectedBranch = address.id"
            >
              <SvgIcon v-if="selectedBranch === address.id" name="check" state="black" size="16" />
            </div>
              <div class="branch-name typography-caption-lg-regular text-white-darker">
                {{ address.address }}
              </div>
            </div>
            <div class="q-pr-sm" >

                <SvgIcon name="round-edit" state="black" size="16" class="q-pl-xs" />
                <SvgIcon v-if="selectedBranch !== address.id" name="trash" state="black" size="16" />
                <SvgIcon v-else name="trash" state="red" size="16" />
              </div>
          </div>
        </div>
        <!-- new address  -->
        <div class="download-section flex justify-start q-mt-md q-px-sm">
            <button @click="handleNewAddresDialog" flat class="download-btn text-primary">
              <SvgIcon name="plus-blue" state="black" size="24" />
              <span class="text-primary q-mr-xs typography-caption-lg-regular">ثبت ادرس جدید</span>
            </button>
          </div>
    </div>
    <NewAddressDialog v-model:model-value="openNewAddress"/>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import SvgIcon from 'src/components/SvgIcon.vue';
import NewAddressDialog from 'src/components/profile/NewAddressDialog.vue';

const openNewAddress = ref(false)
const selectedBranch = ref(null)
const userAddresses = ref( [
            {
                "id": 4,
                "address": "تهران، صندوق پستی 4567",
                "title": "تهران",
                "latitude": 35.744,
                "longitude": 51.375
            },
            {
                "id": 5,
                "address": "اصفهان، صندوق پستی 8910",
                "title": "اصفهان",
                "latitude": 32.6546,
                "longitude": 51.6674
            }
        ])

function handleNewAddresDialog(){
  openNewAddress.value = true
}
</script>

<style scoped>
.branch-option {
  padding: 1.5rem 0.5rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(173, 173, 173, 1);
}

.branch-option.selected {
  background-color: rgba(255, 239, 229, 1);
  border: 1px solid var(--orange-primary);
}

.option-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1 1 0;
  min-width: 0;
}

.branch-name {
  flex: 1 1 0;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.download-btn {
  outline: none;
  border: none;
  background-color: transparent;
  display: flex;
  align-items: center;
  color: rgba(45, 156, 219, 1);
}
</style>

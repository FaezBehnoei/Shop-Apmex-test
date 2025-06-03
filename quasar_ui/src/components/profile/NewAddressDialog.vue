<template>
 <div v-if="props.modelValue"  class="modal-overlay">
   <div class="new-address-dialog">
    <!-- header  -->
      <div class="header-icon flex items-center q-mb-md">
        <button class="btn-header" @click="$emit('update:modelValue', false)">
          <SvgIcon name="close" state="black" size="24"  class="close-icon"/>
        </button>
        <div class="full-width text-center">
          <span class="typography-body-md-medium text-grey-darker">ادرس جدید</span>
        </div>
      </div>
    <!-- Map Section -->
    <div id="leaflet-map" class="leaflet-map"></div>

    <!-- Address Input Section -->
    <div class="form-section">
      <div class="full-width flex flex-center q-mb-md">
        <div class="section-divider"></div>
      </div>
      <InputComponent label="آدرس" v-model="address.address" type="text" placeholder="صادقیه،فلکه سوم،خیابان محمدی" class="text-input" />

      <div class="row">
        <div class="column">
          <InputComponent label="پلاک" v-model="address.buildingNumber" type="text" class="text-input" />
        </div>
        <div class="column">
          <InputComponent label="واحد" v-model="address.unit" type="text" class="text-input" />
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="submit-button">
      <ButtonComponent label="تایید" size="lg" @click="submitAddress" />
    </div>
  </div>
 </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import ButtonComponent from 'components/ButtonComponent.vue';
import SvgIcon from '../SvgIcon.vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import InputComponent from '../InputComponent.vue';

const props = defineProps({
  modelValue: Boolean
});

const emit = defineEmits(['update:modelValue'])

const address = ref({
  title: 'آدرس جدید',
  address: '',
  buildingNumber: '',
  unit: '',
  latitude: 35.7219,
  longitude: 51.3347
});

let map = null;
let marker = null;

function initMap() {
  map = L.map('leaflet-map', {
    center: [address.value.latitude, address.value.longitude],
    zoom: 15,
    zoomControl: false,
    attributionControl: false
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(map);

  const markerHtml = `
  <div class="custom-marker">
    <img src="/icons/name=pin, state=black, size=20px.svg" class="marker-icon" alt="marker" />
  </div>
`;

const icon = L.divIcon({
  html: markerHtml,
  className: '',
  iconSize: [32, 32],
  iconAnchor: [16, 32]
});


  marker = L.marker([address.value.latitude, address.value.longitude], {
    icon
  }).addTo(map);

  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    marker.setLatLng([lat, lng]);
    address.value.latitude = lat;
    address.value.longitude = lng;
  });

  // اطمینان از اینکه نقشه درست رندر می‌شه
  setTimeout(() => map.invalidateSize(), 500);
}


onMounted(() => {
  setTimeout(() => {
    initMap();
    setTimeout(() => map.invalidateSize(), 300);
  }, 300);
});

function submitAddress() {
  emit('update:modelValue', false);
}

watch(() => props.modelValue, (val) => {
  if (val) {
    setTimeout(() => {
      initMap()
      setTimeout(() => map.invalidateSize(), 300)
    }, 300)
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(0.125rem);
  -webkit-backdrop-filter: blur(0.125rem);
  z-index: 9999;
  overflow-y: auto;
}
.new-address-dialog {
  background-color: white;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  padding: 0.2rem 1rem 1rem 1rem;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
}

.leaflet-map {
  width: 100%;
  height: 40vh;
  border-radius: 1.25rem 1.25rem 0 0 ;
  background-color: #E5EFF5;
  margin-bottom: 0.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.header-icon {
  position: relative;
  min-height: 3rem;
  padding: 0 1rem 0rem 1rem;
  border-bottom: 0.0625rem solid rgba(230, 230, 230, 1);
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 0.5rem;
  transform: translateY(-50%);
  cursor: pointer;
}


.row {
  display: flex;
  gap: 1rem;
}

.column {
  flex: 1;
}

.submit-button {
  margin-top: auto;
  padding-top: 1.5rem;
}

:deep(.custom-marker ){
  width: 32px;
  height: 32px;
  background-color: var(--orange-primary);
  border-radius: 50%;
  border: 1px solid rgba(145, 162, 182, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.marker-icon){
  width: 20px;
  height: 20px;
}
.section-divider {
  height: 3px;
  width: 2.5rem;
  background-color: var(--grey-normal-hover); /* دقیق مثل رنگ طرح */
}
.btn-header{
  border: none;
  outline: none;
  background-color: transparent;
}

</style>

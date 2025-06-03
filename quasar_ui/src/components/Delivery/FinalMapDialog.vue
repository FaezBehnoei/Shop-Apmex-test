<template>
  <div v-if="props.modalValue" class="modal-overlay flex items-center justify-center">
    <div class="modal-content">
       <!-- header  -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon"/>
        <div class="full-width text-center">
          <span class="typography-body-lg-bold text-grey-darker">ادرس شعبه {{ address.title }}</span>
        </div>
      </div>

      <!-- Map container -->
      <div class="map-container">
        <div id="leaflet-map" class="map"></div>
      </div>

      <!-- Address box -->
      <div class="address-box q-mt-md">
        <div class="flex flex-center">
          <SvgIcon class="location-container" name="route-location" state="black" size="16"/>
        </div>
        <div class="address-content">
          <div class="typography-caption-lg-regular q-pb-xs">ادرس ما</div>
          <div class="address-text typography-caption-lg-regular text-white-darker">{{ address.address }}</div>
        </div>
      </div>

      <!-- View on map button -->
      <div class="view-map-button-container">
        <ButtonComponent  label="دیدن روی نقشه" size="lg" @click="openInMap"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import ButtonComponent from 'components/ButtonComponent.vue';
import SvgIcon from 'components/SvgIcon.vue';
import {watch} from 'vue';
import 'leaflet/dist/leaflet.css'
// @ts-ignore
import L from 'leaflet';

const props = defineProps({
  modalValue: { type: Boolean, required: true },
  address: Object,
})

let mapInstance = null



watch(() => props.modalValue, (val) => {
  if (val) {
    setTimeout(() => {
      const { latitude, longitude } = props.address;

      if (!mapInstance) {
        mapInstance = L.map('leaflet-map', {
          center: [latitude, longitude],
          zoom: 15,
          zoomAnimation:       true,
          fadeAnimation:       true,
          markerZoomAnimation: true,
          inertia:             true,
          inertiaDeceleration: 3000,
          easeLinearity:       0.35,
          attributionControl: false,
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', ).addTo(mapInstance);

        const customIcon = L.divIcon({
          html: `
            <div class="map-marker">
              <div class="map-marker__inner"></div>
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: '' // جلوی کلاس‌های پیش‌فرض leaflet رو می‌گیره
        });
        L.marker([latitude, longitude],{
        icon: customIcon
       })
         .addTo(mapInstance)

      } else {
        mapInstance.setView([latitude, longitude], 14);
      }

      // تأخیر بیشتر برای لود کامل DOM و tiles
      setTimeout(() => {
        mapInstance.invalidateSize();
      }, 500);
    }, 300);
  }else if(mapInstance){
    mapInstance.remove()
    mapInstance = null
  }
});

function openInMap() {
  const { latitude, longitude } = props.address
  const url = `https://maps.google.com/?q=${latitude},${longitude}`
  window.open(url, '_blank')
}


</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-content {
  background-color: white;
  overflow-y: auto;
  position: fixed;
  flex-direction: column;
  border-radius: 1.25rem 1.25rem 0 0; /* 20px */
  bottom: 0;
  right: 0;
  left: 0;
  padding-inline: 1rem;
  max-height: calc(100vh - 2rem);
}

.header-icon {
  position: relative;
  height: 3.5rem; /* 56px */
  padding: 0 1rem;
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  cursor: pointer;
}

.map-container {
  width: 100%;
  height: 60vh; /* 380px */
  position: relative;
  overflow: hidden;
  border-radius: 1.25rem; /* 20px */
}

.map {
  background-color: #E5EFF5;
  width: 100%;
  height: 100%;
  position: relative;
}

.location-marker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 2.5rem; /* 40px */
  height: 2.5rem;
  background-color: #FF7F33;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0.0625rem 0.25rem 0 rgba(0, 0, 0, 0.08); /* 1px 4px */
  border: 0.25rem solid rgba(81, 81, 81, 1); /* 4px */
}

.marker-inner {
  width: 0.625rem; /* 10px */
  height: 0.625rem;
  background-color: white;
  border-radius: 50%;
}

.address-box {
  gap: 0.5rem;
  padding: 0.5rem 1rem 0.5rem 0.5rem;
  background-color: white;
  border-radius: 1.25rem; /* 20px */
  display: flex;
  flex-direction: row;
  border: 1px solid rgba(145, 162, 182, 0.2);
}

.address-title {
  color: #888;
  font-size: 0.875rem; /* 14px */
  margin-bottom: 0.5rem; /* 8px */
}

.address-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.location-pin {
  margin-left: 0.5rem; /* 8px */
  flex-shrink: 0;
}

.view-map-button-container {
  margin-top: 1.125rem; /* 18px */
  padding-bottom: 1rem;
}

.view-map-button {
  width: 100%;
  padding: 0.875rem; /* 14px */
  background-color: #FF7F33;
  color: white;
  border: none;
  border-radius: 0.75rem; /* 12px */
  font-size: 1rem; /* 16px */
  font-weight: bold;
  cursor: pointer;
  direction: rtl;
}

.location-container {
  padding: 0.75rem; /* 12px */
  background-color: var(--white-light-active);
  border-radius: 50%;
}

.address-text {
  word-wrap: break-word;
}
.custom-marker-container {
  background: none;
  border: none;
}

.custom-map-marker {
  width: 40px;
  height: 40px;
  background-color: #FF7F33;
  border: 4px solid #515151;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
::v-deep .map-marker {
  position: relative;
  width: 40px;
  height: 40px;
  background-color: #FF7F33;
  border: 3px solid #515151;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

::v-deep .map-marker__inner {
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
}


.marker-inner {
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
}
</style>


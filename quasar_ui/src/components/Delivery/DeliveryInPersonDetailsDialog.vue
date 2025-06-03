<template>
  <div v-if="props.modalValue" class="modal-overlay flex items-center justify-center">
    <div class="modal-content">
      <!-- header -->
      <div class="header-icon flex items-center q-mb-md">
        <SvgIcon name="close" state="black" size="24" @click="$emit('update:modalValue', false)" class="close-icon"/>
        <div class="full-width text-center">
          <span class="typography-body-lg-bold text-grey-darker">جزئیات تحویل</span>
        </div>
      </div>

      <!-- date/time -->
      <div class="delivery-datetime q-mb-md">
        <div class="flex q-pa-sm">
          <div class="typography-caption-lg-regular text-grey-darker text-start date-time-box">{{props.timing.day}} - {{props.timing.date}} - {{props.timing.time}}</div>
        </div>
        <div class="devider"></div>
        <!-- address box -->
        <div class="address-box-container flex flex-center">
          <div class="address-box">
          <div class="flex flex-center">
            <SvgIcon class="location-container" name="route-location" state="black" size="16"/>
          </div>
          <div class="address-content">
            <div class="typography-caption-lg-regular q-pb-xs">آدرس ما</div>
            <div class="address-text typography-caption-md-bold text-white-darker">
              {{ address.address }}
            </div>
          </div>
        </div>
        </div>
      </div>



      <!-- map -->
      <div class="map-container">
        <div id="leaflet-map" class="map"></div>
      </div>

      <!-- cancel button -->
      <div class="cancel-button-container">
        <ButtonComponent label="لغو تحویل" size="lg" type="stroke" class="cancel-button"   @click="() => { $emit('cancelDelivery'); $emit('update:modalValue', false) }"
 />
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue'
import SvgIcon from 'components/SvgIcon.vue'
import 'leaflet/dist/leaflet.css'
// @ts-ignore
import L from 'leaflet'
import ButtonComponent from '../ButtonComponent.vue'

const props = defineProps({
  modalValue: Boolean,
  address: {
    type: Object,
    required: true,
    default: () => ({
    })
  },
  timing: { type : Object}
})

defineEmits(['update:modalValue', 'cancelDelivery'])

let mapInstance = null

watch(() => props.modalValue, (val) => {
  if (val) {
    setTimeout(() => {
      const { latitude, longitude } = props.address

      if (!mapInstance) {
        mapInstance = L.map('leaflet-map', {
          center: [latitude, longitude],
          zoom: 15,
          attributionControl: false,
          zoomAnimation: true,
          fadeAnimation: true,
          markerZoomAnimation: true
        })

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance)

        const customIcon = L.divIcon({
          html: `<div class="map-marker"><div class="map-marker__inner"></div></div>`,
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: ''
        })

        L.marker([latitude, longitude], {
          icon: customIcon
        }).addTo(mapInstance)
      } else {
        mapInstance.setView([latitude, longitude], 14)
      }

      setTimeout(() => {
        mapInstance.invalidateSize()
      }, 500)
    }, 300)
  } else if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.modal-content {
  background-color: white;
  overflow-y: auto;
  position: fixed;
  flex-direction: column;
  border-radius: 1.25rem 1.25rem 0 0;
  bottom: 0;
  right: 0;
  left: 0;
  padding: 0 1rem;
  max-height: calc(100vh - 2rem);
}

.header-icon {
  position: relative;
  height: 3.5rem;
}

.close-icon {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  cursor: pointer;
}

.delivery-datetime {
  background-color: white;
  border-radius: 1.25rem;
  margin: 0 0.5rem;
  border: 1px solid rgba(145, 162, 182, 0.2);
  gap: 0.625rem;
}
.address-box-container{
  padding: 0.5rem;
}

.address-box {
  width: 100%;
  background-color: var(--white-light-active);
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 3rem;
  display: flex;
  flex-direction: row;

}

.devider{
  width: 100%;
  background-color: rgba(145, 162, 182, 0.2);
  height: 1px;
}

.date-time-box{
  border: 0.5px solid rgba(145, 162, 182, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 1.5rem;
}

.address-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.address-text {
  word-wrap: break-word;
}

.location-container {
  padding: 0.75rem;
  background-color: white;
  border-radius: 50%;
  color: #FF7F33;
}

.map-container {
  width: 100%;
  height: 24rem;
  border-radius: 1.25rem;
  overflow: hidden;
  margin-top: 1rem;
}

.map {
  background-color: #e5eff5;
  width: 100%;
  height: 100%;
}

:deep(.map-marker) {
  position: relative;
  width: 40px;
  height: 40px;
  background-color: #FF7F33;
  border: 3px solid #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

:deep(.map-marker__inner) {
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
}

.cancel-button-container {
  padding: 1rem 0;
}

.cancel-button {
  color: red;
  border-color: red;
}
.cancel-button:active{
  border-color: red !important;
}
.cancel-button:hover{
  border-color: red !important;
}
</style>

// src/utils/toastService.js
import { Notify } from 'quasar'
import { h } from 'vue'
import SvgIcon from 'components/SvgIcon.vue'

export function showToast({
  type = 'info',               // 'positive', 'negative', 'warning', 'info'
  message = '',
  iconName = '',               // نام آیکون سفارشی (از SvgIcon.vue)
  iconColor = '',
  position = 'top',
  timeout = 4000,
  classes = ''
}) {
  Notify.create({
    type,
    icon: false, // غیرفعال کردن آیکون Quasar
    message: h('div', { class: 'custom-toast-wrapper flex items-center' }, [
      iconName &&
      h('span', { class: 'typography-body-md-regular' }, message),
        h(SvgIcon, {
          name: iconName,
          state:'balck',
          size: 24,
          class: 'q-mr-xs custom-toast-icon',
          style: { color: iconColor }
        }),

    ]),
    position,
    timeout,
    classes
  })
}

export function showSuccess(message) {
  showToast({
    type: 'positive',
    message,
    iconName: 'check-toast',
    iconColor: '#00C897',
    classes: 'my-toast-success'
  })
}

export function showError(message) {
  showToast({
    type: 'negative',
    message,
    iconName: 'close-toast',
    iconColor: '#F04438',
    classes: 'my-toast-error'
  })
}

export function showInfo(message) {
  showToast({
    type: 'info',
    message,
    iconName: 'info',
    iconColor: '#4F46E5',
    classes: 'my-toast-info'
  })
}

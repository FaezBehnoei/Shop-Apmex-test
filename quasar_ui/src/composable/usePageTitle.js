import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const globalTitle = ref(null)

export function usePageTitle(titleRef = null) {
  const route = useRoute()

  if (titleRef) {
    if (typeof titleRef === 'string') {
      globalTitle.value = titleRef
    } else if (titleRef.value) {
      watch(titleRef, (newTitle) => {
        globalTitle.value = newTitle
      }, { immediate: true })
    }
  } else {
    const routeTitle = computed(() => {
      const type = route.params.type

      if (route.path.includes('asset-detail') && type) {
        if (type === 'gold') return 'دارایی طلا'
        if (type === 'silver') return 'دارایی نقره'
        if (type === 'ignot') return 'دارایی فیزیکی'
        if (type === 'rial') return 'دارایی ریالی'
        return `دارایی ${type}`
      }

      if (route.path.includes('withdraw/buy') && type) {
        if (type === 'gold') return 'خرید طلا'
        if (type === 'silver') return 'خرید نقره'
        return `خرید ${type}`
      }

      if (route.path.includes('withdraw/sell') && type) {
        if (type === 'gold') return 'فروش طلا'
        if (type === 'silver') return 'فروش نقره'
        return `فروش ${type}`
      }

      if (route.meta?.title) {
        return route.meta.title
      }

      if (route.params?.name) {
        return route.params.name
      }

      return null
    })

    watch(routeTitle, (newTitle) => {
      if (newTitle) {
        globalTitle.value = newTitle
      }
    }, { immediate: true })
  }

  return { title: globalTitle }
}

<template>
  <q-page class="q-pa-md">
    <h5>لیست کاربران</h5>
    <q-list bordered>
      <q-item v-for="user in users" :key="user.id" clickable>
        <q-item-section>{{ user.name }}</q-item-section>
      </q-item>
    </q-list>
    <q-btn label="خروج" color="negative" @click="logout" />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'

const users = ref([])

onMounted(async () => {
  const res = await api.get('/users')
  users.value = res.data.users
})


const router = useRouter()

async function logout () {
  await api.post('/logout')
  router.push('/')
}
</script>

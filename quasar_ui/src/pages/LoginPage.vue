<template>
  <q-page class="flex flex-center">
    <q-card class="q-pa-md" style="width: 300px">
      <q-card-section>
        <div class="text-h6">ورود</div>
      </q-card-section>

      <q-card-section>
        <q-input v-model="username" label="نام کاربری" />
        <q-input v-model="password" label="رمز عبور" type="password" />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="ورود" color="primary" @click="login" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

const router = useRouter()
const username = ref('')
const password = ref('')

async function login () {
  try {
    const res = await api.post('/login', {
      username: username.value,
      password: password.value
    })
    alert(res.data.message)
    router.push('/users')
  } catch {
    alert('ورود ناموفق')
  }
}
</script>

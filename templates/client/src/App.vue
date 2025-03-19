<template>
  <div v-if="isLoading" class="loading-screen">
    Загрузка...
  </div>
  <div v-else class="app-container">
    <RouterView v-if="isAuthenticated" />
  </div>
</template>

<script setup>
import { ref, watchEffect, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/authStore';

const router = useRouter();
const authStore = useAuthStore();
const isAuthenticated = ref(false);
const isLoading = ref(true);

onMounted(async () => {
  try {
    const auth = await authStore.getMe();
    isAuthenticated.value = !!auth;
    if (!isAuthenticated.value) {
      authStore.deactivateAuth();
      router.push('/auth');
    }
  } catch (error) {
    authStore.deactivateAuth();
    router.push('/auth');
  } finally {
    isLoading.value = false;
  }
});

// Следим за изменением авторизации
watchEffect(() => {
  isAuthenticated.value = !!localStorage.getItem('ais.auth.token');
});

const logout = () => {
  localStorage.removeItem('ais.auth.token');
  isAuthenticated.value = false;
  router.push('/auth');
};
</script>

<style scoped>
.loading-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 20px;
}

.app-container {
  width: 100%;
  height: 100%;
}
</style>

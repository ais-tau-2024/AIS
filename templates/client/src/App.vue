<script setup>
import { ref, watchEffect } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(!!localStorage.getItem('ais.auth.token'));

// Следим за изменением авторизации
watchEffect(() => {
  isAuthenticated.value = !!localStorage.getItem('ais.auth.token');
});

const logout = () => {
  localStorage.removeItem('ais.auth.token');
  isAuthenticated.value = false;
  router.push('/auth'); // Перенаправление на страницу авторизации
};
</script>

<template>
  <RouterView />
</template>

<style scoped>

</style>

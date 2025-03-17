import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router/router.js'  // Импортируем роутер
const pinia = createPinia();
// Создаём приложение и подключаем роутер
const app = createApp(App);
app.use(pinia);  // Подключаем Pinia перед роутером
app.use(router);
app.mount('#app');

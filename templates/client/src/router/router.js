import { createWebHistory, createRouter } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import UsersView from '../views/UsersView.vue'
import StorageView from '../views/StorageView.vue'

const routes = [
  { path: '/', component: HomeView, meta: { requiresAuth: true } }, // Требует авторизации
  { path: '/auth', component: AuthView },
  { path: '/profile', component: ProfileView },
  { path: '/users', component: UsersView },
  { path: '/storage', component: StorageView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('ais.auth.token'); // Проверяем токен

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth'); // Если нет токена, отправляем на страницу входа
  } else if (to.path === '/auth' && isAuthenticated) {
    next('/'); // Если уже авторизован, редиректим в профиль
  } else {
    next();
  }
});

export default router;

import { createWebHistory, createRouter } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import UsersView from '../views/UsersView.vue'
import StorageView from '../views/StorageView.vue'
import TeacherPersonalCardView from '../views/TeacherPersonalCardView.vue'
import StudentPersonalCardView from '../views/StudentPersonalCardView.vue'

const routes = [
    // { path: '/', component: HomeView, meta: { requiresAuth: true } }, // Требует авторизации
    { path: '/auth', component: AuthView },
    { path: '/profile', component: ProfileView },
    { path: '/users', component: UsersView },
    { path: '/user/teacher/:teacherIin', component: TeacherPersonalCardView },
    { path: '/user/student/:studentIin', component: StudentPersonalCardView },
    { path: '/storage', component: StorageView },
    { path: '/storage/:storageId', component: StorageView },
    // { path: '/:pathMatch(.*)*', redirect: '/' }, // Перехват неизвестных маршрутов
    { path: '/:pathMatch(.*)*', redirect: '/profile' }, // Перехват неизвестных маршрутов
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('ais.auth.token') // Проверяем токен

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/auth') // Если нет токена, отправляем на страницу входа
    } else if (to.path === '/auth' && isAuthenticated) {
        next('/profile') // Если уже авторизован, редиректим на главную
    } else {
        next()
    }
})

export default router

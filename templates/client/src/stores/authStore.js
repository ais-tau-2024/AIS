import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router/router'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
    }),

    actions: {
        async getMe({ refresh = false } = {}) {
            try {
                // refresh true - мы обновляем и возвращаем данные с сервера
                // refresh false - мы берем данные с памяти если они там есть, иначе делаем запрос на сервер

                if (refresh == false && this.user != null) {
                    return this.user
                }
                try {
                    const response = await axios.get('userTeacher/me/', {
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                            'Additional-Info': '1',
                        },
                    })
                    this.user = response.data
                } catch {}
                return this.user
            } catch (error) {
                console.error('Ошибка при загрузке данных:', error)
                return null
            }
        },
        deactivateAuth() {
            console.log('Деактивация авторизации')
            localStorage.removeItem('ais.auth.token')
            router.push('/auth')
        },
    },
})

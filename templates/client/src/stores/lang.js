import { defineStore } from 'pinia'

export const useLangStore = defineStore('lang', {
    state: () => ({
        lang: localStorage.getItem('ais.lang') || 'ru', // Читаем язык из localStorage
    }),
    actions: {
        setLang(newLang) {
            this.lang = newLang
            localStorage.setItem('ais.lang', newLang) // Сохраняем выбор пользователя
        },
        changeLang() {
            this.lang = this.lang == 'ru' ? 'kz' : 'ru'
            localStorage.setItem('ais.lang', this.lang) // Сохраняем выбор пользователя
        },
    },
})

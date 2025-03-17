<template>
    <section class="page auth">
        <div class="container">
            <div class="card">
                <div class="header">
                    <select class="form-select w-25" v-model="lang">
                        <option v-for="(value, key) in localization" :value="key" :key="key">
                            {{ value.lang }}
                        </option>
                    </select>
                    <span class="help-link" :title="localization[lang]?.page?.auth?.helpTitle">
                        {{ localization[lang]?.page?.auth?.help }}
                    </span>
                </div>
                <h2 class="title">{{ localization[lang]?.page?.auth?.title }}</h2>
                
                <form @submit.prevent="authPageLogin">  <!-- Используем form для автозаполнения -->
                    <label for="iin" class="form-label required mb-05">
                        {{ localization[lang]?.page?.auth?.iin }}
                    </label>
                    <input 
                        type="text" 
                        id="iin" 
                        class="form-control w-100" 
                        :placeholder="localization[lang]?.page?.auth?.iinPlaceholder" 
                        autocomplete="username"  
                        v-model="authForm.iin"
                    />
                    
                    <label for="password" class="form-label required mb-05">
                        {{ localization[lang]?.page?.auth?.password }}
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        class="form-control w-100" 
                        :placeholder="localization[lang]?.page?.auth?.passwordPlaceholder" 
                        autocomplete="current-password"
                        v-model="authForm.password"
                    />
                    
                    <template v-if="authForm.passwordConfirmationVisible">
                        <label for="passwordConfirmation" class="form-label required">
                            {{ localization[lang]?.page?.auth?.passwordPlaceholderConfirmation }}
                        </label>
                        <input 
                            type="password" 
                            id="passwordConfirmation" 
                            class="form-control w-100" 
                            :placeholder="localization[lang]?.page?.auth?.passwordPlaceholderConfirmation" 
                            autocomplete="new-password" 
                            v-model="authForm.passwordConfirmation"
                        />
                    </template>
                                
                    <button type="submit" class="btn w-100">
                        {{ localization[lang]?.page?.auth?.login }}
                    </button>
                </form>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';
import router from '../router/router'
import { localization } from '../assets/js/localization';
import '../assets/css/root.css'
import '../assets/css/style.css'
import '../assets/css/page-auth.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: "AuthView",
    data() {
        return {
            lang: localStorage.getItem('ais.lang') || 'ru',
            localization: {}, // Загружаем локализацию
            authForm: {
                iin: '',
                password: '',
                passwordConfirmation: '',
                passwordConfirmationVisible: false
            }
        };
    },
    methods: {
        async authPageLogin() {
            const iin = this.authForm.iin;
            const password = this.authForm.password;

            if (!iin || iin.length !== 12) {
                alert("Введите корректный ИИН из 12 цифр");
                return;
            }

            try {
                const response = await axios.post('/auth/teacher/login', {
                    iin,
                    password
                });

                if (response.data.token) {
                    localStorage.setItem('ais.auth.token', response.data.token);
                    router.push('/profile'); // Редирект в профиль
                } else {
                    alert('Ошибка авторизации');
                }
            } catch (error) {
                console.error('Ошибка входа:', error);
                alert('Не удалось войти');
            }
        }
    },
    mounted() {
        this.localization = localization;
    }
};
</script>



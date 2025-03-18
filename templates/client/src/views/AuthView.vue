<template>
    <section class="page auth bg-white">
        <div class="container">
            <div class="card bg-dark text-white">
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
                
                <form @submit.prevent="authPageLogin">
                    <label for="iin" class="form-label required mb-05">
                        {{ localization[lang]?.page?.auth?.iin }}
                    </label>
                    <input 
                        type="text" 
                        id="iin" 
                        class="form-control w-100 mb-3" 
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
                                
                    <button type="submit" class="btn btn-success w-100 mt-4">
                        {{ localization[lang]?.page?.auth?.login }}
                    </button>
                </form>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';
import router from '../router/router';
import { localization } from '../assets/js/localization';
import '../assets/css/root.css';
import '../assets/css/style.css';
import '../assets/css/page-auth.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000';

export default {
    name: "AuthView",
    data() {
        return {
            lang: localStorage.getItem('ais.lang') || 'ru',
            localization: {},
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
            const { iin, password, passwordConfirmation, passwordConfirmationVisible } = this.authForm;

            if (!iin || iin.length !== 12) {
                alert("Введите корректный ИИН из 12 цифр");
                return;
            }
            if (!password) {
                alert("Введите пароль");
                return;
            }

            try {
                // Если подтверждение не активно, проверяем статус пароля
                if (!passwordConfirmationVisible) {
                    const res = await axios.get('/auth/teacher/password', { params: { iin } });
                    // Если пароль не установлен – показываем поле подтверждения
                    if (res.status === 203) {
                        this.authForm.passwordConfirmationVisible = true;
                        alert("Пароль не установлен. Подтвердите новый пароль.");
                        return;
                    }
                }

                // Если требуется подтверждение – проверяем совпадение и создаём пароль
                if (passwordConfirmationVisible) {
                    if (password !== passwordConfirmation) {
                        alert("Пароли не совпадают");
                        return;
                    }
                    await axios.post('/auth/teacher/password', { iin, password });
                    alert("Пароль успешно создан");
                }

                // Выполняем авторизацию
                const loginRes = await axios.post('/auth/teacher/login', { iin, password });
                if (loginRes.data.token) {
                    localStorage.setItem('ais.auth.token', loginRes.data.token);
                    router.push('/profile');
                } else {
                    alert("Ошибка авторизации");
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка. Попробуйте еще раз.");
            }
        }
    },
    mounted() {
        this.localization = localization;
    }
};
</script>

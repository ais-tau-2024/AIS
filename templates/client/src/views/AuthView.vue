<template>
    <section class="page auth bg-light">
        <div class="container">
            <div class="custom-card bg-white text-dark">
                <div class="content d-flex flex-column justify-between">
                    <div class="w-100">
                        <h2 class="title">Sign Up</h2>
                        <form @submit.prevent="handleSubmit">
                            <label for="iin" class="form-label required mb-05">
                                {{ localization[langStore.lang]?.page?.auth?.iin }}
                            </label>
                            <input
                                type="text"
                                id="iin"
                                class="form-control w-100 mb-3"
                                :placeholder="
                                    localization[langStore.lang]?.page?.auth?.iinPlaceholder
                                "
                                autocomplete="username"
                                v-model="authForm.iin"
                                :disabled="step > 1"
                            />

                            <!-- Переход с анимацией -->
                            <transition name="expand">
                                <div v-if="step > 1" class="extra-fields mt-3">
                                    <label for="password" class="form-label required mb-05">
                                        {{ localization[langStore.lang]?.page?.auth?.password }}
                                    </label>
                                    <input
                                        type="password"
                                        id="password"
                                        class="form-control w-100 mb-3"
                                        :placeholder="
                                            localization[langStore.lang]?.page?.auth
                                                ?.passwordPlaceholder
                                        "
                                        autocomplete="current-password"
                                        v-model="authForm.password"
                                    />

                                    <template v-if="!hasPassword">
                                        <label
                                            for="passwordConfirmation"
                                            class="form-label required mt-2"
                                        >
                                            {{
                                                localization[langStore.lang]?.page?.auth
                                                    ?.passwordPlaceholderConfirmation
                                            }}
                                        </label>
                                        <input
                                            type="password"
                                            id="passwordConfirmation"
                                            class="form-control w-100 mb-3"
                                            :placeholder="
                                                localization[langStore.lang]?.page?.auth
                                                    ?.passwordPlaceholderConfirmation
                                            "
                                            autocomplete="new-password"
                                            v-model="authForm.passwordConfirmation"
                                        />
                                    </template>
                                </div>
                            </transition>

                            <button type="submit" class="btn btn-success w-100 mt-4">
                                {{
                                    step === 1
                                        ? localization[langStore.lang]?.page?.auth?.next
                                        : localization[langStore.lang]?.page?.auth?.login
                                }}
                            </button>
                        </form>
                    </div>
                    <div class="w-100">
                        <select class="form-select w-25" v-model="lang">
                            <option v-for="(value, key) in localization" :value="key" :key="key">
                                {{ value.lang }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="img">
                    <img src="/images/bgc.jpg" alt="" />
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'
import router from '../router/router'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import { useAuthStore } from '../stores/authStore'
import '../assets/css/root.css'
import '../assets/css/style.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: 'AuthView',
    data() {
        return {
            lang: null,
            langStore: null,
            authStore: null,
            localization: localization,
            step: 1,
            hasPassword: false,
            authForm: {
                iin: '',
                password: '',
                passwordConfirmation: '',
            },
        }
    },
    created() {
        this.langStore = useLangStore()
        this.authStore = useAuthStore()
        this.lang = this.langStore.lang
    },
    methods: {
        async handleSubmit() {
            if (this.step === 1) {
                if (!this.authForm.iin || this.authForm.iin.length !== 12) {
                    alert('Введите корректный ИИН из 12 цифр')
                    return
                }
                try {
                    const res = await axios.get('/auth/teacher/password', {
                        params: { iin: this.authForm.iin },
                    })
                    if (res.status === 200) {
                        this.hasPassword = true
                    } else if (res.status === 203) {
                        this.hasPassword = false
                        alert('Пароль не установлен. Создайте новый пароль.')
                    }
                    this.step = 2
                } catch (error) {
                    console.error('Ошибка:', error)
                    alert('Произошла ошибка. Попробуйте еще раз.')
                }
            } else if (this.step === 2) {
                if (!this.authForm.password) {
                    alert('Введите пароль')
                    return
                }
                if (
                    !this.hasPassword &&
                    this.authForm.password !== this.authForm.passwordConfirmation
                ) {
                    alert('Пароли не совпадают')
                    return
                }
                try {
                    if (!this.hasPassword) {
                        await axios.post('/auth/teacher/password', {
                            iin: this.authForm.iin,
                            password: this.authForm.password,
                        })
                        alert('Пароль успешно создан')
                    }
                    const loginRes = await axios.post('/auth/teacher/login', {
                        iin: this.authForm.iin,
                        password: this.authForm.password,
                    })
                    if (loginRes.data.token) {
                        localStorage.setItem('ais.auth.token', loginRes.data.token)
                        router.push('/profile')
                    } else {
                        alert('Ошибка авторизации')
                    }
                } catch (error) {
                    console.error('Ошибка:', error)
                    alert('Произошла ошибка. Попробуйте еще раз.')
                }
            }
        },
    },
}
</script>

<style scoped lang="scss">
.page.auth {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.page.auth .container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 20px;
}

.custom-card {
    display: flex;
    width: 1400px;
    border: 1px solid black;
    border-radius: 14px;
    transition: all 0.5s ease;

    .content {
        width: 40%;
        padding: 70px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;

        .title {
            font-size: 64px;
            text-align: left;
            margin-bottom: 50px;
        }

        label {
            margin-bottom: 14px;
        }

        input {
            font-size: 18px;
            padding: 20px 24px;
        }

        button {
            font-size: 24px;
            margin-top: 30px;
            margin-bottom: 120px;
            padding: 24px;
            background-color: #61ba5f;
        }
    }

    .img {
        width: 60%;
        overflow: hidden;
        transition: all 0.5s ease;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: all 0.5s ease;
        }
    }
}

/* Анимация разворачивания */
.expand-enter-active,
.expand-leave-active {
    transition: all 0.5s ease;
    max-height: 500px;
    overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
    max-height: 0;
    opacity: 0;
    margin-top: 0;
}

.expand-enter-to,
.expand-leave-from {
    max-height: 500px;
    opacity: 1;
    // margin-top: 20px;
}
</style>

<template>
	<section class="page auth bg-light">
		<div class="container">
			<div class="card bg-white text-dark">
				<div class="header">
					<select class="form-select w-25" v-model="lang">
						<option
							v-for="(value, key) in localization"
							:value="key"
							:key="key"
						>
							{{ value.lang }}
						</option>
					</select>
					<span
						class="help-link"
						:title="localization[lang]?.page?.auth?.helpTitle"
					>
						{{ localization[lang]?.page?.auth?.help }}
					</span>
				</div>
				<h2 class="title">
					{{ localization[lang]?.page?.auth?.title }}
				</h2>
				<form @submit.prevent="handleSubmit">
					<label for="iin" class="form-label required mb-05">
						{{ localization[lang]?.page?.auth?.iin }}
					</label>
					<input
						type="text"
						id="iin"
						class="form-control w-100 mb-3"
						:placeholder="
							localization[lang]?.page?.auth?.iinPlaceholder
						"
						autocomplete="username"
						v-model="authForm.iin"
						:disabled="step > 1"
					/>
					<template v-if="step > 1">
						<label for="password" class="form-label required mb-05">
							{{ localization[lang]?.page?.auth?.password }}
						</label>
						<input
							type="password"
							id="password"
							class="form-control w-100 mb-3"
							:placeholder="
								localization[lang]?.page?.auth
									?.passwordPlaceholder
							"
							autocomplete="current-password"
							v-model="authForm.password"
						/>
						<template v-if="!hasPassword">
							<label
								for="passwordConfirmation"
								class="form-label required"
							>
								{{
									localization[lang]?.page?.auth
										?.passwordPlaceholderConfirmation
								}}
							</label>
							<input
								type="password"
								id="passwordConfirmation"
								class="form-control w-100 mb-3"
								:placeholder="
									localization[lang]?.page?.auth
										?.passwordPlaceholderConfirmation
								"
								autocomplete="new-password"
								v-model="authForm.passwordConfirmation"
							/>
						</template>
					</template>
					<button type="submit" class="btn btn-success w-100 mt-4">
						{{
							step === 1
								? localization[lang]?.page?.auth?.next
								: localization[lang]?.page?.auth?.login
						}}
					</button>
				</form>
			</div>
		</div>
	</section>
</template>

<script>
import axios from "axios";
import router from "../router/router";
import { localization } from "../assets/js/localization";
import "../assets/css/root.css";
import "../assets/css/style.css";
import "../assets/css/page-auth.css";

axios.defaults.baseURL = "http://127.0.0.1:8000";

export default {
	name: "AuthView",
	data() {
		return {
			lang: localStorage.getItem("ais.lang") || "ru",
			localization: {},
			step: 1,
			hasPassword: false, // true, если пароль уже установлен
			authForm: {
				iin: "",
				password: "",
				passwordConfirmation: "",
			},
		};
	},
	methods: {
		async handleSubmit() {
			if (this.step === 1) {
				if (!this.authForm.iin || this.authForm.iin.length !== 12) {
					alert("Введите корректный ИИН из 12 цифр");
					return;
				}
				try {
					const res = await axios.get("/auth/teacher/password", {
						params: { iin: this.authForm.iin },
					});
					if (res.status === 200) {
						this.hasPassword = true;
					} else if (res.status === 203) {
						this.hasPassword = false;
						alert("Пароль не установлен. Создайте новый пароль.");
					}
					this.step = 2;
				} catch (error) {
					console.error("Ошибка:", error);
					alert("Произошла ошибка. Попробуйте еще раз.");
				}
			} else if (this.step === 2) {
				if (!this.authForm.password) {
					alert("Введите пароль");
					return;
				}
				if (
					!this.hasPassword &&
					this.authForm.password !==
						this.authForm.passwordConfirmation
				) {
					alert("Пароли не совпадают");
					return;
				}
				try {
					if (!this.hasPassword) {
						await axios.post("/auth/teacher/password", {
							iin: this.authForm.iin,
							password: this.authForm.password,
						});
						alert("Пароль успешно создан");
					}
					const loginRes = await axios.post("/auth/teacher/login", {
						iin: this.authForm.iin,
						password: this.authForm.password,
					});
					if (loginRes.data.token) {
						localStorage.setItem(
							"ais.auth.token",
							loginRes.data.token,
						);
						router.push("/profile");
					} else {
						alert("Ошибка авторизации");
					}
				} catch (error) {
					console.error("Ошибка:", error);
					alert("Произошла ошибка. Попробуйте еще раз.");
				}
			}
		},
	},
	mounted() {
		this.localization = localization;
	},
};
</script>

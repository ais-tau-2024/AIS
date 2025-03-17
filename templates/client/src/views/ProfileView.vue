<template>
    <div class="profile-view">
        <LeftPanelComponent class="left-panel" />
        <div class="profile-section p-3">
            <h2 class="fs-3">Profile</h2>
            <hr>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
import router from '../router/router';
import { localization } from '../assets/js/localization';
import LeftPanelComponent from '../components/LeftPanelComponent.vue';

axios.defaults.baseURL = 'http://127.0.0.1:8000';

export default {
    name: "ProfileView",
    components: { LeftPanelComponent },
    data() {
        return {
            data: null, // Изначально пустое
        };
    },
    async created() {
        this.data = await this.getMe(); // Загружаем данные при создании компонента
        console.log(this.data)
    },
    methods: {
        async getMe() {
            try {
                const response = await axios.get('auth/teacher/me', {
                    headers: {
                        'auth': localStorage.getItem('ais.auth.token'),
                    },
                });
                return response.data; // Возвращаем данные
            } catch (error) {
                console.error("Ошибка при загрузке данных:", error);
                return null;
            }
        },
    },
};
</script>
<style scoped>
.profile-view {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: stretch; /* Растянет дочерние элементы */
    justify-content: flex-start; /* Исключит центрирование */
    overflow: hidden; /* Убирает возможную прокрутку */
}

.profile-section {
    flex-grow: 1; /* Занимает оставшееся пространство */
    height: 100%;
    min-width: 0; /* Запрещает выход за границы */
    overflow: hidden; /* Убирает горизонтальную прокрутку */
}

.left-panel {
    min-width: var(--left-panel-width);
    height: 100%;
    flex-shrink: 0; /* Чтобы не сжимался */
}
</style>

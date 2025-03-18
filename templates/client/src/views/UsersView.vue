<template>
    <div class="users-view">
        <LeftPanelComponent class="left-panel" />
        <div class="users-section p-3 fs-6">
            <h1 class="fs-2">Users</h1>
            <hr>
            <div class="my-3">
                <button type="button" :class="'btn me-2 ' + (userType == 'teachers' ? 'btn-success' : 'btn-outline-success')" @click="()=>{userType = 'teachers'}">Преподаватели</button>
                <button :class="'btn ' + (userType == 'students' ? 'btn-success' : 'btn-outline-success')" @click="()=>{userType = 'students'}">Студенты</button>
            </div>
            <table class="table table-striped" v-if="userType == 'students'">
                <thead>
                    <tr>
                        <th scope="col">ФИО</th>
                        <th scope="col">Специальность/Группа образовательных программ</th>
                        <th scope="col">Форма оплаты</th>
                        <th scope="col">Форма оплаты</th>
                        <th scope="col">Форма оплаты</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>Otto</td>
                        <td>Otto</td>
                        <td>@mdo</td>
                    </tr>
                    <tr>
                        <td>Jacob</td>
                        <td>Thornton</td>
                        <td>Thornton</td>
                        <td>Thornton</td>
                        <td>@fat</td>
                    </tr>
                    <tr>
                        <td>@twitter</td>
                        <td>@twitter</td>
                        <td>@twitter</td>
                        <td>@twitter</td>
                        <td>@twitter</td>
                    </tr>
                </tbody>
            </table>
            <table class="table table-striped" v-if="userType == 'teachers'">
                <thead>
                    <tr>
                        <th scope="col">ФИО</th>
                        <!-- <th scope="col">Дата рождения</th> -->
                        <!-- <th scope="col">Дата поступления на работу</th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Mark</td>
                    </tr>
                    <tr>
                        <td>Jacob</td>
                    </tr>
                    <tr>
                        <td>@twitter</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios';
import router from '../router/router'
import {localization} from '../assets/js/localization'
import LeftPanelComponent from '../components/LeftPanelComponent.vue';


axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: "UsersView",
    components: {LeftPanelComponent},
    data() {
        return {
            userType: localStorage.getItem("ais.usersView.userType") || 'students',
            studentList: []
        }
    },
    watch: {
        'userType'(newVal) {
            localStorage.setItem('ais.usersView.userType', newVal)
        }
    },
    async created() {
        this.studentList = await this.getStudentList();
        this.teacherList = await this.getTeacherList();
        
    },
    methods: {
        async getStudentList() {
            axios.get(`${axios.defaults.baseURL}/userStudent/list/`)
            .then(response => {
                console.log("Полученные данные:", response.data);
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
        },
        async getTeacherList() {
            axios.get(`${axios.defaults.baseURL}/userTeacher/list/`)
            .then(response => {
                console.log("Полученные данные:", response.data);
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
        }
    }
}
</script>
<style scoped>
.users-view {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: stretch; /* Растянет дочерние элементы */
    justify-content: flex-start; /* Исключит центрирование */
    overflow: hidden; /* Убирает возможную прокрутку */
}

.users-section {
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

table th {
    font-weight: 600;
}
</style>

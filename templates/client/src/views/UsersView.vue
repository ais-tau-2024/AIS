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
                        <th scope="col" style="width: 250px;">Форма оплаты</th>
                        <th scope="col" style="width: 250px;">Группа</th>
                        <th scope="col" style="width: 250px;">Дата рождения</th>
                        <th scope="col" style="width: 250px;">Дата зачисления</th> 
                    </tr>
                </thead>
                <tbody>
                    <template v-for="student in studentList">
                        <tr>
                            <td class="cursor-pointer elem-hover" @click="()=>{openStudentPersonalCard(student.iin)}">{{ student.firstName + ' ' + student.lastName + ' ' + student.patronymic }}</td>
                            <td>{{ student.formOfPayment == 0 ? 'Платная' : 'Бесплатная' }}</td>
                            <td>{{ student.groupName }}</td>
                            <td>{{ student.birthDate }}</td>
                            <td>{{ student.dateOfEnrollment }}</td>
                        </tr>
                    </template>
                </tbody>
            </table>
            <table class="table table-striped" v-if="userType == 'teachers'">
                <thead>
                    <tr>
                        <th scope="col">ФИО</th>
                        <th scope="col" style="width: 300px;">Дата рождения</th>
                        <th scope="col" style="width: 300px;">Дата поступления на работу</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="teacher in teacherList">
                        <tr>
                            <td class="cursor-pointer elem-hover" @click="()=>{openTeacherPersonalCard(teacher.iin)}">{{ teacher.firstName + ' ' + teacher.lastName + ' ' + teacher.patronymic }}</td>
                            <td>{{ teacher.birthDate }}</td>
                            <td>{{ teacher.admissionDate }}</td>
                        </tr>
                    </template>
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
            studentList: [],
            teacherList: []
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
            return await axios.get(`${axios.defaults.baseURL}/userStudent/list/`, {
              headers: { auth: localStorage.getItem('ais.auth.token') }
            })
            .then(response => {
                console.log("Полученные данные:", response.data);
                return response.data
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
        },
        async getTeacherList() {
            return await axios.get(`${axios.defaults.baseURL}/userTeacher/list/`, {
              headers: { auth: localStorage.getItem('ais.auth.token') }
            })
            .then(response => {
                console.log("Полученные данные:", response.data);
                return response.data
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
        },
        openTeacherPersonalCard(iin) {
            router.push('/user/teacher/'+iin)
        },
        openStudentPersonalCard(iin) {
            router.push('/user/student/'+iin)
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
    overflow-y: scroll;
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

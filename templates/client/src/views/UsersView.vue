<template>
    <div class="users-view">
        <LeftPanelComponent class="left-panel" />
        <div class="users-section p-4" @scroll="onScroll">
            <h1 class="page-title">{{ localization[lang]?.page.users.pageTitle }}</h1>
            <div class="d-flex gap-2">
                <div
                    class="tab"
                    :class="{ active: userType === 'teachers' }"
                    @click="userType = 'teachers'"
                >
                    {{ localization[lang]?.page.users.buttonTeachers || 'Преподаватели' }}
                </div>
                <div
                    class="tab"
                    :class="{ active: userType === 'students' }"
                    @click="userType = 'students'"
                >
                    {{ localization[lang]?.page.users.buttonStudents || 'Студенты' }}
                </div>
            </div>

            <div
                class="d-flex gap-2 my-3 mt-0"
                v-if="userType === 'teachers' || userType === 'students'"
            >
                <!-- Поиск по ФИО или ИИН -->
                <div class="input-group" style="max-width: 400px">
                    <input
                        type="text"
                        class="form-control"
                        :placeholder="
                            localization[lang]?.page.users.searchPlaceholder ||
                            'Введите Ф.И.О. или ИИН'
                        "
                        v-model="searchQuery"
                    />
                    <button
                        class="btn btn-danger d-flex align-items-center justify-content-center"
                        @click="performSearch"
                    >
                        <img class="search-img" src="../assets/icons/white/search.png" alt="" />
                    </button>
                </div>

                <!-- Фильтр по группам (только для студентов) -->
                <select class="form-select" v-if="userType === 'students'" v-model="selectedGroup">
                    <label for="">123</label>
                    <option value="">
                        {{ localization[lang]?.page.users.allGroups || 'Все' }}
                    </option>
                    <option v-for="group in groups" :key="group.id" :value="group.name">
                        {{ group.name }}
                    </option>
                </select>
            </div>

            <table class="table table-striped" v-if="userType === 'students'">
                <thead>
                    <tr>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tableFio }}
                        </th>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tablePayType }}
                        </th>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tableGroup }}
                        </th>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tableBirthday }}
                        </th>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tableDateOfEnrollment }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="student in studentList.results" :key="student.iin">
                        <tr>
                            <td
                                class="cursor-pointer elem-hover"
                                @click="openStudentPersonalCard(student.iin)"
                            >
                                {{ student.lastName }}
                                {{ student.firstName }}
                                {{ student.patronymic }}
                            </td>
                            <td>{{ student.formOfPayment === 0 ? 'Платная' : 'Бесплатная' }}</td>
                            <td>{{ student.groupName }}</td>
                            <td>{{ student.birthDate }}</td>
                            <td>{{ student.dateOfEnrollment }}</td>
                        </tr>
                    </template>
                </tbody>
            </table>
            <table class="table table-striped" v-if="userType === 'teachers'">
                <thead>
                    <tr>
                        <th scope="col">{{ localization[lang]?.page.users.tableFio }}</th>
                        <th scope="col">{{ localization[lang]?.page.users.tableBirthday }}</th>
                        <th scope="col">
                            {{ localization[lang]?.page.users.tableDateOfAdmissionWork }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="teacher in teacherList.results" :key="teacher.iin">
                        <tr>
                            <td
                                class="cursor-pointer elem-hover"
                                @click="openTeacherPersonalCard(teacher.iin)"
                            >
                                {{ teacher.lastName }}
                                {{ teacher.firstName }}
                                {{ teacher.patronymic }}
                            </td>
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
import axios from 'axios'
import router from '../router/router'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import LeftPanelComponent from '../components/LeftPanelComponent.vue'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: 'UsersView',
    components: { LeftPanelComponent },
    data() {
        return {
            langStore: null,
            localization,
            userType: localStorage.getItem('ais.usersView.userType') || 'students',
            // Структура данных соответствует API: { page, total_pages, count, results }
            studentList: { results: [], page: 0, total_pages: 1 },
            teacherList: { results: [], page: 0, total_pages: 1 },
            isLoading: false,

            // Фиотр и сортировка
            searchQuery: '',
            selectedGroup: '',
            groups: [],
        }
    },
    watch: {
        userType(newVal) {
            localStorage.setItem('ais.usersView.userType', newVal)
        },
    },
    computed: {
        lang() {
            return this.langStore?.lang
        },
    },
    async created() {
        await this.getStudentList(1)
        await this.getTeacherList(1)
        this.langStore = useLangStore()
    },
    methods: {
        async getStudentList(page = 1) {
            if (this.isLoading) return
            this.isLoading = true
            try {
                const response = await axios.get(`/userStudent/list/?page=${page}&page_size=30`, {
                    headers: {
                        auth: localStorage.getItem('ais.auth.token'),
                    },
                })
                if (page === 1) {
                    this.studentList = response.data
                } else {
                    this.studentList.results.push(...response.data.results)
                    this.studentList.page = response.data.page
                    this.studentList.total_pages = response.data.total_pages
                }
            } catch (error) {
                console.error('Ошибка:', error)
            } finally {
                this.isLoading = false
            }
        },
        async getTeacherList(page = 1) {
            if (this.isLoading) return
            this.isLoading = true
            try {
                const response = await axios.get(`/userTeacher/list/?page=${page}&page_size=30`, {
                    headers: {
                        auth: localStorage.getItem('ais.auth.token'),
                    },
                })
                if (page === 1) {
                    this.teacherList = response.data
                } else {
                    this.teacherList.results.push(...response.data.results)
                    this.teacherList.page = response.data.page
                    this.teacherList.total_pages = response.data.total_pages
                }
            } catch (error) {
                console.error('Ошибка:', error)
            } finally {
                this.isLoading = false
            }
        },
        onScroll(e) {
            const el = e.target
            // Если прокрутили почти до конца контейнера (отступ 10px)
            if (el.scrollTop + el.clientHeight >= el.scrollHeight - 10) {
                if (
                    this.userType === 'students' &&
                    this.studentList.page < this.studentList.total_pages
                ) {
                    this.getStudentList(this.studentList.page + 1)
                } else if (
                    this.userType === 'teachers' &&
                    this.teacherList.page < this.teacherList.total_pages
                ) {
                    this.getTeacherList(this.teacherList.page + 1)
                }
            }
        },
        openTeacherPersonalCard(iin) {
            router.push('/user/teacher/' + iin)
        },
        openStudentPersonalCard(iin) {
            router.push('/user/student/' + iin)
        },
    },
}
</script>

<style scoped>
* {
    font-size: 20px;
}
.page-title {
    font-weight: bold;
    color: var(--color-blue);
    font-size: 40px;
}

.tab {
    width: max-content;
    padding: 20px 34px;
    margin: 35px 0;

    background-color: white;
    color: var(--color-blue);

    cursor: pointer;

    border-radius: 4px;
    border: 2px solid var(--color-blue);

    font-weight: 500;
    font-size: 20px;

    transition: 0.3s;
}

.tab:hover {
    background-color: var(--color-blue);
    color: white;
}

.tab.active {
    background-color: var(--color-blue);
    color: white;
}

.users-view {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: stretch;
    justify-content: flex-start;
    overflow: hidden;
}
.users-section {
    flex-grow: 1;
    height: 100%;
    min-width: 0;
    overflow: hidden;
    overflow-y: scroll;
}
.left-panel {
    min-width: var(--left-panel-width);
    height: 100%;
    flex-shrink: 0;
}
table th {
    font-weight: 600;
}
th {
    width: max-content !important;
    font-size: 22px;
}

/* search-img */
.search-img {
    width: 18px;
}
</style>

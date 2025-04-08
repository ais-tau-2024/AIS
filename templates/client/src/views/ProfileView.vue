<template>
    <div class="profile-view">
        <LeftPanelComponent class="left-panel" />
        <div class="profile-section p-4" style="overflow-y: scroll !important">
            <h2 class="fs-3">{{ localization[lang]?.page.profile.pageTitle }} - {{ tab }}</h2>
            <hr />

            <div class="mb-2 tabs d-flex">
                <div
                    :class="
                        'tab py-2 px-3 me-3 ' +
                        (tab == localization[lang]?.page.profile.tabs.personalData ? 'active' : '')
                    "
                    @click="
                        () => {
                            tab = localization[lang]?.page.profile.tabs.personalData
                        }
                    "
                >
                    {{ localization[lang]?.page.profile.tabs.personalData }}
                </div>
                <div
                    :class="
                        'tab py-2 px-3 me-3 ' +
                        (tab == localization[lang]?.page.profile.tabs.documents ? 'active' : '')
                    "
                    @click="
                        () => {
                            tab = localization[lang]?.page.profile.tabs.documents
                        }
                    "
                >
                    {{ localization[lang]?.page.profile.tabs.documents }}
                </div>
                <div
                    :class="
                        'tab py-2 px-3 me-3 ' +
                        (tab == localization[lang]?.page.profile.tabs.contactInformation
                            ? 'active'
                            : '')
                    "
                    @click="
                        () => {
                            tab = localization[lang]?.page.profile.tabs.contactInformation
                        }
                    "
                >
                    {{ localization[lang]?.page.profile.tabs.contactInformation }}
                </div>
                <div
                    :class="
                        'tab py-2 px-3 me-3 ' +
                        (tab == localization[lang]?.page.profile.tabs.trainingInformation
                            ? 'active'
                            : '')
                    "
                    @click="
                        () => {
                            tab = localization[lang]?.page.profile.tabs.trainingInformation
                        }
                    "
                >
                    {{ localization[lang]?.page.profile.tabs.trainingInformation }}
                </div>
                <div
                    :class="
                        'tab py-2 px-3 me-3 ' +
                        (tab == localization[lang]?.page.profile.tabs.supervisedGroups
                            ? 'active'
                            : '')
                    "
                    @click="
                        () => {
                            tab = localization[lang]?.page.profile.tabs.supervisedGroups
                        }
                    "
                >
                    {{ localization[lang]?.page.profile.tabs.supervisedGroups }}
                </div>
            </div>
            <hr />
            <div v-if="tab == localization[lang]?.page.profile.tabs.trainingInformation">
                <h3 class="fs-5">Общая информация</h3>
                <div class="form-group">
                    <div class="input-group">
                        <div>
                            <label>Достижения</label>
                        </div>
                        <div class="w-100">
                            <textarea
                                name=""
                                id=""
                                v-model="data.registrationAddress"
                                style="min-width: 100%; min-height: 100px"
                                disabled
                            ></textarea>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label>Отрасль науки</label>
                        <input
                            type="text"
                            :value="data.science_fields ? data.science_fields[0].field : ''"
                            disabled
                        />
                    </div>
                    <div class="input-group">
                        <label>Ученая/Академическая степень</label>
                        <input
                            type="text"
                            :value="
                                data.science_fields ? data.science_fields[0].academicDegree : ''
                            "
                            disabled
                        />
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label>Академический статус</label>
                        <input
                            type="text"
                            :value="
                                data.science_fields ? data.science_fields[0].academicStatus : ''
                            "
                            disabled
                        />
                    </div>
                    <!-- <div class="input-group">
                        <label>Язык преподавания</label>
                        <input type="text" :value="data.registrationAddress" disabled />
                    </div> -->
                </div>
                <h3 class="fs-5 mt-1 mb-1">Образование</h3>
                <div class="form-group">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">
                                    <span class="fw-bold"
                                        >Наименование образовательного учреждения</span
                                    >
                                </th>
                                <th scope="col">
                                    <span class="fw-bold"
                                        >Квалификация по документу образования</span
                                    >
                                </th>
                                <th scope="col">
                                    <span class="fw-bold"
                                        >Направление или специальность по документу</span
                                    >
                                </th>
                                <th scope="col">
                                    <span class="fw-bold">Год окончания</span>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="education in data.education_records">
                                <tr>
                                    <th scope="row">
                                        {{ education.institutionName }}
                                    </th>
                                    <td>
                                        {{ education.qualification }}
                                    </td>
                                    <td>{{ education.specialization }}</td>
                                    <td>{{ education.graduationYear }}</td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-if="tab == localization[lang]?.page.profile.tabs.supervisedGroups">
                <template v-for="group in data.groups">
                    <div class="card mb-2">
                        <div class="card-body">{{ group?.group?.name }}</div>
                    </div>
                </template>
            </div>
            <div v-if="tab == localization[lang]?.page.profile.tabs.contactInformation">
                <div class="form-group">
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.contactInformation.form.homePhoneNumber
                        }}</label>
                        <input type="text" id="" disabled :value="data.homePhone" />
                    </div>
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.contactInformation.form.mobilePhone
                        }}</label>
                        <input type="text" id="" disabled :value="data.phoneNumber" />
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.contactInformation.form.mail
                        }}</label>
                        <input type="text" id="" disabled :value="data.email" />
                    </div>
                </div>
            </div>
            <div v-if="tab == localization[lang]?.page.profile.tabs.documents">
                <div class="form-group">
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.documentTypeLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.documentType" />
                    </div>
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.documentNumberLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.documentNumber" />
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.documentSeriesLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.documentSeries" />
                    </div>
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.documentIssueDateLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.documentIssueDate" />
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.documentExpiryDateLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.documentExpiryDate" />
                    </div>
                    <div class="input-group">
                        <label for="">{{
                            localization[lang]?.page.profile.documents.form.issuingAuthorityLabel
                        }}</label>
                        <input type="text" id="" disabled :value="data.issuingAuthority" />
                    </div>
                </div>
            </div>
            <div v-if="tab == localization[lang]?.page.profile.tabs.personalData">
                <div class="content">
                    <div class="photo-section">
                        <img :src="axiosDefaultsBaseURL + '/' + data.profilePhoto" alt="avatar" />
                    </div>
                    <div class="form-section">
                        <div class="form-group">
                            <div class="input-group">
                                <label for="surname">{{
                                    localization[lang]?.page.profile.personalData.form.lastName
                                }}</label>
                                <input type="text" id="surname" v-model="data.lastName" />
                            </div>
                            <div class="input-group">
                                <label for="surname-translit">{{
                                    localization[lang]?.page.profile.personalData.form
                                        .lastNameTranslit
                                }}</label>
                                <input
                                    type="text"
                                    id="surname-translit"
                                    disabled
                                    :value="transliterateToLatin(data.lastName)"
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="input-group">
                                <label for="name">{{
                                    localization[lang]?.page.profile.personalData.form.firstName
                                }}</label>
                                <input type="text" id="name" v-model="data.firstName" />
                            </div>
                            <div class="input-group">
                                <label for="name-translit">{{
                                    localization[lang]?.page.profile.personalData.form
                                        .firstNameTranslit
                                }}</label>
                                <input
                                    type="text"
                                    id="name-translit"
                                    disabled
                                    :value="transliterateToLatin(data.firstName)"
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="input-group">
                                <label for="patronymic">{{
                                    localization[lang]?.page.profile.personalData.form.patronymic
                                }}</label>
                                <input type="text" id="patronymic" v-model="data.patronymic" />
                            </div>
                            <div class="input-group">
                                <label for="patronymic-translit">{{
                                    localization[lang]?.page.profile.personalData.form
                                        .patronymicTranslit
                                }}</label>
                                <input
                                    type="text"
                                    id="patronymic-translit"
                                    disabled
                                    :value="transliterateToLatin(data.patronymic)"
                                />
                            </div>
                        </div>
                    </div>
                </div>
                <!-- {{ data }} -->
                <div class="form-container" style="margin-bottom: 50px">
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.iin
                            }}</label>
                            <input type="text" v-model="data.iin" />
                        </div>
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.birthDate
                            }}</label>
                            <input type="date" v-model="data.birthDate" />
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.nationality
                            }}</label>
                            <select v-model="data.nationality">
                                <option v-for="nat in nationalities" :key="nat">
                                    {{ nat }}
                                </option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.gender
                            }}</label>
                            <select v-model="data.gender">
                                <option v-for="g in genders" :key="g">
                                    {{ g }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.maritalStatus
                            }}</label>
                            <select v-model="data.maritalStatus">
                                <option v-for="ms in maritalStatuses" :key="ms">
                                    {{ ms }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <h3>
                        {{ localization[lang]?.page.profile.personalData.form.labelPlaceOfBirth }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.placeOfBirth
                            }}</label>
                            <Multiselect
                                v-model="data.placeOfBirth"
                                :options="birthPlaceOptions"
                                label="label"
                                :filterable="true"
                                placeholder="Введите название"
                                @search-change="fetchAutoComplete($event, 'birthPlace')"
                            />
                        </div>
                    </div>
                    <h3>
                        {{
                            localization[lang]?.page.profile.personalData.form.labelPlaceOfResidence
                        }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.registrationPlace
                            }}</label>
                            <Multiselect
                                v-model="data.registrationPlace"
                                :options="registrationPlaceOptions"
                                label="label"
                                :filterable="true"
                                placeholder="Введите название"
                                @search-change="fetchAutoComplete($event, 'registrationPlace')"
                            />
                        </div>
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form
                                    .registrationAddress
                            }}</label>
                            <input type="text" v-model="data.registrationAddress" />
                        </div>
                    </div>

                    <h3>
                        {{
                            localization[lang]?.page.profile.personalData.form.labelPlaceOfResidence
                        }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.residencePlace
                            }}</label>
                            <Multiselect
                                v-model="data.residencePlace"
                                :options="residencePlaceOptions"
                                label="label"
                                :filterable="true"
                                placeholder="Введите название"
                                @search-change="fetchAutoComplete($event, 'residencePlace')"
                            />
                        </div>
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form
                                    .residentialAddress
                            }}</label>
                            <input type="text" v-model="data.residentialAddress" />
                        </div>
                    </div>
                    <button class="save-button" @click="saveForm">
                        {{ localization[lang]?.page.profile.personalData.form.save }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import router from '../router/router'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import { useAuthStore } from '../stores/authStore'
import LeftPanelComponent from '../components/LeftPanelComponent.vue'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: 'ProfileView',
    components: { LeftPanelComponent, Multiselect },
    data() {
        return {
            langStore: null,
            localization: localization,
            axiosDefaultsBaseURL: axios.defaults.baseURL,

            tab: 'Сведения об обучении', // Личные данные, Документы, Сведения об обучении, Курируемые группы

            data: {
                id: null,
                profilePhoto: '',
                firstName: '',
                lastName: '',
                patronymic: '',
                iin: '',
                birthDate: null,
                gender: null,
                nationality: null,
                maritalStatus: null,
                citizenship: null,
                // Для Multiselect используем объект или null
                placeOfBirth: null,
                registrationPlace: null,
                residencePlace: null,
                registrationAddress: '',
                residentialAddress: '',
                documentType: null,
                documentNumber: null,
                documentIssueDate: null,
                documentExpiryDate: null,
                issuingAuthority: null,
                phoneNumber: null,
                homePhone: null,
                email: '',
                teachingLanguage: null,
                groups: {
                    id: null,
                    teacher: null,
                    group: {
                        id: null,
                        name: null,
                    },
                },
            },
            genders: ['Мужской', 'Женский'],
            maritalStatuses: ['Холост/Не замужем', 'Женат/Замужем'],
            nationalities: [
                'Казах',
                'Русский',
                'Уйгур',
                'Кореец',
                'Немец',
                'Татарин',
                'Украинец',
                'Киргиз',
                'Узбек',
                'Азербайджанец',
                'Чеченец',
                'Туркмен',
                'Таджик',
                'Другой',
            ],
            countries: [
                'Казахстан',
                'Россия',
                'Узбекистан',
                'Кыргызстан',
                'Таджикистан',
                'Туркменистан',
                'Китай',
                'Турция',
                'Германия',
                'Украина',
                'США',
                'Корея',
                'Другие',
            ],
            originRegions: [
                /* список регионов */
            ],
            // Опции для автозаполнения
            birthPlaceOptions: [],
            registrationPlaceOptions: [],
            residencePlaceOptions: [],
        }
    },
    computed: {
        lang() {
            this.tab = this.localization[this.langStore?.lang]?.page.profile.tabs.personalData
            return this.langStore?.lang
        },
    },
    async created() {
        const authStore = useAuthStore()
        const auth = await authStore.getMe()
        if (auth == null) {
            authStore.deactivateAuth()
        }
        if (auth) {
            let me = { ...auth }
            // Если приходят строки, преобразуем их в объекты для Multiselect
            me.placeOfBirth = me.placeOfBirth
                ? typeof me.placeOfBirth === 'object' && 'label' in me.placeOfBirth
                    ? me.placeOfBirth
                    : { label: me.placeOfBirth }
                : null

            me.registrationPlace = me.registrationPlace
                ? typeof me.registrationPlace === 'object' && 'label' in me.registrationPlace
                    ? me.registrationPlace
                    : { label: me.registrationPlace }
                : null

            me.residencePlace = me.residencePlace
                ? typeof me.residencePlace === 'object' && 'label' in me.residencePlace
                    ? me.residencePlace
                    : { label: me.residencePlace }
                : null

            me.gender = me.gender == 'male' ? 'Мужской' : 'Женский'
            me.maritalStatus = me.maritalStatus == 'single' ? 'Холост/Не замужем' : 'Женат/Замужем'

            this.data = me
            console.log(me)
        }

        // lang
        this.langStore = useLangStore()

        this.tab = this.localization[this.lang]?.page.profile.tabs.trainingInformation
    },
    methods: {
        transliterateToLatin(text) {
            const map = {
                а: 'a',
                б: 'b',
                в: 'v',
                г: 'g',
                д: 'd',
                е: 'e',
                ё: 'yo',
                ж: 'zh',
                з: 'z',
                и: 'i',
                й: 'y',
                к: 'k',
                л: 'l',
                м: 'm',
                н: 'n',
                о: 'o',
                п: 'p',
                р: 'r',
                с: 's',
                т: 't',
                у: 'u',
                ф: 'f',
                х: 'kh',
                ц: 'ts',
                ч: 'ch',
                ш: 'sh',
                щ: 'sch',
                ъ: '',
                ы: 'y',
                ь: '',
                э: 'e',
                ю: 'yu',
                я: 'ya',
            }
            return text
                .split('')
                .map((char) => map[char] || map[char.toLowerCase()]?.toUpperCase() || char)
                .join('')
        },
        fetchAutoComplete(searchTerm, field) {
            console.log('Поисковый запрос:', searchTerm)
            const uri = encodeURIComponent(searchTerm)
            axios
                .get(`${axios.defaults.baseURL}/helper/autocomplete/?term=${uri}`)
                .then((response) => {
                    console.log('Полученные данные:', response.data)
                    if (field === 'birthPlace') {
                        this.birthPlaceOptions = response.data
                    } else if (field === 'registrationPlace') {
                        this.registrationPlaceOptions = response.data
                    } else if (field === 'residencePlace') {
                        this.residencePlaceOptions = response.data
                    }
                })
                .catch((error) => {
                    console.error('Ошибка автозаполнения:', error)
                })
        },
        saveForm() {
            console.log('save')
        },
    },
}
</script>

<style scoped>
textarea {
    padding: 10px;
}
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

.content {
    display: flex;
    justify-content: space-between;
    align-items: stretch; /* вместо flex-start */
    gap: 20px;
    margin-bottom: 25px;
}

.photo-section {
    width: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    padding: 94px 20px;
    border-radius: 10px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}
.photo-section img {
    width: 120px;
    height: 120px;
    border-radius: 10px;
    background: #ddd;
    transform: scale(1.2);
}
.form-section {
    width: 75%;
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}
@media (max-width: 1000px) {
    .content {
        flex-direction: column;
    }
    .photo-section,
    .form-section {
        width: 100%;
    }
}
.form-group {
    display: flex;
    justify-content: space-between;
}

label {
    display: block;
    font-weight: lighter;
    margin-bottom: 5px;
    font-size: 15px !important;
}
input,
select {
    width: 100%;
    padding: 10px;
    background-color: white;
    border: 1px solid #ccc;
    /* border-radius: 4px; */
}
select {
    cursor: pointer;
}
.input-group {
    width: 49%;
    margin-bottom: 15px;
}
.save-button {
    position: absolute;
    right: 20px;
    bottom: 20px;
    background-color: #129c83;
    color: white;
    padding: 10px 25px;
    border-radius: 5px;
    cursor: pointer;
}
.save-button:hover {
    background-color: #108c76;
}
@media (max-width: 1000px) {
    .form-group {
        flex-direction: column;
        width: 100%;
    }
    .input-group {
        width: 100%;
    }
}

/* tab */
.tab {
    width: max-content;
    background-color: white;
    cursor: pointer;
    transition: 0.2s;
    border-radius: 3px;
    font-weight: 500;
}

.tab:hover {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}

.tab.active {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}
</style>

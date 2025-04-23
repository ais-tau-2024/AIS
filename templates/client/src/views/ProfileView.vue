<template>
    <div class="profile-view">
        <LeftPanelComponent class="left-panel" />
        <div class="profile-section p-4" style="overflow-y: scroll !important">
            <h2 class="page-title">{{ localization[lang]?.page.profile.pageTitle }} - {{ tab }}</h2>

            <div class="tabs d-flex">
                <div
                    :class="
                        'tab me-3 ' +
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
                        'tab me-3 ' +
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
                        'tab me-3 ' +
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
                        'tab me-3 ' +
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
                        'tab me-3 ' +
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

            <!-- РАЗДЕЛЫ -->

            <!-- Раздел навыков -->
            <div v-if="tab == localization[lang]?.page.profile.tabs.trainingInformation">
                <div class="form-group">
                    <div class="input-group">
                        <div>
                            <label>{{
                                localization[lang]?.page.profile.trainingInformation.achievements
                            }}</label>
                        </div>
                        <div class="w-100">
                            <textarea
                                name=""
                                id=""
                                style="min-width: 100%; min-height: 100px"
                                disabled
                            ></textarea>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <label>{{
                            localization[lang]?.page.profile.trainingInformation.scienceField
                        }}</label>
                        <input
                            type="text"
                            :value="data.science_fields ? data.science_fields[0].field : ''"
                            disabled
                        />
                    </div>
                    <div class="input-group">
                        <label>{{
                            localization[lang]?.page.profile.trainingInformation.academicDegree
                        }}</label>
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
                        <label>{{
                            localization[lang]?.page.profile.trainingInformation.academicStatus
                        }}</label>
                        <input
                            type="text"
                            :value="
                                data.science_fields ? data.science_fields[0].academicStatus : ''
                            "
                            disabled
                        />
                    </div>
                </div>
                <h3>{{ localization[lang]?.page.profile.trainingInformation.education }}</h3>
                <div class="form-group">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">
                                    <span class="fw-bold">{{
                                        localization[lang]?.page.profile.trainingInformation
                                            .institutionName
                                    }}</span>
                                </th>
                                <th scope="col">
                                    <span class="fw-bold">{{
                                        localization[lang]?.page.profile.trainingInformation
                                            .qualification
                                    }}</span>
                                </th>
                                <th scope="col">
                                    <span class="fw-bold">{{
                                        localization[lang]?.page.profile.trainingInformation
                                            .specialization
                                    }}</span>
                                </th>
                                <th scope="col">
                                    <span class="fw-bold">{{
                                        localization[lang]?.page.profile.trainingInformation
                                            .graduationYear
                                    }}</span>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="education in data.education_records">
                                <tr>
                                    <th scope="row">{{ education.institutionName }}</th>
                                    <td>{{ education.qualification }}</td>
                                    <td>{{ education.specialization }}</td>
                                    <td>{{ education.graduationYear }}</td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Раздел курируемых групп -->
            <div v-if="tab == localization[lang]?.page.profile.tabs.supervisedGroups">
                <template v-for="group in data.groups">
                    <div class="card group mb-2">
                        <div class="card-body">
                            <div
                                class="card-top"
                                @click="
                                    () => {
                                        if (group) {
                                            group.group.visible = !group.group.visible
                                        }
                                    }
                                "
                            >
                                <p>{{ group?.group?.name }}</p>
                                <img :src="'images/right-arrow.png'" alt="" />
                            </div>
                            <div class="mt-3 fs-5" v-if="group?.group?.visible">
                                <div class="mt-1" v-for="student in group?.group?.students">
                                    {{ student.iin }} - {{ student.lastName }}
                                    {{ student.firstName }} {{ student.patronymic }}
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>

            <!-- Раздел контактной информации -->
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

            <!-- Раздел документов -->
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

            <!-- Раздел персональных данных -->
            <div
                v-if="tab == localization[lang]?.page.profile.tabs.personalData"
                class="personal-page"
            >
                <div class="content personal-card">
                    <div class="photo-section">
                        <img
                            :src="
                                data.profilePhoto
                                    ? axiosDefaultsBaseURL + '/' + data.profilePhoto
                                    : data.gender == 'Мужской'
                                      ? '/images/photo-male.jpeg'
                                      : '/images/photo-female.jpeg'
                            "
                            alt="avatar"
                        />
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
                                class="multiselect"
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
                        {{ localization[lang]?.page.profile.personalData.form.registrationAddress }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.registrationPlace
                            }}</label>
                            <Multiselect
                                class="multiselect"
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
                                    .labelRegistrationPlace
                            }}</label>
                            <input type="text" v-model="data.registrationAddress" />
                        </div>
                    </div>

                    <h3>
                        {{ localization[lang]?.page.profile.personalData.form.residentialAddress }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>{{
                                localization[lang]?.page.profile.personalData.form.residencePlace
                            }}</label>
                            <Multiselect
                                class="multiselect"
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
                                    .labelResidencePlace
                            }}</label>
                            <input type="text" v-model="data.residentialAddress" />
                        </div>
                    </div>
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

            tab: null, // Личные данные, Документы, Сведения об обучении, Курируемые группы

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
            return this.langStore?.lang
        },
        tabs() {
            return this.localization[this.lang]?.page.profile.tabs || {}
        },
    },

    watch: {
        lang(newLang, oldLang) {
            const oldTabs = this.localization[oldLang]?.page.profile.tabs || {}
            const newTabs = this.localization[newLang]?.page.profile.tabs || {}

            const currentTabKey = Object.keys(oldTabs).find((key) => oldTabs[key] === this.tab)

            if (currentTabKey) {
                this.tab = newTabs[currentTabKey]
            }
        },
    },

    created() {
        const authStore = useAuthStore()
        authStore.getMe().then((auth) => {
            if (!auth) return authStore.deactivateAuth()

            const me = { ...auth }

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

            me.gender = me.gender === 'male' ? 'Мужской' : 'Женский'
            me.maritalStatus = me.maritalStatus === 'single' ? 'Холост/Не замужем' : 'Женат/Замужем'

            this.data = me
        })

        this.langStore = useLangStore()
        this.tab = this.localization[this.lang]?.page.profile.tabs.personalData

        setTimeout(() => {
            console.log(this.data.groups)
        }, 1500)
    },
    methods: {
        transliterateToLatin(text) {
            const map = {
                а: 'a',
                ә: 'a',
                б: 'b',
                в: 'v',
                г: 'g',
                ғ: 'g',
                д: 'd',
                е: 'e',
                ё: 'yo',
                ж: 'zh',
                з: 'z',
                и: 'i',
                й: 'y',
                к: 'k',
                қ: 'q',
                л: 'l',
                м: 'm',
                н: 'n',
                ң: 'n',
                о: 'o',
                ө: 'o',
                п: 'p',
                р: 'r',
                с: 's',
                т: 't',
                у: 'u',
                ұ: 'u',
                ү: 'u',
                ф: 'f',
                х: 'kh',
                һ: 'h',
                ц: 'ts',
                ч: 'ch',
                ш: 'sh',
                щ: 'sch',
                ъ: '',
                ы: 'y',
                і: 'i',
                ь: '',
                э: 'e',
                ю: 'yu',
                я: 'ya',
            }
            return text
                .split('')
                .map(
                    (char) =>
                        map[char] ??
                        (map[char.toLowerCase()] ? map[char.toLowerCase()].toUpperCase() : char)
                )
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
h2 {
    font-weight: bold;
    color: var(--color-blue);
}

.page-title {
    font-size: 40px;
}

/* Сделать multiselect как обычный input */
::v-deep .multiselect {
    width: 100%;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 22px;
    line-height: 1;
    min-height: auto;
    display: flex;
    align-items: center;
}

::v-deep .multiselect__tags {
    padding: 20px 24px;
    min-height: auto;
    display: flex;
    align-items: center;
    font-size: 22px;
    border: 0;
}

::v-deep .multiselect__single,
::v-deep .multiselect__input {
    margin: 0;
    padding: 0;
    font-size: 22px;
    line-height: 1;
}

::v-deep .multiselect__placeholder {
    font-size: 22px;
    color: #666;
    line-height: 1;
    padding: 0;
    margin: 0;
}

::v-deep .multiselect__select {
    top: 60%;
    transform: translateY(-50%);
    right: 12px;
}

/* ----- TABS ----- */

.tab {
    width: max-content !important;
    padding: 20px 34px;
    margin-bottom: 10px;

    background-color: white;
    color: var(--color-blue);

    cursor: pointer;
    text-align: center;

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

.tabs {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-top: 35px;
    margin-bottom: 25px;
}

.tab {
    flex: 1 0 auto; /* не сжимай, но позволяй перенос */
    white-space: nowrap; /* не переноси текст внутри */
}

/*  */

textarea {
    padding: 10px;
}
.multiselect__select {
    padding: 30px !important;
}
.profile-view {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: stretch;
    justify-content: flex-start;
    overflow: hidden;
}

.profile-section {
    flex-grow: 1;
    height: 100%;
    min-width: 0;
    overflow: hidden;
}

.left-panel {
    min-width: var(--left-panel-width);
    height: 100%;
    flex-shrink: 0; /* Чтобы не сжимался */
}

.content {
    display: flex;
    justify-content: baseline;
    align-items: stretch;
    gap: 20px;
    margin-bottom: 25px;
}

.photo-section {
    min-width: 350px;
    min-height: 350px;
    width: 350px;
    height: 350px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #ffffff;

    border-radius: 10px;
    border: 2px solid black;
}
.photo-section img {
    min-width: calc(350px - 40px);
    min-height: calc(350px - 40px);
    width: calc(350px - 40px);
    height: calc(350px - 40px);
    border-radius: 10px;
    background: #ddd;
}
.form-section {
    width: 100%;
    background: white;
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

    font-weight: 400;
    font-size: 22px !important;
}
input,
select {
    width: 100%;
    padding: 20px 24px;
    background-color: white;
    border: 1px solid #ccc;

    font-weight: 400;
    font-size: 22px !important;
}
select {
    cursor: pointer;
}
.input-group {
    width: 49%;
    margin-bottom: 14px;
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

/* personal-card */

h3 {
    margin-top: 35px !important;
}

.personal-card label {
    font-size: 18px !important;
}

.personal-card input,
.personal-card select {
    font-size: 18px !important;
}

/* card group */

.card.group {
    cursor: pointer;
}

.card.group .card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.card.group .card-top p {
    padding: 0;
    margin: 0;

    font-size: 22px;
}

.card.group .card-top img {
    width: 20px;
}
</style>

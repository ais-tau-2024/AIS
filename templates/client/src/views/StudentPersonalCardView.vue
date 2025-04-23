<template>
    <div class="profile-view">
        <LeftPanelComponent class="left-panel" />
        <div class="profile-section p-4" style="overflow-y: scroll !important">
            <h2 class="fs-3">
                {{ localization[lang]?.page.studentPersonalCard.pageTitle }}
            </h2>
            <hr />
            <div>
                <div class="content">
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
                                <label for="surname">
                                    {{ localization[lang]?.page.studentPersonalCard.form.lastName }}
                                </label>
                                <input readonly type="text" id="surname" v-model="data.lastName" />
                            </div>
                            <div class="input-group">
                                <label for="surname-translit">
                                    {{
                                        localization[lang]?.page.studentPersonalCard.form
                                            .lastNameTranslit
                                    }}
                                </label>
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
                                <label for="name">
                                    {{
                                        localization[lang]?.page.studentPersonalCard.form.firstName
                                    }}
                                </label>
                                <input readonly type="text" id="name" v-model="data.firstName" />
                            </div>
                            <div class="input-group">
                                <label for="name-translit">
                                    {{
                                        localization[lang]?.page.studentPersonalCard.form
                                            .firstNameTranslit
                                    }}
                                </label>
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
                                <label for="patronymic">
                                    {{
                                        localization[lang]?.page.studentPersonalCard.form.patronymic
                                    }}
                                </label>
                                <input
                                    readonly
                                    type="text"
                                    id="patronymic"
                                    v-model="data.patronymic"
                                />
                            </div>
                            <div class="input-group">
                                <label for="patronymic-translit">
                                    {{
                                        localization[lang]?.page.studentPersonalCard.form
                                            .patronymicTranslit
                                    }}
                                </label>
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
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.iin }}
                            </label>
                            <input readonly type="text" v-model="data.iin" />
                        </div>
                        <div class="input-group">
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.birthDate }}
                            </label>
                            <input readonly type="date" v-model="data.birthDate" />
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.nationality }}
                            </label>
                            <select v-model="data.nationality">
                                <option v-for="nat in nationalities" :key="nat">
                                    {{ nat }}
                                </option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.gender }}
                            </label>
                            <select v-model="data.gender">
                                <option v-for="g in genders" :key="g">
                                    {{ g }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form.maritalStatus
                                }}
                            </label>
                            <select v-model="data.maritalStatus">
                                <option v-for="ms in maritalStatuses" :key="ms">
                                    {{ ms }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.citizenship }}
                            </label>
                            <select v-model="data.citizenship">
                                <option v-for="country in countries" :key="country">
                                    {{ country }}
                                </option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form
                                        .countryOfOrigin
                                }}
                            </label>
                            <select v-model="data.countryOfOrigin">
                                <option v-for="country in countries" :key="country">
                                    {{ country }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="input-group">
                        <label>
                            {{ localization[lang]?.page.studentPersonalCard.form.originRegion }}
                        </label>
                        <select v-model="data.originRegion">
                            <option v-for="region in originRegions" :key="region">
                                {{ region }}
                            </option>
                        </select>
                    </div>
                    <h3>
                        {{ localization[lang]?.page.studentPersonalCard.form.labelPlaceOfBirth }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{ localization[lang]?.page.studentPersonalCard.form.placeOfBirth }}
                            </label>
                            <Multiselect
                                readonly
                                v-model="data.placeOfBirth"
                                :options="birthPlaceOptions"
                                label="label"
                                :filterable="true"
                                :placeholder="
                                    localization[lang]?.page.studentPersonalCard.form
                                        .placeOfBirthPlaceholder || 'Введите название'
                                "
                                @search-change="fetchAutoComplete($event, 'birthPlace')"
                            />
                        </div>
                    </div>
                    <h3>
                        {{
                            localization[lang]?.page.studentPersonalCard.form.labelRegistrationPlace
                        }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form
                                        .registrationPlace
                                }}
                            </label>
                            <Multiselect
                                readonly
                                v-model="data.registrationPlace"
                                :options="registrationPlaceOptions"
                                label="label"
                                :filterable="true"
                                :placeholder="
                                    localization[lang]?.page.studentPersonalCard.form
                                        .registrationPlacePlaceholder || 'Введите название'
                                "
                                @search-change="fetchAutoComplete($event, 'registrationPlace')"
                            />
                        </div>
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form
                                        .registrationAddress
                                }}
                            </label>
                            <input readonly type="text" v-model="data.registrationAddress" />
                        </div>
                    </div>
                    <h3>
                        {{ localization[lang]?.page.studentPersonalCard.form.labelResidencePlace }}
                    </h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form.residencePlace
                                }}
                            </label>
                            <Multiselect
                                readonly
                                v-model="data.residencePlace"
                                :options="residencePlaceOptions"
                                label="label"
                                :filterable="true"
                                :placeholder="
                                    localization[lang]?.page.studentPersonalCard.form
                                        .residencePlacePlaceholder || 'Введите название'
                                "
                                @search-change="fetchAutoComplete($event, 'residencePlace')"
                            />
                        </div>
                        <div class="input-group">
                            <label>
                                {{
                                    localization[lang]?.page.studentPersonalCard.form
                                        .residentialAddress
                                }}
                            </label>
                            <input readonly type="text" v-model="data.residentialAddress" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
function normalizeCountryName(name) {
    if (!name) return ''
    return name
        .toLowerCase()
        .replace(/^\s+|\s+$/g, '') // убрать пробелы по краям
        .replace(/(^|\s|-)\S/g, (match) => match.toUpperCase()) // с большой буквы каждое слово/часть
}

import axios from 'axios'
import router from '../router/router'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import LeftPanelComponent from '../components/LeftPanelComponent.vue'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import { useAuthStore } from '../stores/authStore'
axios.defaults.baseURL = 'http://127.0.0.1:8000'

export default {
    name: 'StudentPersonalCardView',
    components: { LeftPanelComponent, Multiselect },
    data() {
        return {
            langStore: null,
            localization: localization,
            axiosDefaultsBaseURL: axios.defaults.baseURL,
            data: {
                id: null, // Уникальный идентификатор (обычно заполняется автоматически)
                profilePhoto: '', // Ссылка на фотографию профиля
                firstName: '', // Имя
                lastName: '', // Фамилия
                patronymic: '', // Отчество
                iin: '', // ИИН (Индивидуальный Идентификационный Номер)
                birthDate: null, // Дата рождения
                gender: null, // Пол (выбирается из genders)
                nationality: null, // Национальность (выбирается из nationalities)
                maritalStatus: null, // Семейное положение (выбирается из maritalStatuses)
                citizenship: null, // Гражданство (выбирается из countries)
                placeOfBirth: null, // Место рождения (выбирается из originRegions)
                registrationPlace: null, // Место регистрации (выбирается из originRegions)
                residencePlace: null, // Место фактического проживания (выбирается из originRegions)
                registrationAddress: '', // Адрес по прописке (текстовое поле)
                residentialAddress: '', // Адрес проживания (текстовое поле)
                documentType: null, // Тип документа (например, паспорт, удостоверение и т.д.)
                documentNumber: null, // Номер документа
                documentIssueDate: null, // Дата выдачи документа
                documentExpiryDate: null, // Срок действия документа
                issuingAuthority: null, // Орган, выдавший документ
                phoneNumber: null, // Мобильный номер телефона
                homePhone: null, // Домашний номер телефона (опционально)
                email: '', // Электронная почта
                teachingLanguage: null, // Язык обучения (казахский, русский и т.д.)
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
                'г. Астана',
                'г. Алматы',
                'г. Шымкент',
                'Акмолинская область',
                'Актюбинская область',
                'Алматинская область',
                'Атырауская область',
                'Восточно-Казахстанская область',
                'Жамбылская область',
                'Западно-Казахстанская область',
                'Карагандинская область',
                'Костанайская область',
                'Кызылординская область',
                'Мангистауская область',
                'Павлодарская область',
                'Северо-Казахстанская область',
                'Туркестанская область',
                'Иная',
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
    },
    async created() {
        const iin = this.$route.params.studentIin // Получаем IIN из маршрута

        if (iin) {
            try {
                const response = await axios.get(`userStudent/${iin}/`, {
                    headers: { auth: localStorage.getItem('ais.auth.token') },
                })

                let me = response.data

                // Преобразуем строки в объекты для Multiselect
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
                me.maritalStatus =
                    me.maritalStatus == 'single' ? 'Холост/Не замужем' : 'Женат/Замужем'
                me.citizenship = normalizeCountryName(me.citizenship)
                me.countryOfOrigin = normalizeCountryName(me.countryOfOrigin)

                this.data = me
                console.log(me)
            } catch (error) {
                console.error('Ошибка при загрузке данных преподавателя:', error)
            }
        } else {
            console.warn('IIN отсутствует в маршруте')
        }

        // lang
        this.langStore = useLangStore()
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
            // Преобразуем объекты Multiselect в строки для отправки на сервер
            // const payload = { ...this.data };
            // payload.placeOfBirth = payload.placeOfBirth ? payload.placeOfBirth.label : null;
            // payload.registrationPlace = payload.registrationPlace ? payload.registrationPlace.label : null;
            // payload.residencePlace = payload.residencePlace ? payload.residencePlace.label : null;

            // axios.put(`${axios.defaults.baseURL}/userTeacher/teacher/${payload.iin}/update/`, payload, {
            //   headers: { auth: localStorage.getItem('ais.auth.token') }
            // })
            // .then(response => {
            //   console.log("Данные успешно сохранены:", response.data);
            // })
            // .catch(error => {
            //   console.error("Ошибка при сохранении данных:", error);
            // });
        },
    },
}
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
    border-radius: 4px;
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
</style>

<template>
	<div class="profile-view">
		<LeftPanelComponent class="left-panel" />
		<div class="profile-section p-4" style="overflow-y: scroll !important;">
			<h2 class="fs-3">Профиль</h2>
			<hr>
			<div>
				<div class="content">
					<div class="photo-section">
						<img :src="axiosDefaultsBaseURL + '/' + data.profilePhoto" alt="avatar">
					</div>
					<div class="form-section">
						<div class="form-group">
							<div class="input-group">
								<label for="surname">ФАМИЛИЯ</label>
								<input type="text" id="surname" v-model="data.lastName">
							</div>
							<div class="input-group">
								<label for="surname-translit">ФАМИЛИЯ ТРАНСЛИТОМ</label>
								<input type="text" id="surname-translit" disabled :value="transliterateToLatin(data.lastName)">
							</div>
						</div>
						<div class="form-group">
							<div class="input-group">
								<label for="name">ИМЯ</label>
								<input type="text" id="name" v-model="data.firstName">
							</div>
							<div class="input-group">
								<label for="name-translit">ИМЯ ТРАНСЛИТОМ</label>
								<input type="text" id="name-translit" disabled :value="transliterateToLatin(data.firstName)">
							</div>
						</div>
						<div class="form-group">
							<div class="input-group">
								<label for="patronymic">ОТЧЕСТВО</label>
								<input type="text" id="patronymic" v-model="data.patronymic">
							</div>
							<div class="input-group">
								<label for="patronymic-translit">ОТЧЕСТВО ТРАНСЛИТОМ</label>
								<input type="text" id="patronymic-translit" disabled :value="transliterateToLatin(data.patronymic)">
							</div>
						</div>
					</div>
				</div>
				<div class="form-container" style="margin-bottom: 50px;">
					<div class="form-group">
						<div class="input-group">
							<label>ИИН</label>
							<input type="text" v-model="data.iin">
						</div>
						<div class="input-group">
							<label>ДАТА РОЖДЕНИЯ</label>
							<input type="date" v-model="data.birthDate">
						</div>
					</div>
					<div class="form-group">
						<div class="input-group">
							<label>НАЦИОНАЛЬНОСТЬ</label>
							<select v-model="data.nationality">
								<option v-for="nat in nationalities" :key="nat">{{ nat }}</option>
							</select>
						</div>
						<div class="input-group">
							<label>ПОЛ</label>
							<select v-model="data.gender">
								<option v-for="g in genders" :key="g">{{ g }}</option>
							</select>
						</div>
					</div>
					<div class="form-group">
						<div class="input-group">
							<label>СЕМЕЙНОЕ ПОЛОЖЕНИЕ</label>
							<select v-model="data.maritalStatus">
								<option v-for="ms in maritalStatuses" :key="ms">{{ ms }}</option>
							</select>
						</div>
					</div>
					<div class="form-group">
						<div class="input-group">
							<label>ГРАЖДАНСТВО</label>
							<select v-model="data.citizenship">
								<option v-for="country in countries" :key="country">{{ country }}</option>
							</select>
						</div>
						<div class="input-group">
							<label>СТРАНА, ОТКУДА ПРИБЫЛ</label>
							<select v-model="data.originCountry">
								<option v-for="country in countries" :key="country">{{ country }}</option>
							</select>
						</div>
					</div>
					<div class="input-group">
						<label>ОБЛАСТЬ, ОТКУДА ПРИБЫЛ</label>
						<select v-model="data.originRegion">
							<option v-for="region in originRegions" :key="region">{{ region }}</option>
						</select>
					</div>
					<h3>Место рождения</h3>
					<div class="form-group">
						<div class="input-group">
							<label>Населенный пункт рождения (КАТО)</label>
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
					<h3>Место прописки</h3>
					<div class="form-group">
						<div class="input-group">
							<label>Населенный пункт прописки (КАТО)</label>
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
                            <label>Адрес прописки</label>
                            <input type="text" v-model="data.registrationAddress">
                        </div>
					</div>
						  
                    <h3>Место проживания</h3>
                    <div class="form-group">
                        <div class="input-group">
                            <label>Населенный пункт проживания (КАТО)</label>
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
                            <label>Адрес проживания</label>
                            <input type="text" v-model="data.residentialAddress">
                        </div>
                    </div>
					<button class="save-button" @click="saveForm">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
</template>

  
<script>
import axios from 'axios';
import router from '../router/router';
import { localization } from '../assets/js/localization';
import LeftPanelComponent from '../components/LeftPanelComponent.vue';
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";
import { useAuthStore } from '../stores/authStore';
axios.defaults.baseURL = 'http://127.0.0.1:8000';

export default {
  name: "StudentPersonalCardView",
  components: { LeftPanelComponent, Multiselect },
  data() {
    return {
      axiosDefaultsBaseURL: axios.defaults.baseURL,
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
        teachingLanguage: null
      },
      nationalities: [/* список национальностей */],
      genders: ['Мужской', 'Женский'],
      maritalStatuses: ['Холост/Не замужем', 'Женат/Замужем'],
      countries: [/* список стран */],
      originRegions: [/* список регионов */],
      // Опции для автозаполнения
      birthPlaceOptions: [],
      registrationPlaceOptions: [],
      residencePlaceOptions: []
    };
  },
  async created() {
    const iin = this.$route.params.studentIin; // Получаем IIN из маршрута

    if (iin) {
        try {
            const response = await axios.get(`userStudent/${iin}/`, {
                headers: { auth: localStorage.getItem('ais.auth.token') }
            });

            let me = response.data;

            // Преобразуем строки в объекты для Multiselect
            me.placeOfBirth = me.placeOfBirth 
                ? (typeof me.placeOfBirth === 'object' && 'label' in me.placeOfBirth 
                    ? me.placeOfBirth 
                    : { label: me.placeOfBirth }) 
                : null;

            me.registrationPlace = me.registrationPlace 
                ? (typeof me.registrationPlace === 'object' && 'label' in me.registrationPlace 
                    ? me.registrationPlace 
                    : { label: me.registrationPlace }) 
                : null;

            me.residencePlace = me.residencePlace 
                ? (typeof me.residencePlace === 'object' && 'label' in me.residencePlace 
                    ? me.residencePlace 
                    : { label: me.residencePlace }) 
                : null;

            this.data = me;
            console.log(me);
        } catch (error) {
            console.error("Ошибка при загрузке данных преподавателя:", error);
        }
    } else {
        console.warn("IIN отсутствует в маршруте");
    }
},

  methods: {
    transliterateToLatin(text) {
      const map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
      };
      return text.split('').map(char =>
        map[char] || map[char.toLowerCase()]?.toUpperCase() || char
      ).join('');
    },
    fetchAutoComplete(searchTerm, field) {
      console.log("Поисковый запрос:", searchTerm);
      const uri = encodeURIComponent(searchTerm);
      axios.get(`${axios.defaults.baseURL}/helper/autocomplete/?term=${uri}`)
        .then(response => {
          console.log("Полученные данные:", response.data);
          if (field === 'birthPlace') {
            this.birthPlaceOptions = response.data;
          } else if (field === 'registrationPlace') {
            this.registrationPlaceOptions = response.data;
          } else if (field === 'residencePlace') {
            this.residencePlaceOptions = response.data;
          }
        })
        .catch(error => {
          console.error("Ошибка автозаполнения:", error);
        });
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
    }
  }
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
input, select {
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
  background-color: #129C83;
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

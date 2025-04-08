<template>
    <NotificationComponent ref="notifier" />
    <div class="storage-view">
        <LeftPanelComponent class="left-panel" />

        <div class="storage-section p-4">
            <!-- Главная страница -->
            <div v-if="!currentWorkspace" id="home-page">
                <h2 class="fs-3">{{ localization[lang]?.page.storage.pageTitle }}</h2>
                <hr />
                <ul class="workspace-list mb-0 pb-1">
                    <li v-for="ws in workspaces" :key="ws.id" @click="openWorkspace(ws.id)">
                        {{ ws.name }}
                        <div class="workspace-actions">
                            <!-- Кнопка открытия модалки -->
                            <button
                                class="btn btn-info p-2 px-4"
                                @click.stop="openGrantAccessModal(ws.id)"
                                v-if="ws.isOwner == true || ws.isOwner == undefined"
                            >
                                {{ localization[lang]?.page.storage.home.buttonSettings }}
                            </button>
                            <button
                                class="btn btn-success p-2 px-4"
                                @click.stop="renameWorkspace(ws.id, ws.name)"
                            >
                                {{ localization[lang]?.page.storage.home.buttonRename }}
                            </button>
                            <button
                                class="btn btn-danger p-2 px-4"
                                @click.stop="deleteWorkspace(ws.id)"
                            >
                                {{ localization[lang]?.page.storage.home.buttonDelete }}
                            </button>
                        </div>
                    </li>
                </ul>
                <button @click="createWorkspace" class="btn btn-primary w-100">
                    {{ localization[lang]?.page.storage.home.buttonCreate }}
                </button>
            </div>

            <!-- Страница активного рабочего стола -->
            <div v-else id="workspace-page">
                <h2 class="fs-3">{{ localization[lang]?.page.storage.activeWorkspace.title }}</h2>
                <hr />
                <div class="breadcrumbs">
                    <span
                        @click="navigateToFolder('')"
                        @dragover.prevent
                        @drop="handleDropOnBreadcrumb('', $event)"
                        >Home</span
                    >
                    <template v-for="(part, index) in currentPathParts" :key="index">
                        /
                        <span
                            @click="navigateToFolder(currentPathUpTo(index))"
                            @dragover.prevent
                            @drop="handleDropOnBreadcrumb(currentPathUpTo(index), $event)"
                        >
                            {{ part }}
                        </span>
                    </template>
                </div>
                <ul class="file-list">
                    <li
                        v-for="dir in directories"
                        :key="dir"
                        draggable="true"
                        @dblclick="enterFolder(dir)"
                        @dragstart="handleDragStartFolder(dir)"
                        @dragover.prevent
                        @drop="handleDropOnFolder(dir)"
                    >
                        📁 {{ dir }}
                        <div class="folder-actions" @click.stop>
                            <button class="btn btn-danger" @click="deleteFolder(dir)">
                                {{ localization[lang]?.page.storage.activeWorkspace.buttonDelete }}
                            </button>
                        </div>
                    </li>
                    <li
                        v-for="file in files"
                        :key="file.name"
                        draggable="true"
                        @dragstart="handleDragStart(file)"
                    >
                        📄 {{ file.name }}
                        <div class="file-actions" @click.stop>
                            <button
                                class="btn btn-primary"
                                v-if="
                                    file.type == '.png' ||
                                    file.type == '.jpg' ||
                                    file.type == '.jpeg' ||
                                    file.type == '.webp' ||
                                    file.type == '.webp' ||
                                    file.type == '.webp'
                                "
                                @click="openFile(file)"
                            >
                                {{ localization[lang]?.page.storage.activeWorkspace.buttonOpen }}
                            </button>
                            <button class="btn btn-success" @click="downloadFile(file)">
                                {{
                                    localization[lang]?.page.storage.activeWorkspace.buttonDownload
                                }}
                            </button>
                            <button class="btn btn-danger" @click="deleteFile(file)">
                                {{ localization[lang]?.page.storage.activeWorkspace.buttonDelete }}
                            </button>
                        </div>
                    </li>
                </ul>
                <div class="actions">
                    <button @click="createFolder">
                        {{ localization[lang]?.page.storage.activeWorkspace.createFolder }}
                    </button>
                    <div
                        class="dropzone"
                        @dragover.prevent
                        @dragenter.prevent
                        @drop="handleDrop"
                        @click="triggerFileInput"
                    >
                        <p class="p-0 m-0">
                            {{ localization[lang]?.page.storage.activeWorkspace.dragAndDrop }}
                        </p>
                        <input
                            type="file"
                            multiple
                            @change="handleFileSelect"
                            ref="fileInput"
                            hidden
                        />
                    </div>
                    <button @click="goHome">
                        {{ localization[lang]?.page.storage.activeWorkspace.atHome }}
                    </button>
                </div>
            </div>

            <!-- Модальное окно для предоставления доступа -->
            <div v-if="showGrantAccessModal" class="modal" @click="closeGrantModal">
                <div class="modal-content w-50" @click.stop="">
                    <h3 class="fs-3 m-0 p-0">
                        {{ localization[lang]?.page.storage.modalSettings.title }}
                    </h3>
                    <hr />
                    <select v-model="selectedTeacher" class="mb-2 form-select">
                        <option value="" disabled>
                            {{ localization[lang]?.page.storage.modalSettings.selectTeacherOption }}
                        </option>
                        <option v-for="teacher in availableTeachers.available_teachers">
                            {{
                                teacher.iin +
                                ' ' +
                                teacher.firstName +
                                ' ' +
                                teacher.lastName +
                                ' ' +
                                (teacher.patronymic == null ? '' : teacher.patronymic)
                            }}
                        </option>
                    </select>
                    <div class="">
                        <h5 class="fs-5">
                            {{
                                localization[lang]?.page.storage.modalSettings
                                    .teacherListWithAccessTitle
                            }}
                        </h5>
                        <div class="card" style="max-height: 400px; overflow-y: auto">
                            <div class="card-body py-2 pe-2">
                                <div
                                    v-for="teacher in availableTeachers.granted_teachers"
                                    :key="teacher.id"
                                    class="mb-2 d-flex justify-content-between align-items-center w-100"
                                >
                                    <p class="p-0 m-0">
                                        {{
                                            teacher.iin +
                                            ' ' +
                                            teacher.firstName +
                                            ' ' +
                                            teacher.lastName +
                                            ' ' +
                                            (teacher.patronymic == null ? '' : teacher.patronymic)
                                        }}
                                    </p>
                                    <button
                                        @click.stop="
                                            () => {
                                                this.revokeAccess(teacher.iin)
                                            }
                                        "
                                        class="btn btn-danger px-3 m-0"
                                    >
                                        {{
                                            localization[lang]?.page.storage.modalSettings
                                                .buttonDelete
                                        }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <button @click="grantAccess" class="btn btn-success me-1 px-4">
                            {{ localization[lang]?.page.storage.modalSettings.buttonProvide }}
                        </button>
                        <button @click="closeGrantModal" class="btn btn-secondary px-4">
                            {{ localization[lang]?.page.storage.modalSettings.buttonCancel }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- Модальное окно для просмотра файла -->
            <div v-if="showFileModal" class="file-viewer" @click.self="closeFileModal">
                <div class="file-viewer-content">
                    <button class="file-viewer-close" @click="closeFileModal">X</button>
                    <div class="content">
                        <template v-if="fileModalType === 'image'">
                            <img
                                :src="fileModalUrl"
                                alt="Изображение"
                                style="max-width: 100%; max-height: 100%"
                            />
                        </template>
                        <template v-else-if="fileModalType === 'text'">
                            <pre>{{ fileModalContent }}</pre>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import { useAuthStore } from '../stores/authStore'
import LeftPanelComponent from '../components/LeftPanelComponent.vue'
import NotificationComponent from '../components/NotificationComponent.vue'

// Настройка базового URL (например, http://localhost:8000/api)
const axiosDefaultsBaseURL = 'http://localhost:8000/fileManager'

export default {
    name: 'StorageView',
    components: { LeftPanelComponent, NotificationComponent },
    data() {
        return {
            langStore: null,
            localization: localization,

            workspaces: [], // [{ id, name, owner }, ...]
            currentWorkspace: null, // desktop id
            currentPath: '', // например, 'folder1/folder2'
            directories: [],
            files: [],

            grantAccessWorkspace: null,
            showGrantAccessModal: false,
            availableTeachers: [],
            selectedTeacher: '',

            // Данные для просмотра файла
            showFileModal: false,
            fileModalType: '', // 'image' или 'text'
            fileModalUrl: '',
            fileModalContent: '',
        }
    },
    computed: {
        lang() {
            return this.langStore?.lang
        },
        currentPathParts() {
            return this.currentPath ? this.currentPath.split('/') : []
        },
    },
    async created() {
        const authStore = useAuthStore()
        const auth = await authStore.getMe()
        if (auth == null) {
            authStore.deactivateAuth()
        }

        // lang
        this.langStore = useLangStore()

        //
        this.fetchDesktops()
        // Если в маршруте передан storageId, открываем его
        const storageId = this.$route.params.storageId
        if (storageId) {
            this.openWorkspace(storageId)
        }
    },
    watch: {
        $route(to) {
            const storageId = to.params.storageId
            if (!storageId) {
                // Если ушли с маршрута рабочего стола, сбрасываем состояние
                this.currentWorkspace = null
                this.currentPath = ''
                this.directories = []
                this.files = []
            }
        },
    },
    methods: {
        addNotification(notification, status) {
            console.log(notification, status)
            this.$refs.notifier.addNotification({ message: notification, status: status })
        },
        openGrantAccessModal(desktopId) {
            // Не меняем currentWorkspace, чтобы home-page оставался видимым
            this.grantAccessWorkspace = desktopId
            this.showGrantAccessModal = true
            this.fetchAvailableTeachers()
        },
        async fetchAvailableTeachers() {
            try {
                const res = await axios.get(`${axiosDefaultsBaseURL}/teachers/available/`, {
                    params: { desktop_id: this.grantAccessWorkspace },
                    headers: {
                        auth: localStorage.getItem('ais.auth.token'),
                    },
                })
                this.availableTeachers = res.data
                console.log(this.availableTeachers)
                // if (this.availableTeachers.length) {
                // 	this.selectedTeacher = this.availableTeachers[0].id;
                // }
            } catch (err) {
                console.error('Ошибка получения списка преподавателей', err)
            }
        },
        async grantAccess() {
            if (this.selectedTeacher == '') {
                this.addNotification('Выберите преподавателя', 400)
                return
            }
            try {
                console.log(String(this.selectedTeacher).split(' ')[0])
                await axios.post(
                    `${axiosDefaultsBaseURL}/desktops/${this.grantAccessWorkspace}/grant/`,
                    { teacher_id: String(this.selectedTeacher).split(' ')[0] },
                    {
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                    }
                )
                this.addNotification('Доступ предоставлен', 200)
                this.fetchAvailableTeachers()
                this.selectedTeacher = ''
                // this.closeGrantModal()
            } catch (error) {
                console.error('Ошибка предоставления доступа', error)
            }
        },
        async revokeAccess(teacherIin) {
            try {
                await axios.delete(
                    `${axiosDefaultsBaseURL}/desktops/${this.grantAccessWorkspace}/revoke/`,
                    {
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                        data: {
                            teacher_id: teacherIin,
                        },
                    }
                )
                this.addNotification('Доступ удалён', 200)
                this.fetchAvailableTeachers()
            } catch (error) {
                console.error('Ошибка удаления доступа', error)
            }
        },
        closeGrantModal() {
            this.showGrantAccessModal = false
            this.grantAccessWorkspace = null
        },

        async fetchDesktops() {
            try {
                const res = await axios.get(axiosDefaultsBaseURL + '/desktops/list/', {
                    headers: {
                        auth: localStorage.getItem('ais.auth.token'),
                    },
                })
                this.workspaces = res.data
            } catch (err) {
                console.error('Ошибка получения рабочих столов', err)
            }
        },
        async createWorkspace() {
            const name = prompt(
                this.localization[this.lang].page.storage.prompt.enterTheNameOfTheDesktop
            )
            if (name) {
                try {
                    const res = await axios.post(
                        axiosDefaultsBaseURL + '/desktops/',
                        { name },
                        {
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                        }
                    )
                    // Добавляем новый рабочий стол в список
                    this.workspaces.push(res.data)
                } catch (err) {
                    console.error('Ошибка создания рабочего стола', err)
                }
            }
        },
        async deleteWorkspace(desktopId) {
            if (confirm(this.localization[this.lang].page.storage.confirm.deleteTheDesktop)) {
                try {
                    await axios.delete(axiosDefaultsBaseURL + `/desktops/${desktopId}/`, {
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                    })
                    this.workspaces = this.workspaces.filter((ws) => ws.id !== desktopId)
                    if (this.currentWorkspace == desktopId) {
                        this.goHome()
                    }
                } catch (err) {
                    console.error('Ошибка удаления рабочего стола', err)
                }
            }
        },
        async renameWorkspace(desktopId, oldName) {
            console.log(this.lang)
            console.log(this.localization[this.lang].page.storage.prompt)
            const newName = prompt(
                this.localization[this.lang].page.storage.prompt.enterANewDesktopName,
                oldName
            )
            if (newName && newName !== oldName) {
                try {
                    // Для переименования можно реализовать API (например, через FileActionView/PUT)
                    await axios.put(
                        axiosDefaultsBaseURL + `/desktops/${desktopId}/file/`,
                        { old_path: oldName, new_name: newName },
                        {
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                        }
                    )
                    // Обновляем локальный список
                    this.fetchDesktops()
                } catch (err) {
                    console.error('Ошибка переименования рабочего стола', err)
                }
            }
        },
        async openWorkspace(desktopId) {
            this.currentWorkspace = desktopId
            this.currentPath = ''
            this.$router.push({ path: `/storage/${desktopId}` })
            this.fetchFiles()
        },
        async fetchFiles() {
            try {
                const res = await axios.get(
                    axiosDefaultsBaseURL + `/desktops/${this.currentWorkspace}/files/`,
                    {
                        params: { path: this.currentPath },
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                    }
                )
                this.directories = res.data.directories
                this.files = res.data.files
            } catch (err) {
                console.error('Ошибка получения файлов', err)
            }
        },
        async deleteFolder(folder) {
            if (confirm(this.localization[this.lang].page.storage.confirm.deleteFolder)) {
                try {
                    await axios.delete(
                        `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                        {
                            data: {
                                path: `${this.currentPath ? this.currentPath + '/' : ''}${folder}`,
                            },
                            headers: { auth: localStorage.getItem('ais.auth.token') },
                        }
                    )
                    this.fetchFiles()
                    this.addNotification('Папка удалена', 200)
                } catch (error) {
                    console.error('Ошибка удаления папки', error)
                    this.addNotification('Ошибка удаления папки', 500)
                }
            }
        },
        navigateToFolder(path) {
            this.currentPath = path
            this.fetchFiles()
        },
        currentPathUpTo(index) {
            const parts = this.currentPathParts
            return parts.slice(0, index + 1).join('/')
        },
        async enterFolder(folderName) {
            this.currentPath = this.currentPath ? `${this.currentPath}/${folderName}` : folderName
            this.fetchFiles()
        },
        async createFolder() {
            const folderName = prompt(
                this.localization[this.lang].page.storage.prompt.enterTheFolderName
            )
            if (folderName) {
                // Путь, где создается папка
                const path = this.currentPath ? `${this.currentPath}/${folderName}` : folderName
                try {
                    await axios.post(
                        axiosDefaultsBaseURL + `/desktops/${this.currentWorkspace}/createFolder/`,
                        { path },
                        {
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                        }
                    )
                    this.fetchFiles()
                } catch (err) {
                    console.error('Ошибка создания папки', err)
                }
            }
        },
        // Открытие файлового диалога при клике на dropzone
        triggerFileInput() {
            this.$refs.fileInput.click()
        },

        // Обработка перетаскивания файлов
        async handleDrop(event) {
            event.preventDefault()
            const files = event.dataTransfer.files
            await this.uploadFiles(files)
        },

        // Обработка выбора файла через input
        async handleFileSelect(event) {
            const files = event.target.files
            await this.uploadFiles(files)
        },

        // Загрузка нескольких файлов
        async uploadFiles(files) {
            if (!files.length) return

            const token = localStorage.getItem('ais.auth.token')
            const formData = new FormData()

            for (let file of files) {
                formData.append('file', file)
            }
            formData.append('path', this.currentPath)

            try {
                await axios.post(
                    `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/upload/`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            auth: token,
                        },
                    }
                )
                this.fetchFiles() // Обновляем список файлов после загрузки
            } catch (err) {
                console.error('Ошибка загрузки файла', err)
            }
        },
        async deleteFile(file) {
            if (confirm(this.localization[this.lang].page.storage.confirm.deleteFile)) {
                try {
                    await axios.delete(
                        `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                        {
                            data: { path: `${this.currentPath}/${file.name}` },
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                        }
                    )
                    this.fetchFiles()
                } catch (err) {
                    this.addNotification('Ошибка удаления файла', 500)
                }
            }
        },
        async downloadFile(file) {
            try {
                const response = await axios.get(
                    `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                    {
                        params: {
                            path: `${this.currentPath}/${file.name}`,
                            download: true,
                        },
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                        responseType: 'blob', // Указываем, что ожидаем бинарные данные
                    }
                )

                // Создаем URL из бинарных данных
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', file.name) // Указываем имя файла
                document.body.appendChild(link)
                link.click()

                // Удаляем временный объект URL
                window.URL.revokeObjectURL(url)
                document.body.removeChild(link)

                this.addNotification('Файл скачен', 100)
            } catch (error) {
                console.error('Ошибка скачивания файла', error)
                this.addNotification('Не удалось скачать файл', 500)
            }
        },
        goHome() {
            this.currentWorkspace = null
            this.currentPath = ''
            this.directories = []
            this.files = []
            this.$router.push('/storage')
        },

        async openFile(file) {
            console.log('Открываем файл:', file)
            const extension = file.name.split('.').pop().toLowerCase()
            const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

            if (imageExtensions.includes(extension)) {
                try {
                    // Получаем изображение через axios
                    const response = await axios.get(
                        `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                        {
                            params: {
                                path: `${this.currentPath}/${file.name}`,
                            },
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                            responseType: 'blob', // Получаем данные в бинарном формате
                        }
                    )

                    // Создаем временный URL для blob-объекта
                    this.fileModalType = 'image'
                    this.fileModalUrl = URL.createObjectURL(response.data)
                    this.showFileModal = true
                } catch (error) {
                    console.error('Ошибка загрузки изображения', error)
                    this.addNotification('Не удалось открыть изображение', 500)
                }
            } else {
                // Для текстовых файлов
                try {
                    const response = await axios.get(
                        `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                        {
                            params: {
                                path: `${this.currentPath}/${file.name}`,
                            },
                            headers: {
                                auth: localStorage.getItem('ais.auth.token'),
                            },
                            responseType: 'text',
                        }
                    )

                    this.fileModalType = 'text'
                    this.fileModalContent = response.data
                    this.showFileModal = true
                } catch (error) {
                    console.error('Ошибка загрузки текстового файла', error)
                    this.addNotification('Не удалось открыть файл', 500)
                }
            }
        },

        closeFileModal() {
            this.showFileModal = false
            this.fileModalType = ''
            this.fileModalUrl = ''
            this.fileModalContent = ''
        },

        handleDragStart(item) {
            event.dataTransfer.setData('itemName', item.name ? item.name : item)
            event.dataTransfer.setData('itemType', 'file')
        },
        handleDragStartFolder(dir) {
            event.dataTransfer.setData('itemName', dir)
            event.dataTransfer.setData('itemType', 'folder')
        },
        handleDropOnFolder(targetFolder) {
            const itemName = event.dataTransfer.getData('itemName')
            if (!itemName) return
            // Формируем старый путь (из текущей директории)
            const oldPath = this.currentPath ? `${this.currentPath}/${itemName}` : itemName
            // Новый путь – целевая папка (относительно корня рабочего стола)
            const destination = this.currentPath
                ? `${this.currentPath}/${targetFolder}`
                : targetFolder
            axios
                .put(
                    `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                    {
                        old_path: oldPath,
                        destination: destination,
                    },
                    {
                        headers: {
                            auth: localStorage.getItem('ais.auth.token'),
                        },
                    }
                )
                .then((response) => {
                    this.fetchFiles()
                    this.addNotification('Файл/папка перемещены', 200)
                })
                .catch((error) => {
                    console.error('Ошибка перемещения файла', error)
                    this.addNotification('Ошибка перемещения файла', 500)
                })
        },
        handleDropOnBreadcrumb(destinationPath, event) {
            event.preventDefault()
            const itemName = event.dataTransfer.getData('itemName')
            const itemType = event.dataTransfer.getData('itemType')

            if (!itemName) return

            // Если destinationPath пустой (для "Главная"), он должен быть просто корнем
            const newDestination = destinationPath || '/'

            axios
                .put(
                    `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
                    {
                        old_path: this.currentPath ? `${this.currentPath}/${itemName}` : itemName,
                        destination: newDestination,
                    },
                    {
                        headers: { auth: localStorage.getItem('ais.auth.token') },
                    }
                )
                .then((response) => {
                    this.fetchFiles() // Перезагрузка файлов
                    this.addNotification('Файл/папка перемещены', 200)
                })
                .catch((error) => {
                    console.error('Ошибка перемещения:', error)
                    this.addNotification('Ошибка перемещения файла', 500)
                })
        },
    },
}
</script>

<style scoped>
.storage-view {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: stretch; /* Растянет дочерние элементы */
    justify-content: flex-start; /* Исключит центрирование */
    overflow: hidden; /* Убирает возможную прокрутку */
}

.storage-section {
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

.workspace-list,
.file-list {
    list-style: none;
    padding: 0;
}
.workspace-list li,
.file-list li {
    background: #ffffff;
    margin: 5px 0;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
}
/* .workspace-list li:hover, */
/* .file-list li:hover { */
/* } */
.breadcrumbs {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
}
.breadcrumbs span {
    cursor: pointer;
    color: #3498db;
    margin: 0 5px;
}
.breadcrumbs span:hover {
    text-decoration: underline;
}
.breadcrumbs span::after {
    /* content: " / ";/ */
    color: #333;
}
.breadcrumbs span:last-child::after {
    content: '';
}
.actions {
    display: flex;
    gap: 10px;
}
.actions button {
    padding: 8px 16px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.2s;
}
.actions button:hover {
    background-color: #2980b9;
}
.dropzone {
    border: 2px dashed #409eff;
    background-color: #f0f7ff;
    color: #409eff;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.dropzone:hover {
    background-color: #e6f0ff;
}
.workspace-actions {
    display: flex;
    gap: 5px;
}
.workspace-actions button {
    padding: 5px 10px;
    cursor: pointer;
}
.file-actions {
    display: flex;
    gap: 5px;
}
/* .file-actions button {
	padding: 5px 10px;
	background-color: #3498db;
	color: white;
	border: none;
	border-radius: 3px;
	cursor: pointer;
	transition: background 0.2s;
}
.file-actions button:hover {
	background-color: #2980b9;
} */
.modal {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
}
.modal-content button {
    margin-top: 10px;
}
.folder-list {
    list-style: none;
    padding: 0;
}
.folder-list li {
    padding: 10px;
    border: 1px solid #ddd;
    margin: 5px 0;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.2s;
}
.folder-list li:hover {
    background: #f0f0f0;
}
.file-viewer {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    justify-content: center;
    align-items: center;
}
.file-viewer-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 80%;
    max-height: 80%;
    overflow: hidden; /* Убираем прокрутку */
    position: relative;
    display: flex;
    flex-direction: column; /* Выравнивание контента по вертикали */
    align-items: center; /* Центрирование контента */
}

.file-viewer-content .content {
    width: 100%;
    max-height: 80vh;
    overflow-y: auto;
}
.file-viewer-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
}

/* Стили для модального окна просмотра файла */
.file-viewer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.file-viewer-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 80%;
    max-height: 80%;
    overflow: auto;
    position: relative;
}

.file-viewer-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
}
</style>

<template>
  <div class="storage-view">
    <LeftPanelComponent class="left-panel" />
    <div class="storage-section p-4">
      <!-- Главная страница -->
      <div v-if="!currentWorkspace" id="home-page">
        <h2 class="fs-3">Мои рабочие столы</h2>
        <hr>
        <ul class="workspace-list mb-0 pb-1">
          <li v-for="ws in workspaces" :key="ws.id" @click="openWorkspace(ws.id)">
            {{ ws.name }}
            <div class="workspace-actions" @click.stop>
              <button class="rename" @click="renameWorkspace(ws.id, ws.name)">Переименовать</button>
              <button @click="deleteWorkspace(ws.id)">Удалить</button>
            </div>
          </li>
        </ul>
        <button @click="createWorkspace" class="btn btn-primary w-100">Создать рабочий стол</button>
      </div>

      <!-- Страница активного рабочего стола -->
      <div v-else id="workspace-page">
        <h2 class="fs-3">Активный рабочий стол</h2>
        <hr>
        <div class="breadcrumbs">
          <span @click="navigateToFolder('')">Главная</span>
          <template v-for="(part, index) in currentPathParts" :key="index">
            <span @click="navigateToFolder(currentPathUpTo(index))">{{ part }}</span>
          </template>
        </div>
        <ul class="file-list">
          <li v-for="dir in directories" :key="dir" @dblclick="enterFolder(dir)">
            📁 {{ dir }}
          </li>
          <li v-for="file in files" :key="file.name">
            📄 {{ file.name }}
            <div class="file-actions" @click.stop>
              <button @click="openFile(file)">Открыть</button>
              <button @click="deleteFile(file)">Удалить</button>
            </div>
          </li>
        </ul>
        <div class="actions">
          <button @click="createFolder">Создать папку</button>
          <div
            class="dropzone"
            @dragover.prevent
            @dragenter.prevent
            @drop="handleDrop"
            @click="triggerFileInput"
          >
            <p class="p-0 m-0">Перетащите файлы сюда для загрузки</p>
            <input type="file" multiple @change="handleFileSelect" ref="fileInput" hidden />
          </div>
          <button @click="goHome">На главную</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LeftPanelComponent from '../components/LeftPanelComponent.vue'

// Настройка базового URL (например, http://localhost:8000/api)
const axiosDefaultsBaseURL = 'http://localhost:8000/fileManager';

export default {
  name: "StorageView",
  components: { LeftPanelComponent },
  data() {
    return {
      workspaces: [],         // [{ id, name, owner }, ...]
      currentWorkspace: null, // desktop id
      currentPath: '',        // например, 'folder1/folder2'
      directories: [],
      files: [],
      // Дополнительно можно хранить для редактирования, загрузок и т.п.
    }
  },
  computed: {
    currentPathParts() {
      return this.currentPath ? this.currentPath.split('/') : [];
    }
  },
  created() {
    this.fetchDesktops();
    // Если в маршруте передан storageId, открываем его
    const storageId = this.$route.params.storageId;
    if (storageId) {
      this.openWorkspace(storageId);
    }
  },
  watch: {
    '$route'(to) {
      const storageId = to.params.storageId;
      if (!storageId) {
        // Если ушли с маршрута рабочего стола, сбрасываем состояние
        this.currentWorkspace = null;
        this.currentPath = '';
        this.directories = [];
        this.files = [];
      }
    }
  },
  methods: {
    async fetchDesktops() {
      try {
        const res = await axios.get(axiosDefaultsBaseURL+'/desktops/list/', {
              headers: { auth: localStorage.getItem('ais.auth.token') }
          });
        this.workspaces = res.data;
      } catch (err) {
        console.error('Ошибка получения рабочих столов', err);
      }
    },
    async createWorkspace() {
      const name = prompt("Введите название рабочего стола");
      if (name) {
        try {
          const res = await axios.post(axiosDefaultsBaseURL+'/desktops/', { name }, { headers: { auth: localStorage.getItem('ais.auth.token') } });
          // Добавляем новый рабочий стол в список
          this.workspaces.push(res.data);
        } catch (err) {
          console.error('Ошибка создания рабочего стола', err);
        }
      }
    },
    async deleteWorkspace(desktopId) {
      if (confirm("Удалить рабочий стол?")) {
        try {
          await axios.delete(axiosDefaultsBaseURL+`/desktops/${desktopId}/`, {
              headers: { auth: localStorage.getItem('ais.auth.token') }
          });
          this.workspaces = this.workspaces.filter(ws => ws.id !== desktopId);
          if (this.currentWorkspace == desktopId) {
            this.goHome();
          }
        } catch (err) {
          console.error('Ошибка удаления рабочего стола', err);
        }
      }
    },
    async renameWorkspace(desktopId, oldName) {
      const newName = prompt("Введите новое название рабочего стола", oldName);
      if (newName && newName !== oldName) {
        try {
          // Для переименования можно реализовать API (например, через FileActionView/PUT)
          await axios.put(axiosDefaultsBaseURL+`/desktops/${desktopId}/file/`, { old_path: oldName, new_name: newName },
          { headers: { auth: localStorage.getItem('ais.auth.token') } });
          // Обновляем локальный список
          this.fetchDesktops();
        } catch (err) {
          console.error('Ошибка переименования рабочего стола', err);
        }
      }
    },
    async openWorkspace(desktopId) {
      this.currentWorkspace = desktopId;
      this.currentPath = '';
      this.$router.push({ path: `/storage/${desktopId}` });
      this.fetchFiles();
    },
    async fetchFiles() {
      try {
        const res = await axios.get(axiosDefaultsBaseURL+`/desktops/${this.currentWorkspace}/files/`, {
          params: { path: this.currentPath },
          headers: { auth: localStorage.getItem('ais.auth.token') }
        });
        this.directories = res.data.directories;
        this.files = res.data.files;
      } catch (err) {
        console.error('Ошибка получения файлов', err);
      }
    },
    navigateToFolder(path) {
      this.currentPath = path;
      this.fetchFiles();
    },
    currentPathUpTo(index) {
      const parts = this.currentPathParts;
      return parts.slice(0, index + 1).join('/');
    },
    async enterFolder(folderName) {
      this.currentPath = this.currentPath ? `${this.currentPath}/${folderName}` : folderName;
      this.fetchFiles();
    },
    async createFolder() {
      const folderName = prompt("Введите название папки");
      if (folderName) {
        // Путь, где создается папка
        const path = this.currentPath ? `${this.currentPath}/${folderName}` : folderName;
        try {
          await axios.post(axiosDefaultsBaseURL+`/desktops/${this.currentWorkspace}/createFolder/`, { path },
          { headers: { auth: localStorage.getItem('ais.auth.token') } });
          this.fetchFiles();
        } catch (err) {
          console.error('Ошибка создания папки', err);
        }
      }
    },
    // Открытие файлового диалога при клике на dropzone
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    // Обработка перетаскивания файлов
    async handleDrop(event) {
      event.preventDefault();
      const files = event.dataTransfer.files;
      await this.uploadFiles(files);
    },

    // Обработка выбора файла через input
    async handleFileSelect(event) {
      const files = event.target.files;
      await this.uploadFiles(files);
    },

    // Загрузка нескольких файлов
    async uploadFiles(files) {
      if (!files.length) return;
      
      const token = localStorage.getItem("ais.auth.token");
      const formData = new FormData();

      for (let file of files) {
        formData.append("file", file);
      }
      formData.append("path", this.currentPath);

      try {
        await axios.post(
          `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/upload/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              auth: token,
            },
          }
        );
        this.fetchFiles(); // Обновляем список файлов после загрузки
      } catch (err) {
        console.error("Ошибка загрузки файла", err);
      }
    },
    async deleteFile(file) {
      if (confirm("Удалить файл?")) {
        try {
          await axios.delete(
            `${axiosDefaultsBaseURL}/desktops/${this.currentWorkspace}/file/`,
            {
              data: { path: `${this.currentPath}/${file.name}` },
              headers: { auth: localStorage.getItem('ais.auth.token') }
            }
          );
          this.fetchFiles();
        } catch (err) {
          console.error('Ошибка удаления файла', err);
        }
      }
    },
    goHome() {
      this.currentWorkspace = null;
      this.currentPath = '';
      this.directories = [];
      this.files = [];
      this.$router.push('/storage');
    },
    openFile(file) {
      // Здесь можно реализовать просмотр файла (например, получение blob-объекта или URL)
      console.log("Открыть файл", file);
    }
  }
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

.workspace-list, .file-list {
  list-style: none;
  padding: 0;
}
.workspace-list li, .file-list li {
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
.workspace-list li:hover, .file-list li:hover {
  background: #e9ecef;
}
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
  content: " / ";
  color: #333;
}
.breadcrumbs span:last-child::after {
  content: "";
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
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.2s;
}
.workspace-actions button:hover {
  background-color: #c0392b;
}
.workspace-actions button.rename {
  background-color: #2ecc71;
}
.workspace-actions button.rename:hover {
  background-color: #27ae60;
}
.file-actions {
  display: flex;
  gap: 5px;
}
.file-actions button {
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
}
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
  max-width: 500px;
  width: 100%;
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

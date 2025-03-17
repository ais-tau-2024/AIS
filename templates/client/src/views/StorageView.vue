<template>
    <div class="storage-view">
        <LeftPanelComponent class="left-panel" />
        <div class="storage-section p-3">
            Storage
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
    name: "StorageView",
    components: {LeftPanelComponent},
    data() {
        return {
            hi: "123"
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
</style>

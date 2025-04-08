<template>
    <div class="left-panel p-3 bg-dark">
        <div>
            <!-- <div 
                class="panel-elem pb-4"
            >
                <img 
                    :title="localization[langStore.lang].components.leftPanel.homePage"
                    src="../assets/icons/white/home.png" alt="" @click="goPageHome">
            </div> -->
            <div class="panel-elem pb-4">
                <img
                    :title="localization[langStore.lang].components.leftPanel.profilePage"
                    src="../assets/icons/white/account.png"
                    alt=""
                    @click="goPageProfile"
                />
            </div>
            <div class="panel-elem pb-4">
                <img
                    :title="localization[langStore.lang].components.leftPanel.usersPage"
                    src="../assets/icons/white/group.png"
                    alt=""
                    @click="goPageUsers"
                />
            </div>
            <div class="panel-elem pb-4">
                <img
                    :title="localization[langStore.lang].components.leftPanel.storagePage"
                    src="../assets/icons/white/file-management.png"
                    alt=""
                    @click="goPageStorage"
                />
            </div>
        </div>
        <div>
            <div class="panel-elem">
                <img
                    :title="localization[langStore.lang].components.leftPanel.changeLanguage"
                    src="../assets/icons/white/language.png"
                    alt=""
                    @click="changeLanguage"
                    class="mb-3"
                />
                <img
                    :title="localization[langStore.lang].components.leftPanel.logout"
                    src="../assets/icons/white/logout.png"
                    alt=""
                    @click="logout"
                />
            </div>
        </div>
    </div>
</template>

<script>
import router from '../router/router'
import { localization } from '../assets/js/localization'
import { useLangStore } from '../stores/lang'
import { useAuthStore } from '../stores/authStore'

export default {
    name: 'LeftPanelComponent',
    data() {
        return {
            langStore: null,
            authStore: null,
            localization: localization,
        }
    },
    created() {
        this.langStore = useLangStore()
        this.authStore = useAuthStore()
    },
    methods: {
        goPageHome() {
            router.push('/')
        },
        goPageProfile() {
            router.push('/profile')
        },
        goPageUsers() {
            router.push('/users')
        },
        goPageStorage() {
            router.push('/storage')
        },
        changeLanguage() {
            this.langStore.changeLang()
        },
        logout() {
            this.authStore.deactivateAuth()
        },
    },
}
</script>

<style scoped>
.left-panel {
    width: var(--left-panel-width);
    height: 100%;
    flex-shrink: 0;
    position: relative;

    display: flex;
    justify-content: space-between;
    flex-direction: column;
}

.panel-elem {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-direction: column;
}
img {
    width: 25px;
    cursor: pointer;
}
</style>

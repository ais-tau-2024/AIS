<template>
    <div class="notification-container">
        <transition-group name="fade" tag="div">
            <div
                class="alert"
                v-for="notif in notifications"
                :key="notif.id"
                :class="`alert-${notif.statusColor}`"
                @click="removeNotification(notif.id)"
            >
                {{ notif.message }}
            </div>
        </transition-group>
    </div>
</template>

<script>
export default {
    name: 'Notifications',
    data() {
        return {
            notifications: [],
        }
    },
    methods: {
        addNotification({ message, status = 200, duration = 3000 } = {}) {
            console.log(message, status, duration)
            let statusColor = ''
            if (status == 500) {
                statusColor = 'danger'
            }

            if (status == 400) {
                statusColor = 'warning'
            }

            if (status == 200) {
                statusColor = 'success'
            }

            if (status == 100) {
                statusColor = 'info'
            }

            const id = Date.now() + Math.random()
            this.notifications.push({ id, message, statusColor })
            setTimeout(() => {
                this.removeNotification(id)
            }, duration)
        },
        removeNotification(id) {
            this.notifications = this.notifications.filter((n) => n.id !== id)
        },
    },
}
</script>

<style scoped>
.notification-container {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 9999; /* Больше чем у модалок */
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin: 20px;
}

.notification {
    color: #fff;
    padding: 12px 20px;
    margin-bottom: 10px;
    /* border-radius: 4px;
	box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); */
    cursor: pointer;
}

/* .notification-success {
	background: #2ecc71;
}

.notification-error {
	background: #e74c3c;
}

.notification-warning {
	background: #f39c12;
} */

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>

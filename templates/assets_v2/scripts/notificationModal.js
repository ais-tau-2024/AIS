// templates/assets/scripts/notificationModal.js

const notificationModalMethods = {
    newNotification(message = '', status = 'success') {
        this.notifications.visible = true
        this.notifications.messages.push({
            message: message,
            status: status
        })

        // Убираем уведомление через 2.5 секунды
        setTimeout(() => {
            // Удаляем последнее уведомление
            this.notifications.messages.pop()
            
            if (this.notifications.messages.length === 0) {
                this.notifications.visible = false
            }
        }, 2500);
    }
}
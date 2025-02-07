
const authPageMethods = {
    authPageLogin() {
        const iin = this.authData.authForm.iin
        const password = this.authData.authForm.password

        if (iin === '') {
            this.newNotification('Пожалуйста, заполните все поля', 'error')
            return;
        }
        if (iin.length !== 12) {
            this.newNotification('ИИН должен состоять из 12 цифр', 'error')
            return;
        }
        

        if (!this.authData.authForm.passwordConfirmationVisible) {
            axios.get('/auth/teacher/password?iin=' + iin, {
                headers: this.getHeaders()
            }).then((response)=>{
                this.newNotification('Пользователь подтвержден. Введите новый пароль', 'success')
                
                this.authData.authForm.passwordConfirmationVisible = true
            }).catch((error)=>{
                console.error('Ошибка подтверждения:', error);
                if (error.response && error.response.status === 203) {
                    axios.post('/auth/teacher/login', {
                        iin: iin,
                        password: password
                    }, {
                        headers: this.getHeaders()
                    }).then((response) => {
                        this.auth.token = response.data.token;
                        this.page = 'profile';
                        this.newNotification('Вы успешно авторизовались', 'success');
                    }).catch((err) => {
                        console.error('Ошибка входа:', err);
                        this.newNotification('Не удалось авторизоваться', 'error');
                    });
                } else {
                    this.newNotification('Пользователь не найден', 'error');
                }
            })
        } else {

            if (password !== this.authData.authForm.passwordConfirmation) {
                this.newNotification('Пароли не совпадают', 'error')
                return;
            }

            if (password === '') {
                this.newNotification('Пожалуйста, заполните все поля', 'error')
                return;
            }

            axios.post('/auth/teacher/password', {
                iin: iin,
                password: password
            }, {
                headers: this.getHeaders()
            }).then((response)=>{
                this.auth.token = response.data.token
                this.page = 'profile'
                this.newNotification('Вы успешно авторизовались', 'success')
            }).catch((error)=>{
                console.log(error)
                this.newNotification('Не удалось авторизоваться', 'error')
            })
        }

        
    }
}
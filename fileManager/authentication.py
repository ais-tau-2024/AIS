from rest_framework import authentication, exceptions
from custom_auth.models import TeacherAuthTokenModel

class TeacherTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('token')
        if not token:
            return None
        try:
            auth_token = TeacherAuthTokenModel.objects.get(token=token)
        except TeacherAuthTokenModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('Неверный токен')
        return (auth_token.teacher, auth_token)

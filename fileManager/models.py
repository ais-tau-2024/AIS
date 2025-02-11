from django.db import models

# Create your models here.

import os
from django.db import models
from django.conf import settings
from custom_auth.models import TeacherModel

class Desktop(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='desktops')
    name = models.CharField(max_length=255, default='Новый рабочий стол')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_path(self):
        # Путь: media/desktops/{desktop.id}
        return os.path.join(settings.MEDIA_ROOT, 'desktops', str(self.id))


class DesktopAccess(models.Model):
    desktop = models.ForeignKey(Desktop, on_delete=models.CASCADE, related_name='access_list')
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='shared_desktops')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('desktop', 'teacher')

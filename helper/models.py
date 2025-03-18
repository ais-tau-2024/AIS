from django.db import models

# Create your models here.

from django.db import models

class AutoCompleteRecord(models.Model):
    label = models.CharField(max_length=255)
    value = models.IntegerField(unique=True)

    def __str__(self):
        return self.label

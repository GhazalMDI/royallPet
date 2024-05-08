from django.db import models
from django_jalali.db import models as jmodels

class BaseModel(models.Model):
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

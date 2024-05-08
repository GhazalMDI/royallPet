from django.db import models

from utils.baseModel import BaseModel

class Banner(BaseModel):
    image = models.ImageField(upload_to='home/%Y/%m/%d')

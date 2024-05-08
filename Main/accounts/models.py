from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.manager import UserManager
from utils.baseModel import BaseModel
from django_jalali.db import models as jmodels


class User(AbstractBaseUser):
    phone_number = models.CharField(unique=True, max_length=11, verbose_name='تلفن همراه')
    first_name = models.CharField(verbose_name='نام', max_length=20, null=True, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, max_length=255)
    birthday = models.CharField(verbose_name='تاریخ تولد', null=True, blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']
    object = UserManager()

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return 'کاربر'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def __str__(self):
        return f'{self.phone_number}'

    def is_staff(self):
        return self.is_admin

    @property
    def firstwordname(self):
        user_unknown = 'کاربر عزیز'
        if self.first_name and self.full_name:
            return self.first_name[0]
        if self.last_name:
            return self.last_name[0]
        return user_unknown[0]


class Otp(models.Model):
    Random_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=11)
    created = jmodels.jDateTimeField(auto_now_add=True)


class OtpChecked(models.Model):
    Otp_code = models.CharField(max_length=6)
    created = jmodels.jDateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=11, null=True)
    block = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'{self.Otp_code} - {self.phone_number}'


class Address(BaseModel):
    user = models.ForeignKey('User',models.SET_NULL,null=True)
    formatted_address = models.TextField("نشانی پستی")
    county = models.CharField(max_length=255, null=True,verbose_name="شهرستان")
    state = models.CharField(max_length=255,verbose_name="استان")
    village = models.CharField(max_length=255, null=True, blank=True,verbose_name="روستا")
    House_number = models.CharField(max_length=255, null=True,verbose_name="پلاک")
    floor = models.CharField(max_length=255,null=True,verbose_name="طبقه")
    unit = models.CharField(max_length=255, null=True, blank=True,verbose_name="واحد")
    postal_code = models.CharField(max_length=10,null=True,verbose_name="کد پستی")

    def __str__(self):
        return f'{self.formatted_address}'

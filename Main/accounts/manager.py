
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self,phone_number,password,email=None,last_name=None,first_name=None,postal_code=None):
        if not phone_number:
            raise ValidationError('لطفا شماره تلفن صحیح وارد نمایید')
        user = self.model(
            phone_number = phone_number,
            email= email,
            last_name = last_name,
            first_name = first_name,
            postal_code = postal_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone_number,password,email=None,last_name=None,first_name=None,postal_code=None):
        user = self.create_user(phone_number,password,email,last_name,first_name,postal_code)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Username field is required")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirm = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("created_at",)


class Code(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=6, blank=True)

    def save(self, *args, **kwargs):
        # self.number = make_password(self.number)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)

    def refresh_code(self):
        number_list = [i for i in range(10)]
        code_items = []

        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)
        
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string

class ForgotCode(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=6, blank=True, null=True)
    new_password = models.CharField(max_length=128)
    expiry = models.DateTimeField(default=timezone.now() + timedelta(hours=1))

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        self.refresh_code()
        # self.new_password = make_password(self.new_password)
        super().save(*args, **kwargs)

    def refresh_code(self):
        number_list = [i for i in range(10)]
        code_items = []

        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)
        
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string

    def setConfirmationDate(self):
        self.confirmationDate = timezone.now()

    def is_valid(self):
        if self.expiry > timezone.now() :
            return True
        else :
            return False

    def is_expired(self):
        return True if self.expiry < timezone.now() else False


    def is_validForChange(self):
        if self.is_used and self.confirmationDate  + timedelta(hours=1) > timezone.now() :
            return True
        else :
            return False
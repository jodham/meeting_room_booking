from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # first_name = models.CharField(verbose_name='first name', max_length=50)
    # last_name = models.CharField(verbose_name='last name', max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True)
    room_name = models.CharField(max_length=150)
    room_location = models.CharField(max_length=150)
    room_capacity = models.IntegerField()

    def __str__(self):
       return self.room_name


class Bookings(models.Model):
    title = models.CharField(max_length=100)
    booked_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    date_updated = models.DateTimeField(auto_now=True)
    duration = models.TimeField()


class Resource(models.Model):
    rm_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResourceUtilization(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class UserActivity(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()


# class RoomUsage(models.Model):
#     rm_id = models.ForeignKey(Room, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
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


class Roles(models.Model):
    role_name = models.CharField(max_length=100)
    data_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


class Refreshments(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=50)
    last_name = models.CharField(verbose_name='last name', max_length=50)
    active = models.BooleanField(default=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=255, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
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

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Campus(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Facility_Category(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Facility(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Facility_Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Rooms(models.Model):
    location = models.ForeignKey(Campus, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    capacity = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    facilities_ids = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def set_facilities_ids(self, facilities_ids):
        self.facilities_ids = ','.join(map(str, facilities_ids))

    def get_facilities_ids(self):
        return list(map(int, self.facilities_ids.strip("[]").split(',')))

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'pk': self.pk})


"""
    def unsuspend_if_needed(self):
        if self.is_suspended and self.suspension_end and self.suspension_end <= timezone.localtime():
            self.is_suspended = False
            self.suspension_reason = None
            self.suspension_start = None
            self.suspension_end = None
            self.save()
"""


class Booking(models.Model):
    STATUS_PENDING = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2
    STATUS_CANCELLED = 3

    STATUS_CHOICES = [
        (STATUS_PENDING, 'pending'),
        (STATUS_APPROVED, 'approved'),
        (STATUS_REJECTED, 'rejected'),
        (STATUS_CANCELLED, 'cancelled'),
    ]
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings_created")
    title = models.CharField(max_length=100)
    refreshments = models.CharField(max_length=100, null=True)
    extra_peripherals = models.CharField(max_length=100, null=True)
    reject_reason = models.TextField(null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    actioned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bookings_actioned')
    date_actioned = models.DateTimeField(null=True)
    cancelled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('bookings_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Room_Suspension(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    suspension_reason = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"self.room"


class Booking_Approval(models.Model):
    need_approval = models.BooleanField(default=False)


class System_Logs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    key_word = models.CharField(max_length=30)
    date_actioned = models.DateTimeField(auto_now_add=True)

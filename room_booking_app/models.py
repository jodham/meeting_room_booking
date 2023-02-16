from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class UserManager(BaseUserManager):
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


class Roles(models.Model):
    role_name = models.CharField(max_length=30)
    data_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=50)
    last_name = models.CharField(verbose_name='last name', max_length=50)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=255, default=2)
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


"""
    # def get_role_name(self):
    #     role_ids = [int(rid) for rid in self.role.split(',')]
    #     roles = Roles.objects.filter(id__in=role_ids)
    #     role_names = [role.role_name for role in roles]
    # 
    #     if role_names == ['default']:
    #         return 'default'
    #     elif role_names == ['default', 'approver']:
    #         return 'approver'
    #     elif role_names == ['default', 'approver', 'admin']:
    #         return 'admin'
    #     else:
    #         return 'default'

"""


class Campus(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Facility(models.Model):
    title = models.CharField(max_length=30)
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
    facilities_ids = models.CharField(max_length=255, default='', blank=True)
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

    STATUS_CHOICES = [
        (STATUS_PENDING, 'pending'),
        (STATUS_APPROVED, 'approved'),
        (STATUS_REJECTED, 'rejected'),
    ]
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings_created")
    title = models.CharField(max_length=100)
    reject_reason = models.TextField(null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    actioned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bookings_actioned')
    date_actioned = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('bookings_detail', kwargs={'pk': self.pk})


class Room_Suspension(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    suspension_reason = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"Suspension for {{self.room}}"

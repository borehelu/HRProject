from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class Departments(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Employees(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, unique=True)
    address = models.TextField()
    role = models.TextField()
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    username = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, unique=True)
    relationship = models.CharField(max_length=20)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.relationship} to {self.employee.first_name}"


class Skills(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class EmployeeSkills(models.Model):
    PROFICIENCY_CHOICES = (
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Advanced')
    )
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES)

    class Meta:
        unique_together = ('employee', 'skill')

    def __str__(self):
        return f"{self.employee.first_name} {self.skill.name}"


class LeaveTypes(models.Model):
    LEAVE_TYPES = (
        ('Vacation', 'Vacation'),
        ('Sick', 'Sick'),
        ('Maternity', 'Maternity'),
        ('Paternity', 'Paternity'),
        ('Unpaid', 'Unpaid'),
        ('Other', 'Other')
    )
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    accrual_rate = models.IntegerField()
    max_balance = models.IntegerField()
    carryover_limit = models.IntegerField()

    def __str__(self):
        return f"{self.leave_type} at {self.accrual_rate} day/month"


class LeaveBalances(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE)
    accrued_balance = models.IntegerField()
    used_balance = models.IntegerField()
    remaining_balance = models.IntegerField()

    def __str__(self):
        return f"{self.employee.first_name} leave balance {self.remaining_balance}"


class LeaveRequests(models.Model):
    LEAVE_STATUS = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'))
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    comments = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.start_date} to {self.end_date} is {self.status}"

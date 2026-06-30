from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)

    max_customers = models.PositiveIntegerField(default=50)
    max_employees = models.PositiveIntegerField(default=10)
    max_invoices = models.PositiveIntegerField(default=100)

    features = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Business(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Expired', 'Expired'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_businesses'
    )

    business_name = models.CharField(max_length=150)
    business_type = models.CharField(max_length=100, blank=True, null=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)

    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('Trial', 'Trial'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    business = models.OneToOneField(
        Business,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Trial')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = timezone.now().date() + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_active(self):
        today = timezone.now().date()
        return self.status in ['Trial', 'Active'] and self.end_date and self.end_date >= today

    def __str__(self):
        plan_name = self.plan.name if self.plan else 'No Plan'
        return f"{self.business.business_name} - {plan_name}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('SuperAdmin', 'Super Admin'),
        ('BusinessAdmin', 'Business Admin'),
        ('Employee', 'Employee'),
        ('Customer', 'Customer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='user_profiles',
        null=True,
        blank=True
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='BusinessAdmin')
    phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
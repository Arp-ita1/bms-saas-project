from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Closed', 'Closed'),
    ]

    INQUIRY_CHOICES = [
        ('BMS Demo Request', 'BMS Demo Request'),
        ('Pricing Inquiry', 'Pricing / Plan Inquiry'),
        ('Subscription Inquiry', 'Subscription Inquiry'),
        ('Business Setup Help', 'Business Setup Help'),
        ('Enterprise Plan Inquiry', 'Enterprise Plan Inquiry'),
        ('Technical Support', 'Technical Support'),
        ('Feature Request', 'Feature Request'),
        ('Other', 'Other'),
    ]

    PLAN_CHOICES = [
        ('Basic Plan', 'Basic Plan'),
        ('Professional Plan', 'Professional Plan'),
        ('Business Plan', 'Business Plan'),
        ('Enterprise Plan', 'Enterprise Plan'),
        ('Not Sure', 'Not Sure'),
    ]

    name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    inquiry_type = models.CharField(max_length=80, choices=INQUIRY_CHOICES)
    preferred_plan = models.CharField(max_length=80, choices=PLAN_CHOICES, blank=True, null=True)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    admin_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"
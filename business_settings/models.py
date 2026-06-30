from django.db import models


class BusinessProfile(models.Model):
    business = models.OneToOneField(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='business_profile',
        null=True,
        blank=True
    )

    company_name = models.CharField(max_length=160, default='Business Management System')
    owner_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)
    logo = models.ImageField(upload_to='business_logo/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    @classmethod
    def get_profile(cls, business=None):
        if business:
            profile, created = cls.objects.get_or_create(
                business=business,
                defaults={
                    'company_name': business.business_name,
                    'owner_name': business.owner.first_name or business.owner.username,
                    'email': business.email,
                    'phone': business.phone,
                    'address': business.address,
                    'city': business.city,
                    'state': business.state,
                }
            )
            return profile

        profile, created = cls.objects.get_or_create(id=1)
        return profile
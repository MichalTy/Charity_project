from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    FOUNDATION = 'fundacja'
    NGO = 'organizacja pozarządowa'
    COLLECTION_LOCAL = 'zbiórka lokalna'

    TYPE_CHOICES = [
        (FOUNDATION, 'Fundacja'),
        (NGO, 'Organizacja Pozarządowa'),
        (COLLECTION_LOCAL, 'Zbiórka Lokalna'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Donation by {self.user.username if self.user else 'anonymous'}"

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class HazardCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class HazardReport(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(HazardCategory, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pin_code = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='hazard_photos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.category}"
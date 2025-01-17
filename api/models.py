from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Hospital(models.Model):
    name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    api_endpoint=models.URLField()

class PatientRecord(models.Model):
    patient_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    diagnosis = models.TextField()
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    created_at = models.DateTimeField(auto_now_add=True)


    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('researcher', 'Researcher'),
        ('official', 'Government Official'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

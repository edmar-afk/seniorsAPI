from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.

class Pwd(models.Model):
    people = models.TextField()
    age = models.IntegerField()
    gender = models.TextField()
    location = models.TextField()
    

class Infrastructure(models.Model):
    name = models.TextField()
    type = models.TextField()
    description = models.TextField()
    image = models.FileField(
        upload_to='infrastructure/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True
    )
    location = models.TextField()
    
class SeniorCitizen(models.Model):
    people = models.TextField()
    age = models.IntegerField()
    gender = models.TextField()
    location = models.TextField()
    

class Households(models.Model):
    family_name = models.CharField(max_length=100)
    location = models.TextField()
    def __str__(self):
        return self.family_name

class HouseholdMember(models.Model):
    ROLE_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
    ]

    household = models.ForeignKey(Households, related_name='members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.TextField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
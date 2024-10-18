from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_num = models.TextField()
    address = models.TextField()
    dob = models.DateField(blank=True, null=True)
    profile_pic = models.FileField(
        upload_to='profiles/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True
    )
    def __str__(self):
        return self.user.first_name

class Pension(models.Model):
    seniors = models.ForeignKey(User, on_delete=models.CASCADE)
    requirement = models.FileField(upload_to='pensions/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    requirement1 = models.FileField(upload_to='ids/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    requirement2 = models.FileField(upload_to='authorization-letters/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default='Not Eligible')
    qr = models.FileField(upload_to='qrs/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], blank=True)
    notification_status = models.TextField()
    
class Schedule(models.Model):
    description = models.TextField()
    month = models.DateField()
    startDatetime = models.TimeField()
    endDatetime = models.TimeField()

class SubmissionStatus(models.Model):
    is_on = models.BooleanField()

class Notification(models.Model):
    seniors = models.ForeignKey(User, on_delete=models.CASCADE)

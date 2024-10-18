from django.contrib import admin
from .models import Profile, Schedule, Pension, SubmissionStatus
# Register your models here.


admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(Pension)
admin.site.register(SubmissionStatus)
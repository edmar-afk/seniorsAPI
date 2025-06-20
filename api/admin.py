from django.contrib import admin
from .models import Pwd, Infrastructure, SeniorCitizen, HouseholdMember, Households, Feedback

admin.site.register(Pwd)
admin.site.register(Infrastructure)
admin.site.register(SeniorCitizen)
admin.site.register(HouseholdMember)
admin.site.register(Households)
admin.site.register(Feedback)
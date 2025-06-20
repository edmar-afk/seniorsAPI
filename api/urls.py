from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('pwds/', views.PwdView.as_view(), name='pwd-list-create'),
     path('infras/create/', views.InfrastructureCreateView.as_view(), name='infrastructure-create'),
    path('infras/', views.InfrastructureListView.as_view(), name='infrastructure-list'),
    path('seniors/', views.SeniorCitizenListCreateView.as_view(), name='seniors-list-create'),
    path('households/', views.HouseholdListCreateView.as_view(), name='household-list-create'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('feedback/submit/', views.FeedbackCreateView.as_view(), name='submit-feedback'),
    path('feedbacks/', views.FeedbackListView.as_view(), name='list-feedback'),
]

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_picture'),
    path('schedules/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule-list/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('seniors/', views.SeniorsListView.as_view(), name='senior-list'),
    path('pensions/create/<int:senior_id>/', views.PensionCreateView.as_view(), name='create_pension'),
    path('pensions/user/<int:user_id>/', views.PensionListView.as_view(), name='pension-list'),
    path('delete-pension/<int:pension_id>/', views.DeletePensionView.as_view(), name='delete-pension'),
    path('pensions-list/', views.AllPensionListView.as_view(), name='pensions-list'),
    
    path('add-qr-to-pension/<int:pension_id>/', views.AddQrCodeToPension.as_view(), name='add_qr_to_pension'),
    path('send-notification/<int:senior_id>/', views.SendNotificationAPIView.as_view(), name='send-notification'),
    
    
    
    path('submission-status/', views.ToggleSubmissionStatusView.as_view(), name='toggle_submission_status'),
    
    path('pension/submission-count/', views.SubmissionCountView.as_view(), name='submission-count'),
    path('pension/non-submission-count/', views.NonSubmissionCountView.as_view(), name='non-submission-count'),
    
     path('users/registered-count/', views.RegisteredUserCountView.as_view(), name='registered-users-count'),
     path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
     
     path('update-profile-pic/', views.UpdateProfilePicView.as_view(), name='update-profile-pic'),
]

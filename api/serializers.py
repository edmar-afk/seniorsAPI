from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Pension, Schedule, Notification, SubmissionStatus
from django.utils.timezone import now
from django.utils import timezone

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name' , 'password', 'is_superuser', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Use the nested serializer for user details

    class Meta:
        model = Profile
        fields = ['id', 'user', 'mobile_num', 'dob', 'address', 'profile_pic']
        
class UpdateProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic']
        
class UserSerializer(serializers.ModelSerializer):
    mobile_num = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'mobile_num', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        mobile_num = validated_data.pop('mobile_num')
        dob = self.context['request'].data.get('dob')  # Get dob from the request data
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, mobile_num=mobile_num, dob=dob)  # Pass dob to Profile
        return user


class PensionSerializer(serializers.ModelSerializer):
    seniors = UserDetailSerializer()  # Use the nested serializer for user details
    class Meta:
        model = Pension
        fields = '__all__'
        
class SubmitRequirementsSerializer(serializers.ModelSerializer):
    seniors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Accepts the User ID
    class Meta:
        model = Pension
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'description', 'month', 'startDatetime', 'endDatetime']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class PensionQrCodeSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Use the nested serializer for user details
    class Meta:
        model = Pension
        fields = ['id', 'seniors', 'qr', 'status', 'notification_status']
        
class SubmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = ['id', 'is_on']
        

class SubmissionCountSerializer(serializers.Serializer):
    submission_count = serializers.IntegerField()

    @staticmethod
    def get_submission_count():
        today = now().date()
        return Pension.objects.filter(date_submitted__date=today).count()
    
class NonSubmissionCountSerializer(serializers.Serializer):
    non_submission_count = serializers.IntegerField()

    def to_representation(self, instance):
        # Get current date
        today = timezone.now().date()

        # Get all registered users (seniors)
        total_users = User.objects.filter(is_active=True, is_superuser=False).count()

        # Count the number of users who have submitted a pension today
        submitted_today_count = Pension.objects.filter(date_submitted__date=today).values('seniors').distinct().count()

        # Count the users who did NOT submit by subtracting the two
        non_submission_count = total_users - submitted_today_count

        return {'non_submission_count': non_submission_count}
    
class RegisteredUserCountSerializer(serializers.Serializer):
    registered_users_count = serializers.IntegerField()

    def to_representation(self, instance):
        # Count all registered users where is_superuser is False
        registered_users_count = User.objects.filter(is_active=True, is_superuser=False).count()

        return {'registered_users_count': registered_users_count}
# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, RegisteredUserCountSerializer, UpdateProfilePicSerializer, NonSubmissionCountSerializer, SubmissionCountSerializer,  ScheduleSerializer, PensionSerializer, SubmissionStatusSerializer, PensionQrCodeSerializer, SubmitRequirementsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Profile, Schedule, Pension, SubmissionStatus
from rest_framework.views import APIView
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from .utils import generate_qr_code  # Import the function here
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
import requests
import time
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone

from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import requests
import time
from datetime import datetime
from django.utils.dateformat import DateFormat

User = get_user_model()



class UpdateProfilePicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProfilePicSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile picture updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API view to retrieve the profile of a user based on user ID.
    """
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Get the profile associated with the given user ID
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendNotificationAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, senior_id):
        # Get the senior based on the ID provided in the URL
        senior = get_object_or_404(User, id=senior_id)

        # Retrieve the schedule for the current month (or modify the query as needed)
        schedule = Schedule.objects.filter(month__month=datetime.now().month).first()

        # Format the month if a schedule exists in "6 Nov 2024" format
        month_formatted = DateFormat(schedule.month).format('j M Y') if schedule else "a specific date"

        # Default message to be sent
        default_message = (
            f"Maayong adlaw Mr/Mrs. {senior.first_name} nga nagpuyo sa {senior.last_name}. "
            f"Ang DSWD nakahimo sa pagpagawas sa imong pensyon para sa {month_formatted}. "
            "Palihug tan-awa sila sa opisina ug apila ug dala ang QR Code."
        )
        api_key = 'bbb93c7696179a8d2f0217e72a5d90680b3b6111'  # Replace with your actual API key

        phone_number = senior.username.strip()  # Assuming username holds the phone number

        data = {
            'key': api_key,
            'number': phone_number,
            'message': default_message,
            'type': 'sms',
            'prioritize': 1
        }

        success_count = 0
        fail_count = 0
        fail_reasons = []

        try:
            response = requests.post('https://smsgateway.rbsoft.org/services/send.php', data=data)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('success'):
                success_count += 1
            else:
                fail_count += 1
                fail_reasons.append(response_data)
        except Exception as e:
            fail_count += 1
            fail_reasons.append({'error': str(e)})

        time.sleep(2)  # Introduce a 2-second delay

        return Response(
            {
                'success_count': success_count,
                'fail_count': fail_count,
                'fail_reasons': fail_reasons
            },
            status=status.HTTP_200_OK if success_count > 0 else status.HTTP_400_BAD_REQUEST
        )





class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()  # No need to handle validated data here; it's handled in the serializer

        
        
class SeniorsListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Allows unrestricted access

class SeniorView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user 
    
class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
       
        profile = Profile.objects.get(user__id=user_id)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
        

class ScheduleCreateView(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Request Data:", request.data)  # Print request data to see what is being sent
        response = super().post(request, *args, **kwargs)
        print("Response Data:", response.data)  # Print response data to see the result
        return response
    
class ScheduleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    

class PensionCreateView(generics.CreateAPIView):
    serializer_class = SubmitRequirementsSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, senior_id):
        return Response({'detail': 'Use POST to submit a pension file.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, senior_id):
        try:
            senior = User.objects.get(id=senior_id)
        except User.DoesNotExist:
            return Response({'error': 'Senior not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for the serializer
        data = request.data.copy()
        data['seniors'] = senior.id  # Use the senior's ID directly
        if 'notification_status' not in data:
            data['notification_status'] = 'Notification not Sent'

        # Debug: Print data to check the format
        print("Request Data:", data)

        # Use the serializer with the modified data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PensionListView(generics.ListAPIView):
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Pension.objects.filter(seniors__id=user_id)


class DeletePensionView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pension_id, *args, **kwargs):
        # Fetch the pension object by ID
        pension = get_object_or_404(Pension, id=pension_id)

        # Delete the pension object
        pension.delete()

        return Response({"message": "Pension deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class AllPensionListView(generics.ListAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]
  
  
  
class AddQrCodeToPension(generics.CreateAPIView):
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]

    def post(self, request, pension_id):
        # Get the pension object by ID
        pension = get_object_or_404(Pension, id=pension_id)

        # Get the senior (user) data
        senior = pension.seniors
        first_name = senior.first_name  # Retrieve first_name from User model
        user_id = senior.id  # Retrieve the id from User model
        address = senior.last_name 

        # Retrieve the user's profile to get the address
        profile = get_object_or_404(Profile, user=senior)
       
        # Update the status to 'Eligible'
        pension.status = 'Eligible'
        pension.save()

        # Get the current date and time
        current_time = timezone.now()

        # Format the date and time in the desired format (e.g., 6-9-2024-1-30pm)
        transaction_date = current_time.strftime("%m-%d-%Y")  # e.g., 06-09-2024
        transaction_time = current_time.strftime("%I-%M%p").lower()  # e.g., 01-30pm

        # Generate the unique transaction ID (e.g., 1-6-9-2024-1-30pm)
        transaction_id = f"{user_id}-{transaction_date}-{transaction_time}"

        # Generate QR code content with user's first name, status, address, and transaction ID
        qr_content = (
            f"{user_id}\n"
            f"{first_name}\n"
            f"{address}\n"
            f"{pension.status}\n"
            f"{transaction_id}"
        )

        try:
            # Generate QR code
            qr_image = qrcode.make(qr_content)
            qr_io = BytesIO()
            qr_image.save(qr_io, format="PNG")

            # Save QR code to the pension object
            qr_file = ContentFile(qr_io.getvalue(), f"{pension.id}_qr.png")
            pension.qr.save(f"{pension.id}_qr.png", qr_file)
            pension.save()

            # Prepare the response
            response_data = {
                "pension_id": pension.id,
                "qr_code_url": pension.qr.url,  # Assuming 'qr' is a FileField or ImageField
                "transaction_id": transaction_id  # Include the transaction ID in the response
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors during QR code generation or saving
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    

class ToggleSubmissionStatusView(APIView):
    def get_object(self):
        # Assuming there's only one SubmissionStatus object in your system
        return SubmissionStatus.objects.first()

    def get(self, request, *args, **kwargs):
        submission_status = self.get_object()
        serializer = SubmissionStatusSerializer(submission_status)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        submission_status = self.get_object()
        submission_status.is_on = not submission_status.is_on  # Toggle the status
        submission_status.save()
        serializer = SubmissionStatusSerializer(submission_status)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SubmissionCountView(APIView):
    def get(self, request, *args, **kwargs):
        submission_count = SubmissionCountSerializer.get_submission_count()
        data = {'submission_count': submission_count}
        return Response(data)
    


class NonSubmissionCountView(APIView):
    def get(self, request):
        serializer = NonSubmissionCountSerializer({})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisteredUserCountView(APIView):
    def get(self, request):
        serializer = RegisteredUserCountSerializer({})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
SeniorsListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Pwd, Infrastructure, SeniorCitizen, Households, Feedback
from .serializers import PwdSerializer, InfrastructureSerializer, FeedbackSerializer, SeniorCitizenSerializer, HouseholdsSerializer, StatsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class PwdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        pwds = Pwd.objects.all()
        serializer = PwdSerializer(pwds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PwdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfrastructureCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer

class InfrastructureListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer
    

class SeniorCitizenListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = SeniorCitizen.objects.all()
    serializer_class = SeniorCitizenSerializer
    
class HouseholdListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Households.objects.all()
    serializer_class = HouseholdsSerializer


class StatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = {
            "total_pwds": Pwd.objects.count(),
            "total_seniors": SeniorCitizen.objects.count(),
            "total_households": Households.objects.count()
        }
        serializer = StatsSerializer(data)
        return Response(serializer.data)
    

class FeedbackCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Feedback.objects.all().order_by('-id')
    serializer_class = FeedbackSerializer
    
    
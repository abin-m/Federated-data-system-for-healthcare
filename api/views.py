from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Hospital,PatientRecord
from .serializers import HospitalSerializer,PatientRecordSerializer
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import UserSignupSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import requests

class HospitalViewSet(ModelViewSet):
    queryset=Hospital.objects.all()
    serializer_class=HospitalSerializer

    @action(detail=True, methods=['get'])
    def fetch_records(self,request,pk=None):
        hospital=self.get_object()
        response=requests.get(hospital.api_endpoint)
        if response.status_code == 200:
            return Response(response.json())
        return Response({'error':'failed to Fetch records'},status=response.status_code)
    
class PatientRecordViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=PatientRecord.objects.all()
    serializer_class=PatientRecordSerializer

# Action to fetch aggredgated records from multple hospitals
    
@api_view(['GET'])
def aggredgated_data(request):
    hospitals=Hospital.objects.all()
    aggredgated_data=[]
    for hospital in hospitals:
        response=requests.get(hospital.api_endpoint)
        if response.status_code==200:
            aggredgated_data.extend(response.json())
    return Response(aggredgated_data)


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data['tokens'], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# Mocking Hospital end points
class MockHospitalEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        mock_data = {
            "hospital_name": "Example Hospital",
            "location": "City Center",
            "records": [
                {"patient_id": 1, "name": "John Doe", "age": 45, "condition": "Flu"},
                {"patient_id": 2, "name": "Jane Smith", "age": 34, "condition": "Cough"}
            ]
        }
        return Response(mock_data, status=status.HTTP_200_OK)
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
from django.db.models import Q
from django.db.models import Count, Avg
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

class DynamicFilterView(APIView):
    def get(self, request, *args, **kwargs):
        filters = request.query_params  # All query parameters
        queryset = PatientRecord.objects.all()

        # Build the dynamic query
        dynamic_query = Q()
        for field, value in filters.items():
            # Add filtering logic based on field and value
            if "__" in field:  # Handle special operators like __gte, __lte
                dynamic_query &= Q(**{field: value})
            else:  # Default to exact match
                dynamic_query &= Q(**{f"{field}": value})

        # Apply the query to the queryset
        filtered_records = queryset.filter(dynamic_query)

        # Serialize and return results
        from .serializers import AnonymizedPatientRecordSerializer
        serializer = AnonymizedPatientRecordSerializer(filtered_records, many=True)
        return Response(serializer.data)
    
class FilterMetadataView(APIView):
    """
    Returns metadata about the fields available for filtering.
    """
    def get(self, request, *args, **kwargs):
        metadata = {
            "fields": [
                {"name": "age", "type": "integer", "operations": ["=", "__gte", "__lte"]},
                {"name": "diagnosis", "type": "string", "operations": ["=", "__icontains"]},
                {"name": "gender", "type": "string", "operations": ["="]},
                {"name": "created_at", "type": "date", "operations": ["=", "__gte", "__lte"]},
            ]
        }
        return Response(metadata)

class DashboardFilterAnalysisView(APIView):
    """
    Performs aggregations on filtered data for dashboard insights.
    """
    def get(self, request, *args, **kwargs):
        filters = request.query_params
        queryset = PatientRecord.objects.all()

        # Apply filters dynamically
        dynamic_query = Q()
        for field, value in filters.items():
            if "__" in field:
                dynamic_query &= Q(**{field: value})
            else:
                dynamic_query &= Q(**{f"{field}": value})
        filtered_records = queryset.filter(dynamic_query)

        # Perform aggregations
        total_patients = filtered_records.count()
        age_avg = filtered_records.aggregate(average_age=Avg('age'))['average_age']
        gender_distribution = filtered_records.values('gender').annotate(count=Count('gender'))

        return Response({
            "total_patients": total_patients,
            "average_age": age_avg,
            "gender_distribution": list(gender_distribution)
        })

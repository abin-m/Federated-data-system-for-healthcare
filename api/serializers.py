from rest_framework import serializers
from .models import Hospital,PatientRecord
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hospital
        fields='__all__'

class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientRecord
        fields='__all__'

CustomUser = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])  # Correctly access the email from obj
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate the user
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            # If the user exists and password matches, include tokens in the response
            data['tokens'] = self.get_tokens(data)  # Passing 'data' to 'get_tokens'
            return data
        
        raise serializers.ValidationError("Invalid email or password.")
    

class AnonymizedPatientRecordSerializer(serializers.ModelSerializer):
    anonymized_id = serializers.SerializerMethodField()

    class Meta:
        model = PatientRecord
        fields = ['anonymized_id', 'age', 'diagnosis', 'gender', 'created_at']

    def get_anonymized_id(self, obj):
        import hashlib
        return hashlib.sha256(obj.patient_id.encode()).hexdigest()
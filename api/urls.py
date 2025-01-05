from rest_framework.routers import DefaultRouter
from .views import DashboardFilterAnalysisView, DynamicFilterView, FilterMetadataView, HospitalViewSet,PatientRecordViewSet,aggredgated_data,UserSignupView,UserLoginView,CustomTokenRefreshView,MockHospitalEndpoint
from django.urls import path

router= DefaultRouter()
router.register(r'hospitals',HospitalViewSet)
router.register(r'patient-records',PatientRecordViewSet)

urlpatterns= router.urls

urlpatterns+=[
    path('aggregated-data/',aggredgated_data,name='aggredgated_data'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('mock_hospital_data/', MockHospitalEndpoint.as_view(), name='mock_hospital_data'),
    path('dynamic-filter/', DynamicFilterView.as_view(), name='dynamic-filter'),
    path('filter-metadata/', FilterMetadataView.as_view(), name='filter-metadata'),
    path('dashboard-filter-analysis/', DashboardFilterAnalysisView.as_view(), name='dashboard-filter-analysis'),
]
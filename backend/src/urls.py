"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    PatientListCreateView,
    AvailableBedListView,
    AdmissionListView,
    admit_patient,
    discharge_patient
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Patient endpoints
    path('patients', PatientListCreateView.as_view(), name='patient-list-create'),
    
    # Bed endpoints
    path('beds/available', AvailableBedListView.as_view(), name='available-bed-list'),
    
    # Admission endpoints
    path('admissions', AdmissionListView.as_view(), name='admission-list'),
    path('admissions/admit', admit_patient, name='admit-patient'),
    path('admissions/discharge/<int:admission_id>', discharge_patient, name='discharge-patient'),
]

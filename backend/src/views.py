from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Patient, Bed, Admission
from .serializers import (
    PatientSerializer, 
    BedSerializer, 
    AdmissionSerializer,
    AdmitPatientSerializer,
    DischargePatientSerializer
)

class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET /patients?name=<search term>: Search patients by name or return all patients
    POST /patients: Create a new patient
    """
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        """Filter patients by search query if provided."""
        queryset = Patient.objects.all()
        search_query = self.request.query_params.get('name', None)
        
        if search_query:
            # Case-insensitive substring search on patient name
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset.order_by('name')

class AvailableBedListView(generics.ListAPIView):
    """
    GET /beds/available: Return all available beds in the hospital
    """
    serializer_class = BedSerializer
    
    def get_queryset(self):
        """Return beds that don't have active admissions."""
        # Get beds that have no active admissions (discharge_timestamp is null)
        return Bed.objects.exclude(
            admissions__discharge_timestamp__isnull=True
        ).order_by('name')

@api_view(['POST'])
def admit_patient(request):
    """
    POST /admissions/admit: Admit a patient to a bed
    """
    serializer = AdmitPatientSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            admission = serializer.save()
            admission_serializer = AdmissionSerializer(admission)
            return Response(
                {
                    'message': f'Patient {admission.patient.name} successfully admitted to {admission.bed.name}',
                    'admission': admission_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to admit patient: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def discharge_patient(request, admission_id):
    """
    POST /admissions/discharge/<admission_id>: Discharge a patient
    """
    serializer = DischargePatientSerializer(
        data={}, 
        context={'admission_id': admission_id}
    )
    
    if serializer.is_valid():
        try:
            admission = serializer.save()
            admission_serializer = AdmissionSerializer(admission)
            return Response(
                {
                    'message': f'Patient {admission.patient.name} successfully discharged from {admission.bed.name}',
                    'admission': admission_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to discharge patient: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdmissionListView(generics.ListAPIView):
    """
    GET /admissions: Return all admissions
    """
    queryset = Admission.objects.all().order_by('-admitted_timestamp')
    serializer_class = AdmissionSerializer

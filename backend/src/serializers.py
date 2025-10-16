from rest_framework import serializers
from .models import Patient, Bed, Admission


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'dob']


class BedSerializer(serializers.ModelSerializer):
    """Serializer for Bed model."""
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Bed
        fields = ['id', 'name', 'is_available']
        
    def get_is_available(self, obj):
        """Check if bed is available (no active admissions)."""
        return not obj.admissions.filter(discharge_timestamp__isnull=True).exists()


class AdmissionSerializer(serializers.ModelSerializer):
    """Serializer for Admission model."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    bed_name = serializers.CharField(source='bed.name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Admission
        fields = ['id', 'patient', 'bed', 'patient_name', 'bed_name', 
                 'admitted_timestamp', 'discharge_timestamp', 'is_active']
        read_only_fields = ['admitted_timestamp']


class AdmitPatientSerializer(serializers.Serializer):
    """Serializer for admitting a patient to a bed."""
    patient_id = serializers.IntegerField()
    bed_id = serializers.IntegerField()
    
    def validate(self, data):
        """Validate admission data."""
        patient_id = data['patient_id']
        bed_id = data['bed_id']
        
        # Check if patient exists
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError(f"Patient with ID {patient_id} does not exist.")
        
        # Check if bed exists
        try:
            bed = Bed.objects.get(id=bed_id)
        except Bed.DoesNotExist:
            raise serializers.ValidationError(f"Bed with ID {bed_id} does not exist.")
        
        # Check if patient is already admitted (has active admission)
        if patient.admissions.filter(discharge_timestamp__isnull=True).exists():
            raise serializers.ValidationError(f"Patient {patient.name} is already admitted.")
        
        # Check if bed is available (no active admissions)
        if bed.admissions.filter(discharge_timestamp__isnull=True).exists():
            raise serializers.ValidationError(f"Bed {bed.name} is not available.")
        
        data['patient'] = patient
        data['bed'] = bed
        return data
    
    def create(self, validated_data):
        """Create a new admission."""
        return Admission.objects.create(
            patient=validated_data['patient'],
            bed=validated_data['bed']
        )


class DischargePatientSerializer(serializers.Serializer):
    """Serializer for discharging a patient."""
    
    def validate(self, data):
        """Validate discharge data."""
        admission_id = self.context['admission_id']
        
        # Check if admission exists
        try:
            admission = Admission.objects.get(id=admission_id)
        except Admission.DoesNotExist:
            raise serializers.ValidationError(f"Admission with ID {admission_id} does not exist.")
        
        # Check if admission is active
        if not admission.is_active:
            raise serializers.ValidationError(f"Admission {admission_id} is already discharged.")
        
        data['admission'] = admission
        return data
    
    def save(self):
        """Discharge the patient."""
        admission = self.validated_data['admission']
        admission.discharge()
        return admission

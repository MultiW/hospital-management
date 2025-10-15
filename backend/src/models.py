from django.db import models
from django.core.exceptions import ValidationError


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    mrn = models.TextField(unique=True)

    class Meta:
        db_table = 'patient'

    def clean(self):
        """Custom validation to ensure name and MRN are not empty or whitespace."""
        super().clean()
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Name cannot be empty or contain only whitespace.'})
        if not self.mrn or not self.mrn.strip():
            raise ValidationError({'mrn': 'MRN cannot be empty or contain only whitespace.'})

    def save(self, *args, **kwargs):
        """Override save to call clean method for validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (MRN: {self.mrn})"


class Bed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'bed'

    def clean(self):
        """Custom validation to ensure bed name is not empty or whitespace."""
        super().clean()
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Bed name cannot be empty or contain only whitespace.'})

    def save(self, *args, **kwargs):
        """Override save to call clean method for validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Admission(models.Model):
    """
    Admission model representing a patient's admission to a bed.
    """
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.RESTRICT,
        related_name='admissions'
    )
    bed = models.ForeignKey(
        Bed,
        on_delete=models.RESTRICT,
        related_name='admissions'
    )
    admitted_timestamp = models.DateTimeField(auto_now_add=True)
    discharge_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'admission'

    def __str__(self):
        status = "Active" if self.discharge_timestamp is None else "Discharged"
        return f"{self.patient.name} in {self.bed.name} ({status})"

    @property
    def is_active(self):
        """Returns True if the patient is still admitted (no discharge timestamp)."""
        return self.discharge_timestamp is None

    def discharge(self, discharge_time=None):
        """
        Discharge the patient by setting the discharge timestamp.
        
        Args:
            discharge_time: Optional datetime for discharge. If None, uses current time.
        """
        from django.utils import timezone
        if discharge_time is None:
            discharge_time = timezone.now()
        self.discharge_timestamp = discharge_time
        self.save()

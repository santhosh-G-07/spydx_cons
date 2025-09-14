from rest_framework import serializers
from .models import ResumeUpload, TrainingRecord
from .models import AttendanceRecord
from .models import OpportunityRecord

class OpportunityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunityRecord
        fields = '__all__'



class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeUpload
        fields = '__all__'

class TrainingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingRecord
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

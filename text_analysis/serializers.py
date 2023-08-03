from rest_framework import serializers
from .models import ServiceManager, TextAnalysisService, DeleteService


class ServiceManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceManager
        fields = ('name', 'url')

class DeleteServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteService
        fields = '__all__'

class TextAnalysisServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnalysisService
        fields = ('service', 'text')

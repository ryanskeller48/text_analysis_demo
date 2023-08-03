from rest_framework import serializers
from .models import EntityRecognition


class EntityRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRecognition
        fields = '__all__'

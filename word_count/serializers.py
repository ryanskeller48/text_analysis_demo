from rest_framework import serializers
from .models import WordCount


class WordCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCount
        fields = '__all__'

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WordCount
from .serializers import WordCountSerializer
from .word_count import WordCounter


@api_view(['GET', 'POST'])
def word_count(request):
    
    if request.method == 'GET':  # List saved text/responses
        wordcounts = WordCount.objects.all()
        wc_serializer = WordCountSerializer(wordcounts, many=True)
        return Response(wc_serializer.data)

    elif request.method == 'POST':  # Return word count of input_text
        wc_serializer = WordCountSerializer(data=request.data)
        if wc_serializer.is_valid():
            wc = WordCounter(wc_serializer.validated_data["input_text"]).count()
            wc_serializer.validated_data["result"] = wc
            wc_serializer.save()  # Save computed result
            return Response({"result": f"{wc}"}, status=status.HTTP_200_OK)  # Return result
        else:
            return Response(wc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer
from .sentiment_analysis import SentimentAnalyzer

@api_view(['GET', 'POST'])
def sentiment_analysis(request):
    
    if request.method == 'GET':  # List saved text/responses
        sentiments = SentimentAnalysis.objects.all()
        sent_serializer = SentimentAnalysisSerializer(sentiments, many=True)
        return Response(sent_serializer.data)

    elif request.method == 'POST':  # Return computed sentiment from input_text
        sent_serializer = SentimentAnalysisSerializer(data=request.data)
        if sent_serializer.is_valid():
            sent = SentimentAnalyzer(sent_serializer.validated_data["input_text"]).analyze()
            sent_serializer.validated_data["result"] = sent
            sent_serializer.save()  # Save computed result
            return Response({"result": f"{sent}"}, status=status.HTTP_200_OK)  # Return result
        else:
            return Response(sent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
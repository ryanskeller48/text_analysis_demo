from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import EntityRecognition
from .serializers import EntityRecognitionSerializer
from .entity_recognition import EntityRecognizer


@api_view(['GET', 'POST'])
def entity_recognition(request):

    if request.method == 'GET':  # List saved text/responses
        entities = EntityRecognition.objects.all()
        ent_serializer = EntityRecognitionSerializer(entities, many=True)
        return Response(ent_serializer.data)

    elif request.method == 'POST':  # Return recognized entities from input_text
        ent_serializer = EntityRecognitionSerializer(data=request.data)
        if ent_serializer.is_valid():
            entities = EntityRecognizer(ent_serializer.validated_data["input_text"]).get_entities()
            ent_serializer.validated_data["result"] = entities
            ent_serializer.save()  # Save computed result
            return Response({"result": entities}, status=status.HTTP_200_OK)  # Return result
        else:
            return Response(ent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

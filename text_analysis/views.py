from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ServiceManager
from .serializers import TextAnalysisServiceSerializer, ServiceManagerSerializer, DeleteServiceSerializer

import requests
import time
import logging

LOG = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def add_service(request):

    if request.method == 'GET': 
        # List services
        services = ServiceManager.objects.all()
        sm_serializer = ServiceManagerSerializer(services, many=True)
        return Response(sm_serializer.data)

    elif request.method == 'POST': 
        sm_serializer = ServiceManagerSerializer(data=request.data)
        if sm_serializer.is_valid():  # Adding a service
            sm_serializer.save()  # Register service to db
            return Response({"message": "Service registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(sm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def delete_service(request):

    if request.method == 'GET': 
        # List services
        services = ServiceManager.objects.all()
        sm_serializer = ServiceManagerSerializer(services, many=True)
        return Response(sm_serializer.data)
    
    elif request.method == 'POST':
        del_serializer = DeleteServiceSerializer(data=request.data)
        if del_serializer.is_valid():
            target_service = del_serializer.validated_data["name"]
            services = ServiceManager.objects.all()
            for service in services:  # Find correct service
                if service.name == target_service:
                    service.delete()  # Delete targeted service
                    return Response({"message": f"Service {target_service} deleted successfully."}, status=status.HTTP_200_OK)
            return Response({"errors": f"Service name '{target_service}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(del_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def text_analysis(request):

    # Create default services if they none exist -- for startup
    curr_services = ServiceManager.objects.all()
    if len(curr_services) == 0:

        def service_exists(target_service, services):
            # Helper to check if service exists
            for service in services:  # Find correct service
                if service.name == target_service:
                    return True
            return False

        desired_services = [
            ["word-count", "http://127.0.0.1:8000/count/"],
            ["entity-recognition", "http://127.0.0.1:8000/recognize/"],
            ["sentiment-analysis", "http://127.0.0.1:8000/analyze/"],
        ]
        for service in desired_services:  # Create services
            if not service_exists(service[0], curr_services):
                ServiceManager.objects.create(name=service[0], url=service[1])

    
    if request.method == 'GET': 
        # List services
        services = ServiceManager.objects.all()
        sm_serializer = ServiceManagerSerializer(services, many=True)
        return Response(sm_serializer.data)

    elif request.method == 'POST': 
        # Analyze text
        ta_serializer = TextAnalysisServiceSerializer(data=request.data)
        if ta_serializer.is_valid():
            LOG.warning("here")
            services = ServiceManager.objects.all()
            target_service = ta_serializer.validated_data["service"]
            target_endpoint = None  # Endpoint to query
            for service in services:  # Find correct service
                if service.name == target_service:
                    target_endpoint = service.url
                    LOG.warning(target_endpoint)
            if target_endpoint is None:  # Catch non-registered service
                LOG.warning("here2")
                return Response({"errors": f"Service name '{target_service}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            data = {'input_text': ta_serializer.validated_data["text"]}  # Data to be sent to service

            retries = 0
            resp = requests.post(target_endpoint, data=data)  # Get response from service
            LOG.warning(resp)
            while resp.status_code != 200:  # Retry if bad response
                LOG.warning(resp.status_code)
                time.sleep(1)
                retries += 1
                resp = requests.post(target_endpoint, data=data)
                if retries > 1:  # Eventually give up
                    return Response({"errors": f"Service '{target_service}' unreachable."}, status=status.HTTP_404_NOT_FOUND)
            data = resp.json()  # 200 response
            return Response(data, status=status.HTTP_200_OK)

        else:  # Non-valid input
            return Response(ta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

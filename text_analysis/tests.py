import pytest

from django.urls import reverse
from mock import patch, MagicMock

from collections import OrderedDict

from .models import TextAnalysisService, ServiceManager, DeleteService
from .serializers import TextAnalysisServiceSerializer, ServiceManagerSerializer, DeleteServiceSerializer


@pytest.mark.django_db
@pytest.mark.parametrize(
    "service, serializer, model",
    (
        ("add_service", ServiceManagerSerializer, ServiceManager),
        ("delete_service", DeleteServiceSerializer, DeleteService),
        ("text_analysis", TextAnalysisServiceSerializer, TextAnalysisService),
    )
)
def test_get(client, service, serializer, model):
    # Test GET view
    url = reverse(service)
    response = client.get(url)

    objects = model.objects.all()
    expected_data = serializer(objects, many=True).data

    assert response.status_code == 200
    if service == "text_analysis":  # We spawn default services here
        assert response.data == [
            OrderedDict([('name', 'word-count'), ('url', 'http://127.0.0.1:8000/count/')]),
            OrderedDict([('name', 'entity-recognition'), ('url', 'http://127.0.0.1:8000/recognize/')]),
            OrderedDict([('name', 'sentiment-analysis'), ('url', 'http://127.0.0.1:8000/analyze/')])
        ]
    else:
        assert response.data == expected_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_text, service",
    (
        ["Lorem ipsum dolor sit amet", "word-count"],
        ["consectetur adipiscing elit", "sentiment-analysis"],
        ["Quis vel eros donec ac odio tempor orci dapibus ultrices.", "entity-recognition"],
    )
)
def test_post_analysis(client, input_text, service):
    # Test we poll the correct service when given a POST at the root

    url = reverse('text_analysis')
    with patch("text_analysis.views.requests.post") as mock_post, \
            patch("text_analysis.views.ServiceManager.objects.all") as mock_endpoints:

        mock_url = "https://example.com/"  # Mock service url
        # Mock response from server
        mock_response = MagicMock(status_code=200)
        mock_response.json = lambda: {'result': 'value'}
        mock_post.return_value = mock_response
        # Create mock service to poll
        mock_endpoints.return_value = {ServiceManager.objects.create(name=service, url=mock_url)}

        # Send POST and assert we call the service with the correct
        client.post(url, data={"service": service, "text": input_text})
        mock_post.assert_called_once_with(mock_url, data={"input_text": input_text})


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input, error, badfield",
    (
        [{"service": "word-count", "text": ""}, "This field may not be blank.", "text"],  # Empty text
        [{"service": "", "text": "asd"}, "This field may not be blank.", "service"],  # Empty service
        [{"service": "word-count"}, "This field is required.", "text"],  # No text
        [{"text": "asd"}, "This field is required.", "service"],  # No service
        [{"service": "asd", "text": "asd"}, "Service name 'asd' does not exist.", "errors"],  # Nonexistent service
    )
)
def test_text_analysis_bad_input(client, input, error, badfield):
    # Test we catch bad input on root with validation
    url = reverse('text_analysis')
    response = client.post(url, data=input)

    assert response.status_code == 400
    if badfield == "errors":
        # catch nonexistent service error
        assert response.data[badfield] == error
    else:
        assert response.data[badfield][0] == error


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_data, delete_data",
    (
        [{"name": "test-service", "url": "https://example.com/"}, {"name": "test-service"}],
    )
)
def test_delete(client, add_data, delete_data):
    # Test we can delete services

    def service_exists(target_service):
        # Helper to check if service exists
        services = ServiceManager.objects.all()
        for service in services:  # Find correct service
            if service.name == target_service:
                return True
        return False

    add_url = reverse('add_service')
    del_url = reverse('delete_service')
    # Add Service, assert it was created
    target_service = add_data["name"]
    response = client.post(add_url, data=add_data)
    assert service_exists(target_service)
    assert response.data["message"] == "Service registered successfully"
    # Delete service
    response = client.post(del_url, data=delete_data)
    assert response.data["message"] == f"Service {target_service} deleted successfully."
    assert not service_exists(target_service)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input, error, badfield",
    (
        [{"name": ""}, "This field may not be blank.", "name"],  # Empty name
        [{"url": "asd"}, "This field is required.", "name"],  # No name
    )
)
def test_delete_bad_input(client, input, error, badfield):
    # Test we catch bad input with validation when deleting services
    url = reverse('delete_service')
    response = client.post(url, data=input)

    assert response.status_code == 400
    assert response.data[badfield][0] == error


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input, error, badfield",
    (
        [{"name": "asd"}, "Service name 'asd' does not exist.", "errors"],  # Bad name
    )
)
def test_delete_nonexistent_service(client, input, error, badfield):
    # Test we catch bad input when trying to delete nonexistent service
    url = reverse('delete_service')
    response = client.post(url, data=input)

    assert response.status_code == 400
    assert response.data[badfield] == error


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input, error, badfield",
    (
        [{"name": "", "url": "https://example.com/"}, "This field may not be blank.", "name"],  # Empty name
        [{"name": "word-count", "url": ""}, "This field may not be blank.", "url"],  # Empty url
        [{"url": "https://example.com/"}, "This field is required.", "name"],  # No name
        [{"name": "word-count", "url": "example"}, "Enter a valid URL.", "url"],  # Bad url
        [{"name": "word-count"}, "This field is required.", "url"],  # No url
    )
)
def test_add_bad_input(client, input, error, badfield):
    # Test we catch bad input with validation when adding services
    url = reverse('add_service')
    response = client.post(url, data=input)

    assert response.status_code == 400
    assert response.data[badfield][0] == error


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_data",
    (
        {"name": "test-service", "url": "https://example.com/"},
    )
)
def test_add(client, add_data):
    # Test we can create services

    def service_exists(target_service):
        # Helper to check if service exists
        services = ServiceManager.objects.all()
        for service in services:  # Find correct service
            if service.name == target_service:
                return True
        return False

    add_url = reverse('add_service')
    # Add Service, assert it was created
    target_service = add_data["name"]
    response = client.post(add_url, data=add_data)
    assert service_exists(target_service)
    assert response.data["message"] == "Service registered successfully"

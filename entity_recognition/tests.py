import pytest

from django.urls import reverse

from .models import EntityRecognition
from .serializers import EntityRecognitionSerializer


@pytest.mark.django_db
def test_get(client):
    url = reverse('entity_recognition')
    response = client.get(url)

    objects = EntityRecognition.objects.all()
    expected_data = EntityRecognitionSerializer(objects, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_text, result",
    (
        ["Lorem ipsum dolor sIt amet", ["Lorem"]],
        ["cOnsectetur Adipiscing Elit", ["Adipiscing", "Elit"]],
        ["Quis vel Eros donec Ac odio tempor orci Dapibus Ultrices.", ["Quis", "Eros", "Ac", "Dapibus", "Ultrices."]],
        ["nunc mattis enim. sit amet tellus cras adipiscing enim eu turpis. sed", None],
    )
)
def test_entity_recognition(client, input_text, result):
    # Test we return the "correct" entities when POST-ing to the service
    url = reverse('entity_recognition')
    response = client.post(url, data={"input_text": input_text})

    assert response.status_code == 200
    if result is None:  # If no capitalized words, just assert we get some sort of list back
        assert len(response.data["result"]) > 0
    else:  # Normal operation, we have capitalized "entities"
        assert response.data["result"] == result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "key, text, error",
    (
        ["input_text", "", "This field may not be blank."],  # Empty text 
        ["bad_key", "Quis vel eros donec", "This field is required."],  # Wrong key
    )
)
def test_entity_recognition_bad_input(client, key, text, error):
    # Test we catch bad input with validation
    url = reverse('word_count')
    response = client.post(url, data={key: text})

    assert response.status_code == 400
    assert response.data["input_text"][0] == error

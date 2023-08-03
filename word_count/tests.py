import pytest

from django.urls import reverse

from .models import WordCount
from .serializers import WordCountSerializer


@pytest.mark.django_db
def test_get(client):
    url = reverse('word_count')
    response = client.get(url)

    objects = WordCount.objects.all()
    expected_data = WordCountSerializer(objects, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_text, result",
    (
        ["Lorem ipsum dolor sit amet", 5],
        ["consectetur adipiscing elit", 3],
        ["Quis vel eros donec ac odio tempor orci dapibus ultrices.", 10],
        ["nunc mattis enim. Sit amet tellus cras adipiscing enim eu turpis. Sed", 12],
    )
)
def test_word_count(client, input_text, result):
    # Test we return the correct word count when we POST to the service
    url = reverse('word_count')
    response = client.post(url, data={"input_text": input_text})

    assert response.status_code == 200
    assert int(response.data["result"]) == result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "key, text, error",
    (
        ["input_text", "", "This field may not be blank."],  # Empty text 
        ["bad_key", "Quis vel eros donec", "This field is required."],  # Wrong key
    )
)
def test_word_count_bad_input(client, key, text, error):
    # Test we catch bad input with validation
    url = reverse('word_count')
    response = client.post(url, data={key: text})

    assert response.status_code == 400
    assert response.data["input_text"][0] == error

import pytest

from django.urls import reverse

from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer


@pytest.mark.django_db
def test_get(client):
    url = reverse('sentiment_analysis')
    response = client.get(url)

    objects = SentimentAnalysis.objects.all()
    expected_data = SentimentAnalysisSerializer(objects, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_text",
    (
        "Lorem ipsum dolor sit amet",
        "consectetur adipiscing elit",
        "Quis vel eros donec ac odio tempor orci dapibus ultrices.",
        "nunc mattis enim. Sit amet tellus cras adipiscing enim eu turpis. Sed",
    )
)
def test_sentiment_analysis(client, input_text):
    # Test we return a sentiment when POST-ing to the service
    possible_results = ["Happy", "Sad", "Angry", "Excited", "Worried", "Confused"]
    url = reverse('sentiment_analysis')
    response = client.post(url, data={"input_text": input_text})

    assert response.status_code == 200
    assert response.data["result"] in possible_results


@pytest.mark.django_db
@pytest.mark.parametrize(
    "key, text, error",
    (
        ["input_text", "", "This field may not be blank."],  # Empty text 
        ["bad_key", "Quis vel eros donec", "This field is required."],  # Wrong key
    )
)
def test_sentiment_analysis_bad_input(client, key, text, error):
    # Test we catch bad input with validation
    url = reverse('word_count')
    response = client.post(url, data={key: text})

    assert response.status_code == 400
    assert response.data["input_text"][0] == error

from django.urls import path
from .views import sentiment_analysis


urlpatterns = [
    path('analyze/', sentiment_analysis, name="sentiment_analysis")
]

from django.urls import path
from .views import word_count


urlpatterns = [
    path('count/', word_count, name="word_count")
]
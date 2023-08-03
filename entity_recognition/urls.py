from django.urls import path
from .views import entity_recognition


urlpatterns = [
    path('recognize/', entity_recognition, name="entity_recognition")
]
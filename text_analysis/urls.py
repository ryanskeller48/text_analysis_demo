from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from text_analysis.views import text_analysis, add_service, delete_service

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Text Analysis Docs")),
    path('', text_analysis, name="text_analysis"),
    path('add/', add_service, name="add_service"),
    path('delete/', delete_service, name="delete_service"),
    path('', include('entity_recognition.urls')),
    path('', include('sentiment_analysis.urls')),
    path('', include('word_count.urls')),
]

from django.urls import path
from .views import similarity_search

urlpatterns = [
    path('', similarity_search, name='similarity_search'),
]

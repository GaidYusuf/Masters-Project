from django.urls import path
from . import views

app_name = 'prayer_times'

urlpatterns = [
    path('', views.select_location, name='select_location'),
    path('prayer_times/', views.prayer_times, name='prayer_times'),
    path('api/cities/', views.fetch_cities, name='fetch_cities'),
    path('api/countries/', views.fetch_countries, name='fetch_countries'),
]

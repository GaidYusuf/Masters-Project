from django.urls import path
from . import views

urlpatterns = [
    path('surah_list/', views.surah_list, name='surah_list'),
    path('surah/<int:surah_number>/', views.surah_detail, name='surah_detail'),
    path('search/', views.search_verses, name='search_verses'),
]

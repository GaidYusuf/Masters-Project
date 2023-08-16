import datetime
import requests
from django import forms
from django.http import JsonResponse
from django.shortcuts import render


class PrayerTimesForm(forms.Form):
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)


def fetch_prayer_times(city, country):
    url = f'http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2'
    response = requests.get(url)
    data = response.json()
    return data['data']['timings']


def select_location(request):
    if request.method == 'POST':
        form = PrayerTimesForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            prayer_times_data = fetch_prayer_times(city, country)
            nearby_mosques = fetch_nearby_mosques(city, country)
            return render(request, 'prayer_times/prayer_times.html', {'prayer_times': prayer_times_data, 'nearby_mosques': nearby_mosques})
    else:
        form = PrayerTimesForm()

    return render(request, 'prayer_times/select_location.html', {'form': form})


def prayer_times(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        country = request.POST.get('country')
        prayer_times_data = fetch_prayer_times(city, country)
        nearby_mosques = fetch_nearby_mosques(city, country)
    else:
        # Default values for the initial page load
        city = 'London'
        country = 'United Kingdom'
        prayer_times_data = fetch_prayer_times(city, country)
        nearby_mosques = fetch_nearby_mosques(city, country)

    return render(request, 'prayer_times/prayer_times.html', {
        'prayer_times': prayer_times,
        'nearby_mosques': nearby_mosques,
    })


def fetch_countries(request):
    if request.method == 'GET':
        # Replace this with the actual API URL for fetching countries and cities
        api_url = 'https://countriesnow.space/api/v0.1/countries'
        response = requests.get(api_url)
        data = response.json()
        if data.get('error'):
            return JsonResponse({'error': 'Failed to fetch countries data'}, status=500)
        countries_data = data.get('data', [])
        return JsonResponse(countries_data, safe=False)
    return JsonResponse([], safe=False)


def fetch_cities(request):
    if request.method == 'GET':
        api_url = 'https://countriesnow.space/api/v0.1/countries'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            countries_data = data['data']

            # Extract all countries and their respective cities
            countries_cities = {}
            for item in countries_data:
                country_name = item['country']
                cities = item['cities']
                countries_cities[country_name] = cities

            return JsonResponse(countries_cities)
        else:
            return JsonResponse({'error': 'Failed to fetch data from the API'}, status=response.status_code)

    return JsonResponse([], safe=False)


def fetch_location_coordinates(city, country):
    GOOGLE_PLACES_API_KEY = 'AIzaSyBYEdpl74uptE7jJE05xPZKjNHqcQRIu_k'
    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': f'{city}, {country}',
        'key': GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None


def fetch_nearby_mosques(city, country):
    lat, lng = fetch_location_coordinates(city, country)
    if lat is None or lng is None:
        return []

    GOOGLE_PLACES_API_KEY = 'AIzaSyBYEdpl74uptE7jJE05xPZKjNHqcQRIu_k'
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        # 5km radius for nearby places search (adjust as needed)
        'radius': 20000,
        'type': 'mosque',
        'key': GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    mosques = []
    if 'results' in data:
        for result in data['results']:
            mosque_data = {
                'name': result.get('name', ''),
                'lat': result['geometry']['location']['lat'],
                'lng': result['geometry']['location']['lng'],
            }
            mosques.append(mosque_data)
    return mosques

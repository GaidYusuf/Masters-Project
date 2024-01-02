from django.shortcuts import render
import requests



def surah_detail(request, surah_number):
    # Fetch all verses of the Surah
    url = f"https://al-quran1.p.rapidapi.com/{surah_number}/1-286"
    headers = {
        "X-RapidAPI-Key": "c33f0ab387msh0de81eb89986f1cp1adfa8jsn03505a9cc89f",
        "X-RapidAPI-Host": "al-quran1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        verses = [data[str(i)]
                  for i in range(1, len(data) + 1)]  # Get all verses

        # Fetch Surah name and description
        url_surah_info = f"https://al-quran1.p.rapidapi.com/{surah_number}"
        response_surah_info = requests.get(url_surah_info, headers=headers)
        if response_surah_info.status_code == 200:
            data_surah_info = response_surah_info.json()
            surah_name = data_surah_info.get("surah_name_ar", "")
            surah_description = data_surah_info.get("description", "")
        else:
            surah_name = "Surah"
            surah_description = "Description not available."

        total_surahs = 114
        previous_surah = int(surah_number) - \
            1 if int(surah_number) > 1 else total_surahs
        next_surah = int(surah_number) + \
            1 if int(surah_number) < total_surahs else 1

        return render(request, 'quran/surah_detail.html', {
            'surah_number': surah_number,
            'surah_name': surah_name,
            'surah_description': surah_description,
            'verses': verses,
            'previous_surah': previous_surah,
            'next_surah': next_surah,
        })
    else:
        # Handle the case when the API request fails
        return render(request, 'quran/surah_detail.html', {'surah_number': surah_number, 'verses': []})


def surah_list(request):
    url = "https://api.quran.com/api/v4/chapters"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        surahs = data.get("chapters", [])

        return render(request, 'quran/surah_list.html', {'surahs': surahs})
    else:
        # Handle the case when the API request fails
        return render(request, 'quran/surah_list.html', {'surahs': []})


def search_verses(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        # Make API call to search for the keyword in the Quran
        url = f"https://al-quran1.p.rapidapi.com/corpus/{keyword}"
        headers = {
            "X-RapidAPI-Key": "c33f0ab387msh0de81eb89986f1cp1adfa8jsn03505a9cc89f",
            "X-RapidAPI-Host": "al-quran1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return render(request, 'quran/search_results.html', {'results': data})
        else:
            return render(request, 'quran/search_results.html', {'results': []})

    return render(request, 'quran/search_results.html', {'results': []})

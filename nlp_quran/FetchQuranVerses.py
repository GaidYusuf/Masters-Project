import requests

# API request
url = "http://api.alquran.cloud/v1/quran/en.asad"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Save the data to a text file after preprocessing
    with open('quran_data1.txt', 'w', encoding='utf-8') as file:
        for surah in data['data']['surahs']:
            for verse in surah['ayahs']:
                verse_id = verse['number']
                verse_text = verse['text']
                file.write(f"Verse ID: {verse_id}\n")
                file.write(f"Original Text: {verse_text}\n")
                file.write("=" * 50 + "\n")

    print("Data saved to 'quran_data1.txt'.")

else:
    print("Failed to fetch data from the API.")

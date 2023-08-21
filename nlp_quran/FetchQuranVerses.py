import requests
import re

translation_key = "english_saheeh"
base_url = "https://quranenc.com/api/v1/translation/aya"

# Regular expression to match footnote markers
footnote_pattern = r'\[\d+\]'

# Save the data to a text file after preprocessing
with open('quran_translations.txt', 'w', encoding='utf-8') as file:
    for surah in range(1, 115):  # Quran has 114 surahs
        ayah = 1
        while True:
            url = f"{base_url}/{translation_key}/{surah}/{ayah}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    aya_data = data["result"]
                    aya_number = aya_data['aya']
                    arabic_text = aya_data['arabic_text']
                    translation = aya_data['translation']

                    # Remove footnote markers using regular expression
                    cleaned_translation = re.sub(
                        footnote_pattern, '', translation)

                    # Remove aya_number from the cleaned translation
                    cleaned_translation = cleaned_translation.replace(
                        f"({aya_number})", '')

                    file.write(f"Verse ({surah}:{aya_number})\n")
                    file.write(f"Arabic Text: {arabic_text}\n")
                    file.write(f"Translation: {cleaned_translation.strip()}\n")
                    file.write("=" * 50 + "\n")

                ayah += 1
            else:
                break

print("Translations saved to 'quran_translations.txt'.")

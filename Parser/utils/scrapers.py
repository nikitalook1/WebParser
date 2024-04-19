import os

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from docx import Document


def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            return text
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"


def save_text_to_docx(text, filename):
    document = Document()
    document.add_paragraph(text)
    file_path = os.path.join('texts', filename)
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    document.save(full_file_path)
    return file_path  # Верните относительный путь

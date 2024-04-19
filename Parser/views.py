import os

from django.shortcuts import render, redirect
from .forms import WebsiteForm
from django.http import HttpResponse, FileResponse

from .models import Website
from .utils.scrapers import fetch_data, save_text_to_docx


def add_website(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            new_website = form.save(commit=False)
            new_website.save()  # Сначала сохраните объект, чтобы получить ID
            text = fetch_data(new_website.url)
            filename = f"website_{new_website.pk}.docx"
            file_path = save_text_to_docx(text, filename)
            new_website.text_file.name = file_path  # Сохранение относительного пути к файлу
            new_website.save()  # Повторно сохраните объект с файлом
            return redirect('success_url', website_id=new_website.pk)
    else:
        form = WebsiteForm()
    return render(request, 'add_website.html', {'form': form})


def success_view(request, website_id):
    website = Website.objects.get(id=website_id)
    # Предполагается, что в вашем шаблоне есть переменная context 'website'
    return render(request, 'success_url.html', {'website': website})

def download_text(request, website_id):
    # Предполагается, что у вас есть модель Website с полем url
    website = Website.objects.get(id=website_id)
    text = fetch_data(website.url)
    filename = f"website_{website_id}.txt"
    save_path = save_text_to_docx(text, f"temp/{filename}")  # Сохраните файл в папку temp

    # Открыть файл для чтения и создать HTTP ответ
    with open(save_path, 'r', encoding='utf-8') as file:
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    response = FileResponse(open(save_path, 'rb'), as_attachment=True, filename=filename)
    # Удаление файла после закрытия ответа
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.callback = lambda: os.remove(save_path)
    return response
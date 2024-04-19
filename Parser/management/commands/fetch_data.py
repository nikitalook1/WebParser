from django.core.management.base import BaseCommand
from Parser.models import Website, PageData
from Parser.utils.scrapers import fetch_data

class Command(BaseCommand):
    help = 'Fetches text data from websites'

    def handle(self, *args, **kwargs):
        websites = Website.objects.all()
        if not websites:
            self.stdout.write(self.style.WARNING('No websites to fetch data from.'))
            return
        for website in websites:
            self.stdout.write(f'Fetching data from {website.url}')
            content = fetch_data(website.url)
            PageData.objects.create(website=website, content=content)
            self.stdout.write(self.style.SUCCESS(f'Data fetched and saved for {website.url}'))
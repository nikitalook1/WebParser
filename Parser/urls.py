from django.urls import path
from .views import add_website, download_text

urlpatterns = [
    path('add_website/', add_website, name='add_website'),
    path('download_text/<int:website_id>/', download_text, name='download_text'),
]

from django.db import models

class Website(models.Model):
    url = models.URLField()
    text_file = models.FileField(upload_to='texts/', null=True, blank=True)

class PageData(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    content = models.TextField()

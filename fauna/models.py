from django.db import models
from destinations.models import Destinations

class Fauna(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE, related_name='fauna')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    description_2 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ImageFauna(models.Model):
    fauna = models.ForeignKey(Fauna, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='fauna/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.fauna.title}"

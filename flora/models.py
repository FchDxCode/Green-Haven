from django.db import models
from destinations.models import Destinations 

class Flora(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE, related_name='flora')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    description_2 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ImageFlora(models.Model):
    flora = models.ForeignKey(Flora, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='flora/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.flora.title}"

from django.db import models

class Destinations(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.TextField(max_length=1000)
    description = models.TextField()
    description_2 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ImageDestinations(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.destinations.title}"

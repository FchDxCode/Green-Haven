from rest_framework import serializers
from destinations.models import Destinations, ImageDestinations
from flora.models import Flora, ImageFlora
from health.models import Health, ImageHealth
from kuliner.models import Kuliner, ImageKuliner
from guides.models import Guides, ImageGuides
from fauna.models import Fauna, ImageFauna

# destinations

class ImageDestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDestinations
        fields = ['destinations', 'image', 'created_at', 'updated_at']

class DestinationsSerializer(serializers.ModelSerializer):
    images = ImageDestinationsSerializer(many=True, read_only=True)
    class Meta:
        model = Destinations
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']        

# flora
class ImageFloraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFlora
        fields = ['flora', 'image', 'created_at', 'updated_at']
    
class FloraSerializer(serializers.ModelSerializer):
    images = ImageFloraSerializer(many=True, read_only=True)
    class Meta:
        model = Flora
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']

# health
class ImageHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHealth
        fields = ['health', 'image', 'created_at', 'updated_at']
        
class HealthSerializer(serializers.ModelSerializer):
    images = ImageHealthSerializer(many=True, read_only=True)
    class Meta:
        model = Health
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']
        
# kuliner
class ImageKulinerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageKuliner
        fields = ['kuliner', 'image', 'created_at', 'updated_at']
        
class KulinerSerializer(serializers.ModelSerializer):
    images = ImageKulinerSerializer(many=True, read_only=True)
    class Meta:
        model = Kuliner
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']

# guides
class ImageGuidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGuides
        fields = ['guides', 'image', 'created_at', 'updated_at']
        
class GuidesSerializer(serializers.ModelSerializer):
    images = ImageGuidesSerializer(many=True, read_only=True)
    class Meta:
        model = Guides
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']

# fauna
class ImageFaunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFauna
        fields = ['fauna', 'image', 'created_at', 'updated_at']

class FaunaSerializer(serializers.ModelSerializer):
    images = ImageFaunaSerializer(many=True, read_only=True)
    class Meta:
        model = Fauna
        fields = ['title', 'slug', 'description', 'description_2', 'created_at', 'updated_at', 'images']


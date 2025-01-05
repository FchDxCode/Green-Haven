from rest_framework.response import Response
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from itertools import chain
from random import sample
from operator import attrgetter

class BasePublicViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        """
        Get object by ID or slug
        """
        queryset = self.get_queryset()
        lookup = self.kwargs.get(self.lookup_field)
        
        if lookup.isdigit():
            obj = get_object_or_404(queryset, id=lookup)
        else:
            obj = get_object_or_404(queryset, slug=lookup)
            
        return obj
    
# destinations    
class DestinationsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    lookup_field = 'slug'

class ImageDestinationsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageDestinations.objects.all()
    serializer_class = ImageDestinationsSerializer
    lookup_field = 'slug'
    
# flora
class FloraViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Flora.objects.all()
    serializer_class = FloraSerializer
    lookup_field = 'slug'
    
class ImageFloraViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageFlora.objects.all()
    serializer_class = ImageFloraSerializer
    lookup_field = 'slug'

# health
class HealthViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer
    lookup_field = 'slug'

class ImageHealthViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageHealth.objects.all()
    serializer_class = ImageHealthSerializer
    lookup_field = 'slug'

# kuliner
class KulinerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Kuliner.objects.all()    
    serializer_class = KulinerSerializer
    lookup_field = 'slug'

class ImageKulinerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageKuliner.objects.all()
    serializer_class = ImageKulinerSerializer
    lookup_field = 'slug'

# guides
class GuidesViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Guides.objects.all()
    serializer_class = GuidesSerializer
    lookup_field = 'slug'

class ImageGuidesViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageGuides.objects.all()
    serializer_class = ImageGuidesSerializer
    lookup_field = 'slug'

# fauna
class FaunaViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Fauna.objects.all()
    serializer_class = FaunaSerializer
    lookup_field = 'slug'

class ImageFaunaViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ImageFauna.objects.all()
    serializer_class = ImageFaunaSerializer
    lookup_field = 'slug'

class LatestContentView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Mengambil semua data dan menggabungkannya
        all_content = list(chain(
            Destinations.objects.all(),
            Flora.objects.all(),
            Fauna.objects.all(),
            Kuliner.objects.all(),
            Health.objects.all(),
            Guides.objects.all()
        ))
        
        # Urutkan berdasarkan created_at dan ambil 5 data terbaru
        latest_content = sorted(all_content, key=attrgetter('created_at'), reverse=True)[:5]
        
        # Serialize data berdasarkan tipe model
        results = []
        for item in latest_content:
            if isinstance(item, Destinations):
                results.append({
                    'type': 'destination',
                    'data': DestinationsSerializer(item).data
                })
            elif isinstance(item, Flora):
                results.append({
                    'type': 'flora',
                    'data': FloraSerializer(item).data
                })
            elif isinstance(item, Fauna):
                results.append({
                    'type': 'fauna',
                    'data': FaunaSerializer(item).data
                })
            elif isinstance(item, Kuliner):
                results.append({
                    'type': 'kuliner',
                    'data': KulinerSerializer(item).data
                })
            elif isinstance(item, Health):
                results.append({
                    'type': 'health',
                    'data': HealthSerializer(item).data
                })
            elif isinstance(item, Guides):
                results.append({
                    'type': 'guides',
                    'data': GuidesSerializer(item).data
                })

        return Response({
            'count': len(results),
            'results': results
        })

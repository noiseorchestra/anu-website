from django.urls import path, include
from sounds.models import Recording, StreamEvent
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recording
        fields = ['title', 'date', 'link', 'info']

# ViewSets define the view behavior.
class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class StreamEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StreamEvent
        fields = ['title', 'date', 'info']

# ViewSets define the view behavior.
class StreamEventViewSet(viewsets.ModelViewSet):
    queryset = StreamEvent.objects.all()
    serializer_class = StreamEventSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'recordings', RecordingViewSet)
router.register(r'events', StreamEventViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('sounds-api/', include('rest_framework.urls', namespace='rest_framework'))
]

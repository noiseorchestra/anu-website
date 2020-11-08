from rest_framework import serializers

from rest_framework import serializers

class Recordings(object):
    def __init__(self, recordings):
        self.recordings = recordings

# create a serializer
class RecordingSerializer(serializers.Serializer):
    # intialize fields
    recordings = serializers.ListField(child = serializers.CharField())

from django.contrib import admin

from .models import Recording, StreamEvent

admin.site.register(Recording)
admin.site.register(StreamEvent)

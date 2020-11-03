from django.db import models
from django.urls import reverse

class NoiseAudioWeb(models.Model):

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True)
    about = models.TextField()
    owner = models.CharField(max_length=250)
    jacktrip_hub_server = models.CharField(max_length=15)
    influxdb = models.CharField(max_length=20)
    stream_address = models.CharField(max_length=100)
    file_storage = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vue_frontend:dashboard',
                       args=[self.slug])

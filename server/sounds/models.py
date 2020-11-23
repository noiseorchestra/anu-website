from django.db import models

class Recording(models.Model):

    title = models.CharField(max_length=250)
    link = models.CharField(max_length=100)
    info = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.title

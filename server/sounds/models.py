from django.db import models

class Recording(models.Model):

    title = models.CharField(max_length=250)
    date = models.DateField()
    link = models.CharField(max_length=100)
    info = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.title

class StreamEvent(models.Model):

    title = models.CharField(max_length=250)
    date = models.DateTimeField()
    info = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.title

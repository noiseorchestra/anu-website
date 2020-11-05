from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):
    NAV_POSITION = (
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True)
    body = RichTextUploadingField()
    nav_position = models.CharField(max_length=20,
                                    choices=NAV_POSITION,
                                    default='01')

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:page',
                       args=[self.slug])

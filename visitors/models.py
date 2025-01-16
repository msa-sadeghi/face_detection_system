from django.db import models


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='visitor_photos/')
    face_encoding = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


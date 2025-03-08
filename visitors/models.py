from django.db import models
from django.utils.translation import gettext as _

class Visitor(models.Model):
    name = models.CharField(max_length=100,verbose_name= _("نام"))
    family = models.CharField(max_length=100,verbose_name= _("نام خانوادگی"))
    nationalCode = models.IntegerField(verbose_name= _("کدملی"))
    company = models.CharField(max_length=100,verbose_name= _("شرکت"))
    contact = models.CharField(max_length=100, verbose_name= _("شماره تماس"))
    photo = models.ImageField(upload_to='visitor_photos/')
    face_encoding = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("مراجعه کننده")
        verbose_name_plural  = _(" مراجعه کنندگان")
    def __str__(self):
        return self.name


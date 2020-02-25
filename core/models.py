from django.db import models
from django.utils.text import slugify


class Governorate(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='core/images/', null=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Governorate, self).save(*args, **kwargs)


class City(models.Model):
    title = models.CharField(max_length=150)
    governorate = models.ForeignKey(Governorate, on_delete=models.PROTECT, related_name='cities')
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(City, self).save(*args, **kwargs)
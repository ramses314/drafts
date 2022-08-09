from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='image/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
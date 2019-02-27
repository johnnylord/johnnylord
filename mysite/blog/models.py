from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    # DATABASE FIELD
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    slug = models.SlugField()
    feature_image = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    draft = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=timezone.localtime)
    publish_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

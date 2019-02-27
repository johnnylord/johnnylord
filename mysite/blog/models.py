from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Category(MPTTModel):
    # DATABASE FIELD
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
            'self',
            blank=True,
            null=True,
            related_name='children',
            on_delete=models.CASCADE)
    slug = models.SlugField()

    # Meta for MPTT
    class MPTTMeta:
        order_insertion_by = ['name']

    # Meta for model instance
    class Meta:
        unique_together = (('parent', 'slug'),)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


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

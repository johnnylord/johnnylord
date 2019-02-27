from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from .storage import OverwriteStorage

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

    def get_url_list(self):
        """Return a list of urls related to this category"""
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []

        slugs = [ i.slug for i in ancestors ]
        urls = []
        for i in range(len(slugs)):
            urls.append('/'.join(slugs[:i+1]))
        return urls


def get_feature_image_path(instance, filename):
    return 'blog/' + instance.slug + '-' + filename

class Post(models.Model):
    # DATABASE FIELD
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    slug = models.SlugField()
    feature_image = models.ImageField(
        storage=OverwriteStorage(),
        upload_to=get_feature_image_path,
        blank=True,
        null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    draft = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=timezone.localtime)
    publish_date = models.DateTimeField(blank=True, null=True)
    category = TreeForeignKey(
        'Category',
        blank=True,
        null=True,
        related_name='posts',
        on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/'.join([self.category.get_url_list[-1], self.slug])


@receiver(pre_delete, sender=Post)
def post_pre_delete(sender, instance, **kwargs):
    instance.feature_image.delete(save=False)

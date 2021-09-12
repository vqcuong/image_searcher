from django.db import models
from django.utils import timezone

class ImagePool(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    image_folder = models.CharField(max_length=1000, null=False, unique=True, editable=True)
    feature_file = models.CharField(max_length=1000, null=True, default=None, editable=True)
    name = models.CharField(max_length=100, null=True, default=None, editable=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

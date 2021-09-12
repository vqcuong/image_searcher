from rest_framework import serializers 
from .models import ImagePool


class ImagePoolSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = ImagePool
        fields = ('id',
                  'image_folder',
                  'feature_file',
                  'name',
                  'created_at',
                  'updated_at')

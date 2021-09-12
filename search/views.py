import os
from django.db import models
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .models import ImagePool
from .serializers import ImagePoolSerializer
from .jobs.image_pool import DirectedImagePool

def index(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST', 'DELETE'])
def image_pool(request: HttpRequest):
    if request.method == 'GET':
        image_pools = ImagePool.objects.all()
        serializer = ImagePoolSerializer(image_pools, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ImagePoolSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        deleting_id = data["id"]
        deleting_objs = ImagePool.objects.filter(id = deleting_id)
        deleting_objs.delete()
        return JsonResponse({"message": f"Deleted image pool of id: {deleting_id} successfully!"},
                status=status.HTTP_204_NO_CONTENT
            )
    else:
        return JsonResponse({"message": f"Method {request.method} doesn't supported currently"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

@api_view(['POST'])
def image_pool_detail(request: HttpRequest):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        image_folder = data['image_folder']
        image_files = os.listdir(image_folder)
        image_files = list(filter(lambda x: not x.startswith("."), image_files))
        image_files = list(map(lambda x: os.path.join(image_folder, x), image_files))
        return JsonResponse({"image_files": image_files})
    else:
        return JsonResponse({"message": f"Method {request.method} doesn't supported currently"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

@api_view(['POST'])
def search_image(request: HttpRequest):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        searching_image = data['image']
        search_threshold = data.get('threshold', 0.95)
        image_pool = ImagePool.objects.first(id = data["from_pool_id"])
        directed_pool = DirectedImagePool(
            image_folder=image_pool.image_folder,
            feature_file=image_pool.feature_file
        )
        result = directed_pool.search_image(searching_image, search_threshold)
        return JsonResponse(result)
    else:
        return JsonResponse({"message": f"Method {request.method} doesn't supported currently"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

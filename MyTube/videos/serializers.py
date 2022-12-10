from rest_framework import serializers
from django.db import models
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id','title','like','dislike','video_file','thumbnail']
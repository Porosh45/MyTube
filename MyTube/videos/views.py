from .models import  Video
from .serializers import VideoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics 
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.
# class VideoList(APIView):
#     serializer_class = VideoSerializer
#
#     def get(self,request):
#         owner = self.request.user
#         video = Video.objects.all()
#         serializer = VideoSerializer(video, many = True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         owner = self.request.user
#         serializer = VideoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status = status.HTTP_201_CREATED)
#
# class VideoDetail(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     def get_video(self, pk):
#         owner = self.request.user
#         try:
#             return Video.objects.get(pk = pk)
#         except Video.DoesNotExist:
#             return Http404
#
#     def get(self,request, pk):
#         video = get_video(pk)
#         serializer = VideoSerializer(video)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         video = self.get_video(pk)
#         owner = self.request.user
#         serializer = VideoSerializer(video, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         video = get_video(pk)
#         video.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)

class VideoList(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    permission_classes  = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner =self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = Video.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)


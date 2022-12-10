from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from User.models import User
# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='upload/video_files', validators = [FileExtensionValidator(allowed_extensions= ['mp4'])])
    thumbnail = models.FileField(upload_to='upload/thumbnails', validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])
    like = models.IntegerField(default = 0)
    dislike = models.IntegerField(default = 0)
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(to = User, related_name = 'videos', on_delete = models.CASCADE)
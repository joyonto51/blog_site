from django.db import models
from django.contrib.auth.models import User

from blog_site import settings


# class BlogManager(models.Manager):
#     def get_queryset(self):
#         return self.get_queryset().exclude(status=False).order_by('-created_at')

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    manage_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_blogs')

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='{}/'.format(id))
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    # objects = BlogManager()

    def __str__(self):
        return self.title
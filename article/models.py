import calendar
from django.db import models
from accounts.models import User
from blog_site import settings


# class BlogManager(models.Manager):
#     def get_queryset(self):
#         return self.get_queryset().exclude(status=False).order_by('-created_at')

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='childes')
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    title = models.CharField(max_length=200)
    about = models.CharField(max_length=200, default='')
    content = models.TextField()
    image = models.ImageField(upload_to='blog/image/')

    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    # objects = BlogManager()

    def __str__(self):
        return self.title

    @property
    def date(self):
        return self.updated_at.date().day

    @property
    def month(self):
        return calendar.month_name[self.updated_at.month][:3]


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text + ' - ' + self.author.full_name

    @property
    def created_datetime(self):
        date = self.created_at.date().strftime('%b %d,%Y')
        time = self.created_at.time().strftime("%I:%M %p")

        return "{}  {}".format(time, date)

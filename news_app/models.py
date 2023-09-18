from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)


class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    upload_time = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.Draft
    )
    views=models.IntegerField(default=0)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list_detail', args=[self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message = models.TextField()

    def __str__(self):
        return self.message
class Comment(models.Model):
    news=models.ForeignKey(News,
                           on_delete=models.CASCADE,
                           related_name='comments')
    user=models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name='comments')
    body=models.TextField()
    created_time=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['created_time']
    def __str__(self):
        return self.body

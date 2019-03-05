import os
import math
import random
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.text import Truncator, slugify
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save

from BlogProject.settings import base
from markdown import markdown

def get_filename_ext(filepath):
  base_name = os.path.basename(filepath)
  name, ext = os.path.splitext(base_name)
  return name, ext


def profile_image_upload_path(instance, filename):
  new_filename = random.randint(1, 387468796567)
  name, ext = get_filename_ext(filename)
  user_name = slugify(instance.__str__())
  path = os.path.join('profile_pictures', user_name)
  return os.path.join(path, '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext))


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)  
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count/20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count=self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class UserProfile(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    user = models.OneToOneField(User, related_name='user_profile')
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=profile_image_upload_path, 
                                        storage=FileSystemStorage(location=base.MEDIA_ROOT), 
                                        null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.user.username













@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()
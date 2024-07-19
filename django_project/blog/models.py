from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #used default to give option to change time & date posted
    author = models.ForeignKey(User, on_delete=models.CASCADE) #if the suer is deleted their post should also be deleted that why using (on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')

  
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={ 'pk' : self.pk})
  

    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name="comments")
    name = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' %(self.post.title, self.name)


    
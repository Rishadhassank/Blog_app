from django.db import models
from django.contrib.auth.models import User
from PIL import Image # type: ignore




# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)       # to run the same method of parent class , we use 'super'

        img = Image.open(self.image.path)

        # Resize the image if it's larger than 300x300
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_level=models.IntegerField(default=1)
    score=models.IntegerField(default=0)
    rank=models.IntegerField(default=0)

    @classmethod
    def create(cls,user):
        user_info=cls( user=user)
        user_info.rank=user.pk  
        return user_info

    def __str__(self):
        return str(self.user)

class Question(models.Model):
    heading=models.CharField(max_length=200,unique=True)
    question_no=models.IntegerField(default=1)
    product_image = models.ImageField(upload_to='question_images')
    question_answer=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return str(self.heading)


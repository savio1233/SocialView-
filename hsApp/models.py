from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    document = models.FileField(upload_to="docs")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tags(models.Model):
    date = models.DateField(auto_now_add=True,null=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    totalCount = models.IntegerField(default=0,null=True)
    poCount = models.IntegerField(default=0,null=True)
    neCount = models.IntegerField(default=0,null=True)
    nuCount = models.IntegerField(default=0,null=True)



class Post(models.Model):
    idea = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    desc = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)



class Comments(models.Model):
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    idea = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Feedback(models.Model):
    date = models.DateField(auto_now_add=True)
    feedback = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Chat(models.Model):
    date = models.DateField(auto_now_add=True)
    sender = models.EmailField()
    receiver = models.EmailField()
    message = models.CharField(max_length=200)


class Detection(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    results = models.CharField(max_length=200, null=True)
    scoreTitle = models.CharField(max_length=200, null=True)
    scoreDesc = models.CharField(max_length=200, null=True)

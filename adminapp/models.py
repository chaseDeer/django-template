from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=64)
    language = models.CharField(max_length=64)
    imageurl = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
    updata_time = models.DateTimeField(auto_now=True)
    readnum = models.CharField(max_length=128)
    articlecontent = models.TextField()


class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    is_login = models.IntegerField(default=0)
    creat_time = models.DateTimeField(auto_now_add=True)

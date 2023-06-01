from django.db import models


# Create your models here.

class Admins(models.Model):
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=128)
    is_superadmin = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Users(models.Model):
    openid = models.CharField(max_length=128)
    age = models.CharField(max_length=128)
    gender = models.CharField(max_length=128)
    avatar_url = models.CharField(max_length=512)
    nickname = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Images(models.Model):
    image_name = models.CharField(max_length=256)
    image_url = models.CharField(max_length=256)
    image_type = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Records(models.Model):
    user_id = models.CharField(max_length=128)
    images_id = models.CharField(max_length=512)
    level = models.CharField(max_length=256)
    is_finshed = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Lunbo(models.Model):
    lunbo_url = models.CharField(max_length=512)
    is_start = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

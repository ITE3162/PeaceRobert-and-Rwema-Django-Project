from enum import unique
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


STATUS=((0,"Draft"),(1,"published"))
class Post(models.Model):
    title = models.CharField(max_length=200)
    tags= models.CharField(max_length=200)
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.IntegerField(choices=STATUS, default=0)
    thumbnail = models.ImageField(upload_to='images/')

    class Meta:
        ordering=['-created_on']

    def _str_(self):
        return self.title

class Contact(models.Model):
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message=models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_on']

    def _str_(self):
        return self.email


class Team(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    profile = models.ImageField(upload_to='team')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.name

class About(models.Model):
    content = models.TextField()
    profile = models.ImageField(upload_to='service')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.content

class What_we_do(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.ImageField(upload_to='service')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.content
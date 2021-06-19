from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)


class Topic(models.Model):
    name = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class Comment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    message = models.TextField()

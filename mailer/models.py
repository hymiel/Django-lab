"""메일 발송 모델 예시"""
from django.db import models

# Create your models here.

class Email(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()

    class Meta:
        ordering = ['name']
        db_table = 'email'

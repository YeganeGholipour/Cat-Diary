from django.db import models
from django.contrib.auth.models import User

class CatDiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    entry = models.TextField()
    # photo = models.ImageField(upload_to='cat_photos/')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

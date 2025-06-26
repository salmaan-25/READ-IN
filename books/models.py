# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.IntegerField()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_url = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book_id']

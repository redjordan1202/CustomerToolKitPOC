from django.db import models

# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.name

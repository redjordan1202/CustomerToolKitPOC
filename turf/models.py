from django.db import models

from categories.models import Category
# Create your models here.

class TurfType(models.Model):
    name = models.CharField(max_length=255)
    pile_height = models.DecimalField(decimal_places=2, max_digits=4)
    blade_shape = models.CharField(max_length=50)
    blade_material = models.CharField(max_length=50)
    tuft_bind_strength = models.IntegerField()
    backing_material = models.CharField(max_length=50)
    warranty_length = models.IntegerField()
    spec_sheet_url = models.URLField(max_length=255)
    pet_friendly = models.BooleanField()
    sports_field = models.BooleanField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

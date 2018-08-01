from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=250)
    year = models.IntegerField()
    genres = models.CharField(max_length=250)
    rating = models.DecimalField(decimal_places=1,max_digits=3)


    def __str__(self):
        return self.title


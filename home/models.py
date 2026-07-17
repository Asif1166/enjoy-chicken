from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CV(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cvs')
    file = models.FileField(upload_to='cvs/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.category.name}"
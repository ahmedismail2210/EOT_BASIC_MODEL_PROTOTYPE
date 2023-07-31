from django.db import models
from autoslug import AutoSlugField


class properties(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="properties/%y/%m/%d/" , null=True , default=None)
    no_rooms = models.CharField(max_length=1 ,null=True , default=None)
    price = models.CharField(max_length=5 ,null=True , default=None)
    fans = models.CharField(max_length=2 ,null=True , default=None)
    slug= AutoSlugField(populate_from="title" , unique=True, null=True , default=None)
    
    
class Review(models.Model):
    text = models.TextField(null=True)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(null=True )
    property = models.CharField(max_length=100 )
    address = models.CharField(max_length=200 )
    img = models.ImageField(upload_to="property/%y/%m/%d/" , null=True , default=None)


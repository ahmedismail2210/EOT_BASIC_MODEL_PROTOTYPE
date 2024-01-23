from django.db import models
from django.contrib.auth.models import User


class NewReview(models.Model):
  text = models.TextField()
  author = models.CharField(max_length=100)
  date = models.DateTimeField()
  property = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  length = models.IntegerField()
  reasonableness = models.IntegerField()
  comprehensiveness = models.IntegerField()
  relevancy = models.IntegerField()
  tonality = models.FloatField()

  def __str__(self):
    return f"Reviewed by: {self.author}"


class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  image = models.ImageField(upload_to="properties/%y/%m/%d/",
                            null=True,
                            default=None)
  bio = models.CharField(max_length=200)

  def __str__(self):
    return self.user.username

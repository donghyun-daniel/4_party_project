from django.db import models
# Create your models here.

# HotelName,HotelAddress,HotelRating,Date,ReviewRating,ReviewTitle,ReviewText

class RawData(models.Model):
    def __str__(self):
        return str(self.id)
    id = models.AutoField(primary_key=True, default=0)
    HotelName = models.TextField()
    HotelAddress = models.TextField()
    HotelRating = models.FloatField()
    ReviewDate = models.TextField()
    ReviewRating = models.FloatField()
    ReviewTitle = models.TextField()
    ReviewText = models.TextField(default="")

class Hotel(models.Model):
    def __str__(self):
        return str(self.idx)
    idx = models.IntegerField(default=0)
    text = models.TextField(default='')
    label = models.IntegerField()
    # HotelName = models.TextField()
    # HotelAddress = models.TextField()
    # HotelRating = models.FloatField()
    # ReviewDate = models.DateField()
    # ReviewTitle = models.TextField()
    # ReviewRating = models.FloatField()
    # Positive = models.TextField(default="")
    # Positive = models.TextField(default="")

class UploadFile(models.Model):
    def __str__(self):
        return self.file.name
    file = models.FileField(upload_to="rawfile")
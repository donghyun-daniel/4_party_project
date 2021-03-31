from django.contrib import admin
from .models import UploadFile
from .models import RawData

# Register your models here.
admin.site.register(UploadFile)
admin.site.register(RawData)
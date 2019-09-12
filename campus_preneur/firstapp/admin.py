from django.contrib import admin
from firstapp import models

# Register your models here

admin.site.register(models.UserInfo)
admin.site.register(models.Question)

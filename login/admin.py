
# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Project)
admin.site.register(models.Status)
admin.site.register(models.ProjectType)
admin.site.register(models.Language)

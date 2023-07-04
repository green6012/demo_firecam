from django.contrib import admin
from .models import Camera
from .models import Warning

# Register your models here.
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user')

class WarningAdmin(admin.ModelAdmin):
    list_display = ('time', 'location', 'user')

admin.site.register(Camera, CameraAdmin)
admin.site.register(Warning, WarningAdmin)
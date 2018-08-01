from django.contrib import admin

# Register your models here.
from .models import Movies


admin.site.register(Movies)

class MovieAdmin(admin.ModelAdmin):
    list_display = '__all__'

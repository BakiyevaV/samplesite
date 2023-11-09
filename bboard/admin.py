from django.contrib import admin
from .models import Bb

# Register your models here.

class BbAdmin(admin.ModelAdmin):
    list_display = ('title','price','publiched')
    list_display_links = ('title',)
    search_fields = ('title','content')
admin.site.register(Bb,BbAdmin)
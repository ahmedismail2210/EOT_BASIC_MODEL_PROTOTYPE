from django.contrib import admin
from .models import properties , Review


class adminProperties(admin.ModelAdmin):
    list_display = ('title' , 'desc' , 'image' , 'slug')


class adminReview(admin.ModelAdmin):
    list_display = ('text' , 'author' ,'date' , 'property' ,'address' , 'img')
    
admin.site.register(properties , adminProperties)
admin.site.register(Review , adminReview)



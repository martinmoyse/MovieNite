from django.contrib import admin
from .models import ListedShow, User, List

# Register your models here.
admin.site.register(User)
admin.site.register(List)
admin.site.register(ListedShow)
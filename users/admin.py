from django.contrib import admin

from users.models import Message, Profiles, Skills

# Register your models here.
admin.site.register(Profiles)
admin.site.register(Skills)
admin.site.register(Message)

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Inventory)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(RequestRecord)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

    
class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Sales)
admin.site.register(DrugItemsSales)
admin.site.register(EmailReceivers)
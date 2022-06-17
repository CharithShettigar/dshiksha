from django.contrib import admin

# Register your models here.

from . import models as sm

admin.site.register(sm.Class)
admin.site.register(sm.AssignClass)
admin.site.register(sm.Subject)
admin.site.register(sm.Chapter)
admin.site.register(sm.Staff)
admin.site.register(sm.Accountant)
admin.site.register(sm.School)
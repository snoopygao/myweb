from django.contrib import admin
from .models import OpsRecord, Engineer, Project
# Register your models here.

admin.site.register(OpsRecord)
# @admin.register(OpsRecord)
# class OpsReAdmin(admin.ModelAdmin):
#     list_display = ('', '', '', '',)
admin.site.register(Engineer)
admin.site.register(Project)

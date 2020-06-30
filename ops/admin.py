from django.contrib import admin
from .models import OpsRecord


@admin.register(OpsRecord)
class OpsReAdmin(admin.ModelAdmin):
    list_display = ('hans_name', 'source', 'qcategory', 'project', 'area', 'qdate', 'qmethod', 'short_q', 'short_p', 'result', 'limit', 'spending')
    list_display_links = ('short_q', )
    list_filter = ('qcategory', 'area', 'qdate')
    search_fields = ('project__project_name', )
    list_per_page = 10

    def hans_name(self, obj):
        return obj.engineer.last_name + obj.engineer.first_name
    hans_name.short_description = '处理人'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['engineer', 'source', 'qcategory', 'project', 'area', 'qdate', 'qmethod', 'question', 'limit']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not change:
            obj.engineer = request.user
        obj.save()



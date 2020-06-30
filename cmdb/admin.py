from django.contrib import admin
from .models import *
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        })
    return ctx


admin.site.site_header = '集成售后运维CMDB系统'
admin.site.site_title = '美好的一天'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'contract_type', 'project', 'start', 'end', 'file')


admin.site.register(City)
admin.site.register(AssetType)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotline', 'local_manager')


@admin.register(DataCenter)
class DCAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'project')


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'dc', 'need_ops')


@admin.register(Production)
class ProAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'pro_link', 'login')


@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ('project_name', 'project_type', 'commit_date', 'warranty_start_date', 'warranty_end_date', 'ops_start_data', 'ops_require')
    actions = ['导出']
    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


class ServerIfInline(admin.StackedInline):
    model = Interface
    exclude = ['switch_related', 'security_related', 'storage_related']
    extra = 1


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    inlines = [ServerIfInline]
    list_display = ('asset_name', 'supllier', 'model', 'sn', 'os_ip', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


class SwitchIfInline(admin.StackedInline):
    model = Interface
    exclude = ['server_related', 'security_related', 'storage_related']
    extra = 1


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    inlines = [SwitchIfInline]
    list_display = ('asset_name', 'supllier', 'model', 'sn', 'device_type', 'app_type', 'net_type', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


admin.site.register(VirtualInterface)


class StorageIfInline(admin.StackedInline):
    model = Interface
    exclude = ['server_related', 'switch_related', 'security_related']
    extra = 1


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [StorageIfInline]
    list_display = ('asset_name', 'supllier', 'model', 'sn', 'role', 'controller', 'mnt_address', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


admin.site.register(SafetyType)


class SecurityIfInline(admin.StackedInline):
    model = Interface
    exclude = ['server_related', 'switch_related', 'storage_related']
    extra = 1


@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    inlines = [SecurityIfInline]


@admin.register(VirtualServer)
class VirSerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'os', 'login_method', 'login_pass', 'platform')


@admin.register(DigitalAsset)
class DigiAstAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'supllier', 'soft_type', 'auth_type', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


admin.site.register(fhsds)


@admin.register(FHSD)
class FHSDAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'supllier', 'device_type', 'model', 'sn', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


admin.site.register(OfficeDev)


@admin.register(OfficeDevice)
class OfficeDeviceAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'supllier', 'device_type', 'model', 'sn', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


admin.site.register(EPs)


@admin.register(EndPointDevice)
class EPDAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'supllier', 'eps_type', 'model', 'sn', 'gbid', 'mnt_address', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')


@admin.register(Lines)
class LinesAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'supllier', 'model', 'sn', 'line_speed', 'mnt_address', 'line_addr', 'warrany_start_date', 'warrany_end_date', 'project', 'asset_status')
    exclude = ('height', )


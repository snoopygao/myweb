from django.db import models
from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Engineer(models.Model):
    pass


# 地市
class City(models.Model):
    name = models.CharField(max_length=8, verbose_name='地市字典')

    class Meta:
        verbose_name = '地市字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目
class Project(models.Model):
    project_types = (
        (0, '建设型'),
        (1, '服务型'),
        (2, '建设带维护'),
    )
    project_name = models.CharField(max_length=50, verbose_name='项目名称')
    project_type = models.IntegerField(choices=project_types, verbose_name='项目类型')
    commit_date = models.DateField(verbose_name='验收日期')
    warranty_start_date = models.DateField(verbose_name='保修开始日期')
    warranty_end_date = models.DateField(verbose_name='保修结束日期')
    ops_start_data = models.DateField(verbose_name='交维日期')
    ops_require = models.TextField(verbose_name='售后主要内容', help_text='响应时间，响应方式，SLA等')
    patrol_require = models.TextField(blank=True, null=True, verbose_name='巡检要求', help_text='内容，频次，报告相关要求等')
    project_participate = models.CharField(max_length=50, verbose_name='项目参与人', help_text='填写项目经理及工程师')
    ops_engineer = models.ForeignKey(Engineer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='维护承接人')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ["warranty_end_date"]

    def __str__(self):
        return self.project_name


# 合同
class Contract(models.Model):
    contract_types = (
        (0, '采购'),
        (1, '销售'),
    )
    name = models.CharField(max_length=50, verbose_name='合同名称')
    contract_type = models.IntegerField(choices=contract_types, verbose_name='合同类型')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='所属项目')
    start = models.DateField(verbose_name='合同开始时间')
    end = models.DateField(verbose_name='合同终止时间')
    file = models.FileField(upload_to='files/contract/')
    contact = models.CharField(max_length=30, verbose_name='联系人', help_text='供货商/采购者主要联系人和联系方式')

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 资产类型
class AssetType(models.Model):
    name = models.CharField(max_length=20, verbose_name='资产类型字典', help_text='请使用通用型的分类，如:PC，服务器，交换机')

    class Meta:
        verbose_name = '资产类型字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 厂商和供应商
class Supplier(models.Model):
    name = models.CharField(max_length=40, verbose_name='厂家/供货商', help_text='标准品牌厂商或其它供货商')
    hotline = models.CharField(max_length=30, verbose_name='400/电话', help_text='报修电话')
    local_manager = models.CharField(max_length=30, blank=True, null=True, verbose_name='本地联系人', help_text='记录姓名和电话')

    class Meta:
        verbose_name = '厂家/供货商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 机房
class DataCenter(models.Model):
    name = models.CharField(max_length=30, verbose_name='机房/建筑名称')
    address = models.CharField(max_length=50, verbose_name='地址')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='所属项目')
    contact = models.CharField(max_length=50, verbose_name='机房/建筑联系人', help_text='记录进入机房/建筑需要联系的人及方式')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 机柜
class Rack(models.Model):
    name = models.CharField(max_length=10, verbose_name='机柜编号', help_text='类似A01,B05等')
    height = models.IntegerField(verbose_name='机柜高度U')
    dc = models.ForeignKey(DataCenter, verbose_name='所在机房', on_delete=models.SET_NULL, blank=True, null=True)
    ops = (
        (0, '不需要'),
        (1, '需要'),
    )
    need_ops = models.IntegerField(verbose_name='是否需要维护', choices=ops, default=1)

    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 业务
class Production(models.Model):
    pro_types = (
        (0, '虚拟化'),
        (1, '数据库'),
        (2, 'HA双机'),
        (3, '容灾'),
        (4, '监控业务'),
        (5, '分布式'),
        (6, '其它业务')
    )
    name = models.CharField(max_length=30, verbose_name='业务名称')
    type = models.IntegerField(choices=pro_types, verbose_name='业务类型', help_text='交换机和安全设备的堆叠可归类到HA或虚拟化')
    pro_link = models.URLField(verbose_name='业务地址')
    login = models.CharField(max_length=30, verbose_name='用户名和密码')

    class Meta:
        verbose_name = '业务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 通用资产抽象
class AssetCommon(models.Model):
    status = (
        ('在用', '在用'),
        ('闲置', '闲置'),
        ('下架', '下架'),
    )
    asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, verbose_name='资产类型')
    asset_name = models.CharField(max_length=30, verbose_name='资产名称')
    supllier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='品牌/供应商')
    model = models.CharField(max_length=30, verbose_name='资产型号')
    sn = models.CharField(max_length=50, verbose_name='序列号/ID/SN')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='所属项目')
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, verbose_name='关联合同')
    warrany_start_date = models.DateField(verbose_name='保修开始时间')
    warrany_end_date = models.DateField(verbose_name='保修结束时间')
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='所在机柜')
    height = models.IntegerField(verbose_name='资产高度/u', blank=True, null=True)
    production = models.ForeignKey(Production, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='所属业务')
    mnt_address = models.GenericIPAddressField(verbose_name='管理地址', blank=True, null=True)
    mnt_pass = models.CharField(max_length=20, verbose_name='用户名密码', blank=True, null=True)
    asset_status = models.CharField(max_length=10, choices=status, verbose_name='资产状态')
    memo = models.CharField(max_length=50, blank=True, null=True, verbose_name='备注')

    class Meta:
        abstract = True
        ordering = ['project', 'asset_type', 'asset_status']


# 接口
class Interface(models.Model):
    p_mode = (
        (0, '以太光'),
        (1, '以太电'),
        (2, 'IB'),
        (3, 'FCoE'),
        (4, '串口'),
    )
    p_speed = (
        (0, '1000M'),
        (1, '10G'),
        (2, '100M'),
        (3, '40G'),
        (4, '2G'),
        (5, '4G'),
        (6, '8G'),
        (7, '16G'),
        (8, '9600K'),
    )
    c_mode = (
        (0, 'ACCESS'),
        (1, 'TRUNK'),
        (2, 'iSCSI'),
        (3, 'FC'),
        (4, '其它'),
    )
    interface_code = models.CharField(max_length=20, verbose_name='接口编号', help_text='按设备内部识别填写"本地连接1|ens160|G0/0/1"')
    physical_mode = models.IntegerField(choices=p_mode, default=1, verbose_name='端口类型')
    speed = models.IntegerField(choices=p_speed, default=0, verbose_name='端口速率')
    port_mode = models.IntegerField(choices=c_mode, default=0, verbose_name='配置类型')
    vlan_code = models.IntegerField(verbose_name='Vlan编号', blank=True, null=True)
    ip_info = models.GenericIPAddressField(verbose_name='地址信息', blank=True, null=True, help_text='填写IP地址')
    neighbor = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='对端接口')
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    server_related = models.ForeignKey('Server', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='所属服务器')
    switch_related = models.ForeignKey('Switch', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='所属网络设备')
    storage_related = models.ForeignKey('Storage', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='所属存储设备')
    security_related = models.ForeignKey('Security', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='所属安全设备')

    class Meta:
        verbose_name = '物理接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.interface_code


# 虚拟接口
class VirtualInterface(models.Model):
    v_types = (
        (0, '聚合'),
        (1, 'vlanif'),
        (2, '子接口'),
    )
    name = models.CharField(max_length=30, verbose_name='接口名称')
    v_type = models.IntegerField(choices=v_types, default=1, verbose_name='接口类型')
    interface = models.ForeignKey(Interface, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='所属接口')
    address = models.CharField(max_length=50, verbose_name='地址信息')

    class Meta:
        verbose_name = '虚拟接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 服务器
class Server(AssetCommon):
    types = (
        (0, '机架'),
        (1, '塔式'),
        (2, '刀片'),
    )
    type = models.IntegerField(choices=types, default=0, verbose_name='服务器架构')
    cpu = models.CharField(max_length=40, verbose_name='CPU信息', help_text='Intel(R) Xeon(R) CPU E7-4809 v2 @ 1.90GHz *2')
    memory = models.CharField(max_length=30, verbose_name='内存信息', help_text='32GB * 16')
    disk = models.CharField(max_length=40, verbose_name='硬盘信息', help_text='SAS-SSD*2-RAID1-SYS; SATA-HDD*3-RAID5-DATA')
    power_supply = models.CharField(max_length=30, verbose_name='电源信息', help_text='750W * 2')
    os = models.CharField(max_length=40, verbose_name='操作系统', help_text='Windows server 2016 DateCenter/CentOS 7.3')
    os_ip = models.GenericIPAddressField(verbose_name='系统IP地址')
    login_method = models.CharField(max_length=30, verbose_name='系统登录方式', help_text='远程桌面/SSH等')
    login_pass = models.CharField(max_length=30, verbose_name='用户名密码')
    # network_card = GenericRelation(Interface)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


# 存储
class Storage(AssetCommon):
    roles = (
        (0, '主控柜'),
        (1, '扩展柜'),
        (2, '备份一体机'),
        (3, '虚拟带库'),
        (4, '光盘库'),
    )
    ctl = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
    )
    role = models.IntegerField(verbose_name='设备角色', choices=roles, default=0)
    disk = models.CharField(max_length=50, verbose_name='硬盘信息', help_text='SAS-SSD*10-RAID10;SAS-HDD*15-RAID6')
    controller = models.IntegerField(verbose_name='控制器数量', choices=ctl, default=2)
    power_supply = models.CharField(max_length=30, verbose_name='电源信息', help_text='750W * 2')

    class Meta:
        verbose_name = '存储'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


# 网络设备
class Switch(AssetCommon):
    d_type = (
        (0, '核心'),
        (1, '接入'),
        (2, '汇聚'),
    )
    a_type = (
        (0, '业务交换机'),
        (1, '管理交换机'),
        (2, '存储交换机'),
        (3, '业务路由器'),
        (4, '管理路由器'),
    )
    n_type = (
        (0, '以太网'),
        (1, 'FC'),
        (2, 'FCoE'),
    )
    device_type = models.IntegerField(verbose_name='设备应用类型', choices=d_type, default=1)
    app_type = models.IntegerField(verbose_name='设备业务类型', choices=a_type, default=0)
    net_type = models.IntegerField(verbose_name='设备网络类型', choices=n_type, default=0)
    # interface = models.ForeignKey(Interface, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='接口信息')
    power_supply = models.CharField(max_length=30, verbose_name='电源信息', help_text='75W * 2')
    lic = models.CharField(max_length=1000, blank=True, null=True, verbose_name='设备授权信息')
    neighbor = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='关联设备')
    configuration = models.TextField(max_length=3000, verbose_name='配置备份', help_text='将设备的配置信息粘贴到此处')

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


# 安全设备
class SafetyType(models.Model):
    name = models.CharField(max_length=20, verbose_name='安全设备类型字典')

    class Meta:
        verbose_name = '安全设备类型字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Security(AssetCommon):
    app_type = models.ForeignKey(SafetyType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='设备类型')
    # interface = models.ForeignKey(Interface, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='接口信息')
    power_supply = models.CharField(max_length=30, verbose_name='电源信息', help_text='750W * 2')
    disk = models.CharField(max_length=30, blank=True, null=True, verbose_name='硬盘信息', help_text='若含有硬盘，请记录。')
    lic = models.CharField(max_length=1000, blank=True, null=True, verbose_name='设备授权信息')
    configuration = models.TextField(max_length=3000, verbose_name='配置备份', help_text='将设备的配置信息粘贴到此处')

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


# 虚拟机
class VirtualServer(models.Model):
    name = models.CharField(max_length=30, verbose_name='虚拟机名称')
    cpu = models.CharField(max_length=10, verbose_name='CPU信息', help_text='CPU数量')
    memory = models.CharField(max_length=10, verbose_name='内存信息', help_text='内存大小 GB')
    disk = models.CharField(max_length=20, verbose_name='硬盘信息', help_text='数量及大小')
    ip = models.CharField(max_length=20, verbose_name='网卡及IP地址')
    os = models.CharField(max_length=40, verbose_name='操作系统', help_text='Windows server 2016 DateCenter/CentOS 7.3')
    login_method = models.CharField(max_length=30, verbose_name='系统登录方式', help_text='远程桌面/SSH等')
    login_pass = models.CharField(max_length=30, verbose_name='用户名密码')
    platform = models.ForeignKey(Production, on_delete=models.SET_NULL, null=True, verbose_name='承载平台')

    class Meta:
        verbose_name = '虚拟机'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 数字资产
class DigitalAsset(AssetCommon):
    soft_types = (
        (0, '操作系统'),
        (1, '办公软件'),
        (2, '业务软件'),
        (3, '功能模块'),
    )
    auth_types = (
        (0, '永久授权'),
        (1, '带有效期'),
        (2, '临时授权'),
    )
    soft_type = models.IntegerField(verbose_name='软件类型', choices=soft_types, default=0)
    auth_type = models.IntegerField(verbose_name='授权类型', choices=auth_types, default=0)
    model = models.CharField(verbose_name='详细授权信息', max_length=100, help_text='Windows Server 2016 DataCenter * 10 永久;'
                                                                                    'Office 365 * 50 2022年9月30日；'
                                                                                    'IDS 模块 * 2 2020年10月1日')
    sn = models.TextField(verbose_name='KEY文件', max_length=5000)

    class Meta:
        verbose_name = '数字资产'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


class fhsds(models.Model):
    name = models.CharField(max_length=20, verbose_name='基础环境字典', help_text='按照风火水电大类添加')

    class Meta:
        verbose_name = '基础环境字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 风火水电
class FHSD(AssetCommon):
    device_type = models.ForeignKey(fhsds, on_delete=models.SET_NULL, null=True, verbose_name='设备类型')

    class Meta:
        verbose_name = '基础环境设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_type


class OfficeDev(models.Model):
    name = models.CharField(max_length=20, verbose_name='办公设备字典', help_text='按照大类添加')

    class Meta:
        verbose_name = '办公设备字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 办公设备
class OfficeDevice(AssetCommon):
    device_type = models.ForeignKey(OfficeDev, on_delete=models.SET_NULL, null=True, verbose_name='设备类型')

    class Meta:
        verbose_name = '办公设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_type


class EPs(models.Model):
    name = models.CharField(max_length=20, verbose_name='终端设备字典', help_text='按照大类添加')

    class Meta:
        verbose_name = '终端设备字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 终端设备
class EndPointDevice(AssetCommon):
    eps_type = models.ForeignKey(EPs, on_delete=models.PROTECT, verbose_name='终端设备类型')
    gbid = models.CharField(max_length=30, verbose_name='编码', help_text='设备ID，视频国标18位数字，其它按相应规则填写', null=True, blank=True)

    class Meta:
        verbose_name = '终端设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


# 线路
class Lines(AssetCommon):
    types = (
        (0, '互联网专线'),
        (1, '电路'),
        (2, '普通宽带'),
        (3, '物联网卡'),
        (4, 'IPTV'),
        (5, '固话/手机卡'),
    )
    model = models.IntegerField(verbose_name='线路类型', choices=types)
    line_speed = models.CharField(max_length=10, verbose_name='线路速率', help_text='M或G')
    line_addr = models.CharField(max_length=100, verbose_name='线路物理地址', help_text='物联网卡和手机卡可定位到车辆或人员')
    sn = models.CharField(max_length=20, verbose_name='线路代号', help_text='专线的代号，用于报修')
    supllier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='运营商')
    mnt_address = models.GenericIPAddressField(verbose_name='出口地址', blank=True, null=True)
    mnt_pass = models.CharField(max_length=20, verbose_name='拨号鉴权信息', blank=True, null=True)

    class Meta:
        verbose_name = '线路'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name




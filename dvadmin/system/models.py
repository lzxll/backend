import hashlib
import os

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix, get_custom_app_models


class Role(CoreModel):
    name = models.CharField(
        max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, unique=True,
                           verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(
        default=1, verbose_name="角色顺序", help_text="角色顺序")
    status = models.BooleanField(
        default=True, verbose_name="角色状态", help_text="角色状态")

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class CustomUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = super(CustomUserManager, self).create_superuser(
            username, email, password, **extra_fields)
        user.set_password(password)
        try:
            user.role.add(Role.objects.get(name="管理员"))
            user.save(using=self._db)
            return user
        except ObjectDoesNotExist:
            user.delete()
            raise ValidationError(
                "角色`管理员`不存在, 创建失败, 请先执行python manage.py init")


class Users(CoreModel, AbstractUser):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="用户账号",
                                help_text="用户账号")
    email = models.EmailField(
        max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(
        max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(
        max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    USER_TYPE = (
        (0, "后台用户"),
        (1, "前台用户"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True, help_text="用户类型"
    )
    post = models.ManyToManyField(to="Post", blank=True, verbose_name="关联岗位", db_constraint=False,
                                  help_text="关联岗位")
    role = models.ManyToManyField(to="Role", blank=True, verbose_name="关联角色", db_constraint=False,
                                  help_text="关联角色")
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="所属部门",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联部门",
    )
    objects = CustomUserManager()

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Post(CoreModel):
    name = models.CharField(null=False, max_length=64,
                            verbose_name="岗位名称", help_text="岗位名称")
    code = models.CharField(
        max_length=32, verbose_name="岗位编码", help_text="岗位编码")
    sort = models.IntegerField(
        default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        (0, "离职"),
        (1, "在职"),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name="岗位状态", help_text="岗位状态")

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "岗位表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(
        max_length=64, verbose_name="部门名称", help_text="部门名称")
    key = models.CharField(max_length=64, unique=True, null=True,
                           blank=True, verbose_name="关联字符", help_text="关联字符")
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(
        max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(
        max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(
        max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(
        default=True, verbose_name="部门状态", null=True, blank=True, help_text="部门状态")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级部门",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级部门",
    )

    @classmethod
    def recursion_all_dept(cls, dept_id: int, dept_all_list=None, dept_list=None):
        """
        递归获取部门的所有下级部门
        :param dept_id: 需要获取的id
        :param dept_all_list: 所有列表
        :param dept_list: 递归list
        :return:
        """
        if not dept_all_list:
            dept_all_list = Dept.objects.values("id", "parent")
        if dept_list is None:
            dept_list = [dept_id]
        for ele in dept_all_list:
            if ele.get("parent") == dept_id:
                dept_list.append(ele.get("id"))
                cls.recursion_all_dept(ele.get("id"), dept_all_list, dept_list)
        return list(set(dept_list))

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Menu(CoreModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.CASCADE,
        verbose_name="上级菜单",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="上级菜单",
    )
    icon = models.CharField(
        max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    name = models.CharField(
        max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.BooleanField(
        default=False, verbose_name="是否外链", help_text="是否外链")
    link_url = models.CharField(
        max_length=255, verbose_name="链接地址", null=True, blank=True, help_text="链接地址")
    is_catalog = models.BooleanField(
        default=False, verbose_name="是否目录", help_text="是否目录")
    web_path = models.CharField(
        max_length=128, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(
        max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    component_name = models.CharField(max_length=50, verbose_name="组件名称", null=True, blank=True,
                                      help_text="组件名称")
    status = models.BooleanField(
        default=True, blank=True, verbose_name="菜单状态", help_text="菜单状态")
    cache = models.BooleanField(
        default=False, blank=True, verbose_name="是否页面缓存", help_text="是否页面缓存")
    visible = models.BooleanField(default=True, blank=True, verbose_name="侧边栏中是否显示",
                                  help_text="侧边栏中是否显示")
    is_iframe = models.BooleanField(
        default=False, blank=True, verbose_name="框架外显示", help_text="框架外显示")
    is_affix = models.BooleanField(
        default=False, blank=True, verbose_name="是否固定", help_text="是否固定")

    @classmethod
    def get_all_parent(cls, id: int, all_list=None, nodes=None):
        """
        递归获取给定ID的所有层级
        :param id: 参数ID
        :param all_list: 所有列表
        :param nodes: 递归列表
        :return: nodes
        """
        if not all_list:
            all_list = Menu.objects.values("id", "name", "parent")
        if nodes is None:
            nodes = []
        for ele in all_list:
            if ele.get("id") == id:
                parent_id = ele.get("parent")
                if parent_id is not None:
                    cls.get_all_parent(parent_id, all_list, nodes)
                nodes.append(ele)
        return nodes

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class MenuField(CoreModel):
    model = models.CharField(max_length=64, verbose_name='表名')
    menu = models.ForeignKey(
        to='Menu', on_delete=models.CASCADE, verbose_name='菜单', db_constraint=False)
    field_name = models.CharField(max_length=64, verbose_name='模型表字段名')
    title = models.CharField(max_length=64, verbose_name='字段显示名')

    class Meta:
        db_table = table_prefix + "system_menu_field"
        verbose_name = "菜单字段表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class FieldPermission(CoreModel):
    role = models.ForeignKey(
        to='Role', on_delete=models.CASCADE, verbose_name='角色', db_constraint=False)
    field = models.ForeignKey(to='MenuField', on_delete=models.CASCADE,
                              related_name='menu_field', verbose_name='字段', db_constraint=False)
    is_query = models.BooleanField(default=1, verbose_name='是否可查询')
    is_create = models.BooleanField(default=1, verbose_name='是否可创建')
    is_update = models.BooleanField(default=1, verbose_name='是否可更新')

    class Meta:
        db_table = table_prefix + "system_field_permission"
        verbose_name = "字段权限表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class MenuButton(CoreModel):
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menuPermission",
        on_delete=models.CASCADE,
        verbose_name="关联菜单",
        help_text="关联菜单",
    )
    name = models.CharField(max_length=64, verbose_name="名称", help_text="名称")
    value = models.CharField(unique=True, max_length=64,
                             verbose_name="权限值", help_text="权限值")
    api = models.CharField(
        max_length=200, verbose_name="接口地址", help_text="接口地址")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")

    class Meta:
        db_table = table_prefix + "system_menu_button"
        verbose_name = "菜单权限表"
        verbose_name_plural = verbose_name
        ordering = ("-name",)


class RoleMenuPermission(CoreModel):
    role = models.ForeignKey(
        to="Role",
        db_constraint=False,
        related_name="role_menu",
        on_delete=models.CASCADE,
        verbose_name="关联角色",
        help_text="关联角色",
    )
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="role_menu",
        on_delete=models.CASCADE,
        verbose_name="关联菜单",
        help_text="关联菜单",
    )

    class Meta:
        db_table = table_prefix + "role_menu_permission"
        verbose_name = "角色菜单权限表"
        verbose_name_plural = verbose_name
        # ordering = ("-create_datetime",)


class RoleMenuButtonPermission(CoreModel):
    role = models.ForeignKey(
        to="Role",
        db_constraint=False,
        related_name="role_menu_button",
        on_delete=models.CASCADE,
        verbose_name="关联角色",
        help_text="关联角色",
    )
    menu_button = models.ForeignKey(
        to="MenuButton",
        db_constraint=False,
        related_name="menu_button_permission",
        on_delete=models.CASCADE,
        verbose_name="关联菜单按钮",
        help_text="关联菜单按钮",
        null=True,
        blank=True
    )
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围",
                                     help_text="数据权限范围")
    dept = models.ManyToManyField(to="Dept", blank=True, verbose_name="数据权限-关联部门", db_constraint=False,
                                  help_text="数据权限-关联部门")

    class Meta:
        db_table = table_prefix + "role_menu_button_permission"
        verbose_name = "角色按钮权限表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Dictionary(CoreModel):
    TYPE_LIST = (
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "datetime"),
        (4, "time"),
        (5, "files"),
        (6, "boolean"),
        (7, "images"),
    )
    label = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name="字典名称", help_text="字典名称")
    value = models.CharField(max_length=200, blank=True,
                             null=True, verbose_name="字典编号", help_text="字典编号/实际值")
    parent = models.ForeignKey(
        to="self",
        related_name="sublist",
        db_constraint=False,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="父级",
        help_text="父级",
    )
    type = models.IntegerField(
        choices=TYPE_LIST, default=0, verbose_name="数据值类型", help_text="数据值类型")
    color = models.CharField(max_length=20, blank=True,
                             null=True, verbose_name="颜色", help_text="颜色")
    is_value = models.BooleanField(default=False, verbose_name="是否为value值",
                                   help_text="是否为value值,用来做具体值存放")
    status = models.BooleanField(
        default=True, verbose_name="状态", help_text="状态")
    sort = models.IntegerField(
        default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    remark = models.CharField(
        max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + "system_dictionary"
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_dictionary()  # 有更新则刷新字典配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_dictionary()
        return res


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True,
                                       help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True,
                                    help_text="请求地址")
    request_body = models.TextField(
        verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True,
                                      help_text="请求方式")
    request_msg = models.TextField(
        verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True,
                                  help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True,
                                       help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True,
                                     help_text="响应状态码")
    request_os = models.CharField(
        max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(
        verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(
        default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + "system_operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(max_length=200, null=True,
                            blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name, null=True, blank=True,)
    file_url = models.CharField(
        max_length=255, blank=True, verbose_name="文件地址", help_text="文件地址")
    engine = models.CharField(
        max_length=100, default='local', blank=True, verbose_name="引擎", help_text="引擎")
    mime_type = models.CharField(
        max_length=100, blank=True, verbose_name="Mime类型", help_text="Mime类型")
    size = models.CharField(max_length=36, blank=True,
                            verbose_name="文件大小", help_text="文件大小")
    md5sum = models.CharField(
        max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.url.size
        if not self.file_url:
            url = media_file_name(self, self.name)
            self.file_url = f'media/{url}'
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Area(CoreModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码",
                            help_text="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区层级(1省份 2城市 3区县 4乡级)",
                                   help_text="地区层级(1省份 2城市 3区县 4乡级)")
    pinyin = models.CharField(
        max_length=255, verbose_name="拼音", help_text="拼音")
    initials = models.CharField(
        max_length=20, verbose_name="首字母", help_text="首字母")
    enable = models.BooleanField(
        default=True, verbose_name="是否启用", help_text="是否启用")
    pcode = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父地区编码",
    )

    class Meta:
        db_table = table_prefix + "system_area"
        verbose_name = "地区表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return f"{self.name}"


class ApiWhiteList(CoreModel):
    url = models.CharField(
        max_length=200, help_text="url地址", verbose_name="url")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")
    enable_datasource = models.BooleanField(default=True, verbose_name="激活数据权限", help_text="激活数据权限",
                                            blank=True)

    class Meta:
        db_table = table_prefix + "api_white_list"
        verbose_name = "接口白名单"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class SystemConfig(CoreModel):
    parent = models.ForeignKey(
        to="self",
        verbose_name="父级",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父级",
    )
    title = models.CharField(max_length=50, verbose_name="标题", help_text="标题")
    key = models.CharField(max_length=20, verbose_name="键",
                           help_text="键", db_index=True)
    value = models.JSONField(
        max_length=100, verbose_name="值", help_text="值", null=True, blank=True)
    sort = models.IntegerField(
        default=0, verbose_name="排序", help_text="排序", blank=True)
    status = models.BooleanField(
        default=True, verbose_name="启用状态", help_text="启用状态")
    data_options = models.JSONField(
        verbose_name="数据options", help_text="数据options", null=True, blank=True)
    FORM_ITEM_TYPE_LIST = (
        (0, "text"),
        (1, "datetime"),
        (2, "date"),
        (3, "textarea"),
        (4, "select"),
        (5, "checkbox"),
        (6, "radio"),
        (7, "img"),
        (8, "file"),
        (9, "switch"),
        (10, "number"),
        (11, "array"),
        (12, "imgs"),
        (13, "foreignkey"),
        (14, "manytomany"),
        (15, "time"),
    )
    form_item_type = models.IntegerField(
        choices=FORM_ITEM_TYPE_LIST, verbose_name="表单类型", help_text="表单类型", default=0, blank=True
    )
    rule = models.JSONField(null=True, blank=True,
                            verbose_name="校验规则", help_text="校验规则")
    placeholder = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="提示信息", help_text="提示信息")
    setting = models.JSONField(
        null=True, blank=True, verbose_name="配置", help_text="配置")

    class Meta:
        db_table = table_prefix + "system_config"
        verbose_name = "系统配置表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)
        unique_together = (("key", "parent_id"),)

    def __str__(self):
        return f"{self.title}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_system_config()
        return res


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = ((1, "普通登录"), (2, "微信扫码登录"),)
    username = models.CharField(
        max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip",
                          null=True, blank=True, help_text="登录ip")
    agent = models.TextField(verbose_name="agent信息",
                             null=True, blank=True, help_text="agent信息")
    browser = models.CharField(
        max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=200, verbose_name="操作系统",
                          null=True, blank=True, help_text="操作系统")
    continent = models.CharField(
        max_length=50, verbose_name="州", null=True, blank=True, help_text="州")
    country = models.CharField(
        max_length=50, verbose_name="国家", null=True, blank=True, help_text="国家")
    province = models.CharField(
        max_length=50, verbose_name="省份", null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=50, verbose_name="城市",
                            null=True, blank=True, help_text="城市")
    district = models.CharField(
        max_length=50, verbose_name="县区", null=True, blank=True, help_text="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商",
                           null=True, blank=True, help_text="运营商")
    area_code = models.CharField(
        max_length=50, verbose_name="区域代码", null=True, blank=True, help_text="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="英文全称", null=True, blank=True,
                                       help_text="英文全称")
    country_code = models.CharField(
        max_length=50, verbose_name="简称", null=True, blank=True, help_text="简称")
    longitude = models.CharField(
        max_length=50, verbose_name="经度", null=True, blank=True, help_text="经度")
    latitude = models.CharField(
        max_length=50, verbose_name="纬度", null=True, blank=True, help_text="纬度")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型",
                                     help_text="登录类型")

    class Meta:
        db_table = table_prefix + "system_login_log"
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenter(CoreModel):
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    content = models.TextField(verbose_name="内容", help_text="内容")
    target_type = models.IntegerField(
        default=0, verbose_name="目标类型", help_text="目标类型")
    target_user = models.ManyToManyField(to=Users, related_name='user', through='MessageCenterTargetUser',
                                         through_fields=('messagecenter', 'users'), blank=True, verbose_name="目标用户",
                                         help_text="目标用户")
    target_dept = models.ManyToManyField(to=Dept, blank=True, db_constraint=False,
                                         verbose_name="目标部门", help_text="目标部门")
    target_role = models.ManyToManyField(to=Role, blank=True, db_constraint=False,
                                         verbose_name="目标角色", help_text="目标角色")

    class Meta:
        db_table = table_prefix + "message_center"
        verbose_name = "消息中心"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(Users, related_name="target_user", on_delete=models.CASCADE, db_constraint=False,
                              verbose_name="关联用户表", help_text="关联用户表")
    messagecenter = models.ForeignKey(MessageCenter, on_delete=models.CASCADE, db_constraint=False,
                                      verbose_name="关联消息中心表", help_text="关联消息中心表")
    is_read = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="是否已读", help_text="是否已读")

    class Meta:
        db_table = table_prefix + "message_center_target_user"
        verbose_name = "消息中心目标用户表"
        verbose_name_plural = verbose_name

# 水泥基因库


class AdmixtureGene(models.Model):
    # Field name made lowercase.
    admixture_id = models.CharField(
        db_column='admixture_ID', primary_key=True, max_length=100, db_comment='掺合料表索引项(-)')
    # Field name made lowercase.
    fa = models.ForeignKey('FaGene', models.DO_NOTHING, db_column='FA_ID',
                           blank=True, null=True, db_comment='粉煤灰表索引项(-)')
    # Field name made lowercase.
    slag = models.ForeignKey('SlagGene', models.DO_NOTHING,
                             db_column='slag_ID', blank=True, null=True, db_comment='矿渣表索引项(-)')
    # Field name made lowercase.
    slag_fine = models.ForeignKey('SlagFineGene', models.DO_NOTHING,
                                  db_column='slag_fine_ID', blank=True, null=True, db_comment='超细矿渣表索引项(-)')
    # Field name made lowercase.
    silica_fume = models.ForeignKey('SilicaFumeGene', models.DO_NOTHING,
                                    db_column='silica_fume_ID', blank=True, null=True, db_comment='硅灰表索引项(-)')
    # Field name made lowercase.
    lsp = models.ForeignKey('LspGene', models.DO_NOTHING, db_column='LSP_ID',
                            blank=True, null=True, db_comment='石灰石表索引项(-)')

    class Meta:
        managed = False  # 表示 Django 不会自动创建和管理与这个模型关联的数据库表
        db_table = 'admixture_gene'  # 表示这个模型对应的数据库表名


class AeaGene(models.Model):
    # Field name made lowercase.
    aea_id = models.CharField(
        db_column='AEA_ID', primary_key=True, max_length=100, db_comment='引气剂表索引编号(-)')
    # Field name made lowercase.
    aea_content_1 = models.FloatField(
        db_column='AEA_content_1', blank=True, null=True, db_comment='引气剂用量(kg/m3)')
    # Field name made lowercase.
    aea_content_2 = models.FloatField(
        db_column='AEA_content_2', blank=True, null=True, db_comment='引气剂用量(%)')
    # Field name made lowercase.
    aea_gas_ratio = models.FloatField(
        db_column='AEA_gas_ratio', blank=True, null=True, db_comment='引气剂含气量(%)')

    class Meta:
        managed = False
        db_table = 'aea_gene'


class AgregateCoarseGene(models.Model):
    # Field name made lowercase.
    agregate_coarse_id = models.CharField(
        db_column='agregate_coarse_ID', primary_key=True, max_length=100, db_comment='粗骨料表索引项(-)')
    type = models.CharField(max_length=100, blank=True,
                            null=True, db_comment='粗骨料类别(-)')
    range_5_10 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围5mm~10mm内的粗骨料含量(kg/m3)')
    # Field renamed to remove unsuitable characters.
    range_5_12_5 = models.FloatField(
        db_column='range_5_12.5', blank=True, null=True, db_comment='粒径范围5mm~12.5mm内的粗骨料含量(kg/m3)')
    range_5_16 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围5mm~16mm内的粗骨料含量(kg/m3)')
    range_5_20 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围5mm~20mm内的粗骨料含量(kg/m3)')
    range_5_30 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围5mm~30mm内的粗骨料含量(kg/m3)')
    range_10_20 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围10mm~20mm内的粗骨料含量(kg/m3)')
    range_20_30 = models.FloatField(
        blank=True, null=True, db_comment='粒径范围20mm~30mm内的粗骨料含量(kg/m3)')
    ratio = models.FloatField(blank=True, null=True, db_comment='占比(%)')
    bulk_density = models.FloatField(
        blank=True, null=True, db_comment='堆积密度(kg/m³)')
    apparent_density = models.FloatField(
        blank=True, null=True, db_comment='表观密度(kg/m³)')
    mud_ratio = models.FloatField(blank=True, null=True, db_comment='含泥量(%)')
    agregate_coarse_content = models.FloatField(
        blank=True, null=True, db_comment='粗骨料用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'agregate_coarse_gene'


class AgregateFineGene(models.Model):
    # Field name made lowercase.
    agregate_fine_id = models.CharField(
        db_column='agregate_fine_ID', primary_key=True, max_length=100, db_comment='细骨料表索引项(-)')
    type_natural = models.CharField(
        max_length=100, blank=True, null=True, db_comment='天然砂类别(-)')
    # Field name made lowercase.
    mx_natural = models.FloatField(
        db_column='Mx_natural', blank=True, null=True, db_comment='天然砂细度模数(-)')
    bulk_density_natural = models.FloatField(
        blank=True, null=True, db_comment='天然砂堆积密度(kg/m³)')
    apparent_density_natural = models.FloatField(
        blank=True, null=True, db_comment='天然砂表观密度(kg/m³)')
    mud_ratio_natural = models.FloatField(
        blank=True, null=True, db_comment='天然砂含泥量(%)')
    agregate_fine_content_natural = models.FloatField(
        blank=True, null=True, db_comment='天然砂用量(kg/m3)')
    type_artificial = models.CharField(
        max_length=100, blank=True, null=True, db_comment='人工砂类别(-)')
    # Field name made lowercase.
    mx_artificial = models.FloatField(
        db_column='Mx_artificial', blank=True, null=True, db_comment='人工砂细度模数(-)')
    bulk_density_artificial = models.FloatField(
        blank=True, null=True, db_comment='人工砂堆积密度(kg/m³)')
    apparent_density_artificial = models.FloatField(
        blank=True, null=True, db_comment='人工砂表观密度(kg/m³)')
    limestone_powder_content_artificial = models.FloatField(
        blank=True, null=True, db_comment='人工砂石粉含量(-)')
    agregate_fine_content_artificial = models.FloatField(
        blank=True, null=True, db_comment='人工砂用量(kg/m3)')
    sand_rate = models.FloatField(blank=True, null=True, db_comment='砂率(%)')

    class Meta:
        managed = False
        db_table = 'agregate_fine_gene'


class CarbonizationGene(models.Model):
    # Field name made lowercase.
    carbonization_id = models.CharField(
        db_column='carbonization_ID', primary_key=True, max_length=100, db_comment='碳化表征表索引项(-)')
    carbon_start_time = models.FloatField(
        blank=True, null=True, db_comment='碳化开始时间(-)')
    carbon_duration_time = models.FloatField(
        blank=True, null=True, db_comment='碳化持续时间(-)')
    carbon_depth = models.FloatField(blank=True, null=True, db_comment='碳化深度')
    compressive_strength_28days = models.FloatField(
        blank=True, null=True, db_comment='28天抗压强度(MPa)')

    class Meta:
        managed = False
        db_table = 'carbonization_gene'


class CementGene(models.Model):
    # Field name made lowercase.
    cement_id = models.CharField(
        db_column='cement_ID', primary_key=True, max_length=100, db_comment='水泥表索引编号(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey('OxidePercentage', models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    # Field name made lowercase.
    loss = models.FloatField(db_column='Loss', blank=True, null=True)
    cement_content = models.FloatField(
        blank=True, null=True, db_comment='水泥用量(kg/m3)')
    cement_strength = models.CharField(
        max_length=100, blank=True, null=True, db_comment='水泥强度(-)')

    class Meta:
        managed = False
        db_table = 'cement_gene'


class ConcreteAllGene(models.Model):
    # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True,
                          max_length=100, db_comment='数据索引编号(-)')
    concrete_strength = models.CharField(
        max_length=100, blank=True, null=True, db_comment='混凝土强度(-)')
    # Field name made lowercase.
    cement = models.ForeignKey(CementGene, models.DO_NOTHING,
                               db_column='cement_ID', blank=True, null=True, db_comment='水泥表索引编号(-)')
    water_content = models.FloatField(
        blank=True, null=True, db_comment='水用量(kg/m3)')
    water_ratio = models.FloatField(
        blank=True, null=True, db_comment='水胶比/水灰比(-)')
    # Field name made lowercase.
    water_res = models.ForeignKey('WaterResGene', models.DO_NOTHING,
                                  db_column='water_res_ID', blank=True, null=True, db_comment='减水剂表索引编号(-)')
    # Field name made lowercase.
    ad_content = models.FloatField(
        db_column='AD_content', blank=True, null=True, db_comment='外加剂用量(%)')
    # Field name made lowercase.
    aea = models.ForeignKey(AeaGene, models.DO_NOTHING, db_column='AEA_ID',
                            blank=True, null=True, db_comment='引气剂表索引编号(-)')
    gas_ratio = models.FloatField(blank=True, null=True, db_comment='含气量(%)')
    # Field name made lowercase.
    agregate_coarse = models.ForeignKey(AgregateCoarseGene, models.DO_NOTHING,
                                        db_column='agregate_coarse_ID', blank=True, null=True, db_comment='粗骨料表索引项(-)')
    # Field name made lowercase.
    agregate_fine = models.ForeignKey(AgregateFineGene, models.DO_NOTHING,
                                      db_column='agregate_fine_ID', blank=True, null=True, db_comment='细骨料表索引项(-)')
    # Field name made lowercase.
    admixture = models.ForeignKey(AdmixtureGene, models.DO_NOTHING,
                                  db_column='admixture_ID', blank=True, null=True, db_comment='掺合料表索引项(-)')
    # Field name made lowercase.
    pore_characteristics = models.ForeignKey(
        'PoreGene', models.DO_NOTHING, db_column='pore_characteristics_ID', blank=True, null=True, db_comment='孔隙特征表索引项(-)')
    # Field name made lowercase.
    carbonization = models.ForeignKey(CarbonizationGene, models.DO_NOTHING,
                                      db_column='carbonization_ID', blank=True, null=True, db_comment='碳化表征表索引项(-)')
    # Field name made lowercase.
    frost_resistancer = models.ForeignKey('FrostResistanceWaterGene', models.DO_NOTHING,
                                          db_column='frost_resistancer_ID', blank=True, null=True, db_comment='抗冻性表索引项(-)')
    # Field name made lowercase.
    impermeability = models.ForeignKey('ImpermeabilityGene', models.DO_NOTHING,
                                       db_column='impermeability_ID', blank=True, null=True, db_comment='氯离子抗渗性能表索引项(-)')
    # Field name made lowercase.
    paper = models.ForeignKey('PaperSource', models.DO_NOTHING,
                              db_column='paper_ID', blank=True, null=True, db_comment='文献信息表索引编号(-)')

    class Meta:
        managed = False
        db_table = 'concrete_all_gene'


class FaGene(models.Model):
    # Field name made lowercase.
    fa_id = models.CharField(
        db_column='FA_ID', primary_key=True, max_length=100, db_comment='粉煤灰表索引项(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey('OxidePercentage', models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    # Field name made lowercase.
    fa_content_1 = models.FloatField(
        db_column='FA_content_1', blank=True, null=True, db_comment='粉煤灰一级用量(kg/m3)')
    # Field name made lowercase.
    fa_content_2 = models.FloatField(
        db_column='FA_content_2', blank=True, null=True, db_comment='粉煤灰二级用量(kg/m3)')
    # Field name made lowercase.
    fa_content = models.FloatField(
        db_column='FA_content', blank=True, null=True, db_comment='粉煤灰总用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'fa_gene'


class FrostResistanceWaterGene(models.Model):
    # Field name made lowercase.
    frost_resistance_id = models.CharField(
        db_column='frost_resistance_ID', primary_key=True, max_length=100, db_comment='抗冻性表索引项(-)')
    max_freeze_thaw_water = models.FloatField(
        blank=True, null=True, db_comment='抗水冻性最大冻融次数(-)')
    relative_elastic_modulus_rate = models.FloatField(
        blank=True, null=True, db_comment='相对弹性模量率(%)')
    average_mass_loss_rate = models.FloatField(
        blank=True, null=True, db_comment='平均质量损失率(%)')
    measure = models.CharField(
        max_length=100, blank=True, null=True, db_comment='试验方法(-)')
    porosity_freeze_thaw = models.FloatField(
        blank=True, null=True, db_comment='冻融后的孔隙率(%)')
    frost_resistance_level = models.CharField(
        max_length=100, blank=True, null=True, db_comment='抗冻等级(-)')
    durability_coefficient = models.FloatField(
        blank=True, null=True, db_comment='耐久系数(-)')
    salt_type = models.CharField(
        max_length=100, blank=True, null=True, db_comment='盐的种类(-)')
    salt_concentration = models.FloatField(
        blank=True, null=True, db_comment='盐的浓度(%)')
    max_freeze_thaw_salt = models.FloatField(
        blank=True, null=True, db_comment='抗盐冻性最大冻融次数(-)')
    loss_elastic_modulus_salt = models.FloatField(
        blank=True, null=True, db_comment='抗盐冻性弹性模量损失(%)')
    elastic_modulus_salt = models.FloatField(
        blank=True, null=True, db_comment='抗盐冻性弹性模量(Gpa)')
    erosion_per_area_salt = models.FloatField(
        blank=True, null=True, db_comment='抗盐冻性单位面积剥蚀量(%)')
    compressive_strength_3days = models.FloatField(
        blank=True, null=True, db_comment='3天抗压强度(MPa)')
    compressive_strength_7days = models.FloatField(
        blank=True, null=True, db_comment='7天抗压强度(MPa)')
    compressive_strength_28days = models.FloatField(
        blank=True, null=True, db_comment='28天抗压强度(MPa)')

    class Meta:
        managed = False
        db_table = 'frost_resistance_water_gene'


class ImpermeabilityGene(models.Model):
    # Field name made lowercase.
    impermeability_id = models.CharField(
        db_column='impermeability_ID', primary_key=True, max_length=100, db_comment='氯离子抗渗性能表索引项(-)')
    # Field name made lowercase.
    sf = models.FloatField(db_column='SF', blank=True,
                           null=True, db_comment='氯离子扩散系数(10-12)')
    # Field name made lowercase.
    k = models.FloatField(db_column='K', blank=True,
                          null=True, db_comment='氯离子渗透系数(-)')
    electric_flux = models.FloatField(
        blank=True, null=True, db_comment='电通量(C)')
    compressive_strength_28days = models.FloatField(
        blank=True, null=True, db_comment='28天抗压强度(MPa)')

    class Meta:
        managed = False
        db_table = 'impermeability_gene'


class LspGene(models.Model):
    # Field name made lowercase.
    lsp_id = models.CharField(
        db_column='LSP_ID', primary_key=True, max_length=100, db_comment='石灰石表索引项(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey('OxidePercentage', models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    # Field name made lowercase.
    ssa = models.FloatField(db_column='SSa', blank=True,
                            null=True, db_comment='比表面积(m2/g)')
    # Field name made lowercase.
    lsp_content = models.FloatField(
        db_column='LSP_content', blank=True, null=True, db_comment='石灰石粉用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'lsp_gene'


class OxidePercentage(models.Model):
    # Field name made lowercase.
    oxide_id = models.CharField(
        db_column='oxide_ID', primary_key=True, max_length=100, db_comment='氧化物百分比表索引项(-)')
    # Field name made lowercase.
    cao = models.FloatField(db_column='CaO', blank=True,
                            null=True, db_comment='氧化钙占比(%)')
    # Field name made lowercase.
    sio2 = models.FloatField(db_column='SiO2', blank=True,
                             null=True, db_comment='二氧化硅占比(%)')
    # Field name made lowercase.
    al2o3 = models.FloatField(
        db_column='Al2O3', blank=True, null=True, db_comment='氧化铝占比(%)')
    # Field name made lowercase.
    fe2o3 = models.FloatField(
        db_column='Fe2O3', blank=True, null=True, db_comment='氧化铁占比(%)')
    # Field name made lowercase.
    mgo = models.FloatField(db_column='MgO', blank=True,
                            null=True, db_comment='氧化镁占比(%)')
    # Field name made lowercase.
    so3 = models.FloatField(db_column='SO3', blank=True,
                            null=True, db_comment='三氧化硫占比(%)')
    type = models.CharField(max_length=100, blank=True,
                            null=True, db_comment='当前氧化物归属材料(-)')
    content = models.FloatField(
        blank=True, null=True, db_comment='氧化物含量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'oxide_percentage'


class PaperSource(models.Model):
    # Field name made lowercase.
    paper_id = models.CharField(
        db_column='paper_ID', primary_key=True, max_length=100, db_comment='文献信息表索引项(-)')
    paper_author = models.CharField(
        max_length=100, blank=True, null=True, db_comment='文献作者(-)')
    # Field name made lowercase.
    paper_doi = models.CharField(
        db_column='paper_DOI', max_length=100, blank=True, null=True, db_comment='文献DOI(-)')
    paper_name = models.CharField(
        max_length=100, blank=True, null=True, db_comment='文献名称(-)')

    class Meta:
        managed = False
        db_table = 'paper_source'


class PoreGene(models.Model):
    # Field name made lowercase.
    pore_characteristics_id = models.CharField(
        db_column='pore_characteristics_ID', primary_key=True, max_length=100, db_comment='孔隙特征表索引项(-)')
    porosity = models.FloatField(blank=True, null=True, db_comment='孔隙率(%)')
    # Field name made lowercase.
    ave_pore_d = models.FloatField(
        db_column='ave_pore_D', blank=True, null=True, db_comment='平均孔径(nm)')
    less_10 = models.FloatField(
        blank=True, null=True, db_comment='孔径小于10nm的气孔占比(%)')
    range_10_100 = models.FloatField(
        blank=True, null=True, db_comment='孔径处于10nm和100nm之间的气孔占比(%)')
    more_100 = models.FloatField(
        blank=True, null=True, db_comment='孔径大于100nm的气孔占比(%)')
    # Field name made lowercase.
    sfav = models.FloatField(db_column='SFAV', blank=True,
                             null=True, db_comment='气泡间距系数(um)')
    pore_num = models.FloatField(blank=True, null=True, db_comment='气孔数量(-)')

    class Meta:
        managed = False
        db_table = 'pore_gene'


class SilicaFumeGene(models.Model):
    # Field name made lowercase.
    silica_fume_id = models.CharField(
        db_column='silica_fume_ID', primary_key=True, max_length=100, db_comment='硅灰表索引项(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey(OxidePercentage, models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    # Field name made lowercase.
    ssa = models.FloatField(db_column='SSa', blank=True,
                            null=True, db_comment='比表面积(m2/g)')
    silica_fume_content = models.FloatField(
        blank=True, null=True, db_comment='硅灰用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'silica_fume_gene'


class SlagFineGene(models.Model):
    # Field name made lowercase.
    slag_fine_id = models.CharField(
        db_column='slag_fine_ID', primary_key=True, max_length=100, db_comment='超细矿渣表索引项(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey(OxidePercentage, models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    slag_fine_content = models.FloatField(
        blank=True, null=True, db_comment='超细矿渣用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'slag_fine_gene'


class SlagGene(models.Model):
    # Field name made lowercase.
    slag_id = models.CharField(
        db_column='slag_ID', primary_key=True, max_length=100, db_comment='矿渣表索引项(-)')
    # Field name made lowercase.
    oxide = models.ForeignKey(OxidePercentage, models.DO_NOTHING,
                              db_column='oxide_ID', blank=True, null=True, db_comment='氧化物百分比表索引项(-)')
    slag_content = models.FloatField(
        blank=True, null=True, db_comment='矿渣粉用量(kg/m3)')

    class Meta:
        managed = False
        db_table = 'slag_gene'


class WaterResGene(models.Model):
    # Field name made lowercase.
    water_res_id = models.CharField(
        db_column='water_res_ID', primary_key=True, max_length=100, db_comment='减水剂表索引编号(-)')
    water_res_content_1 = models.FloatField(
        blank=True, null=True, db_comment='减水剂用量(kg/m3)')
    water_res_content_2 = models.FloatField(
        blank=True, null=True, db_comment='减水剂用量(%)')
    water_res_ratio = models.FloatField(
        blank=True, null=True, db_comment='减水率(%)')

    class Meta:
        managed = False
        db_table = 'water_res_gene'

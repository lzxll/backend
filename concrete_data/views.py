from django.db.models import Q
import json
from .models import CementGene, ConcreteAllGene
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from .models import ConcreteAllGene
# from .serializers import ConcreteAllGeneModelSerializer, ConcreteAllGeneModelCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from .models import ConcreteAllGene
from dvadmin.utils.serializers import CustomModelSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ConcreteAllGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = ConcreteAllGene
        fields = "__all__"


class ConcreteAllGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = ConcreteAllGene
        fields = '__all__'


class ConcreteAllGeneModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ConcreteAllGene.objects.all()
    serializer_class = ConcreteAllGeneModelSerializer
    create_serializer_class = ConcreteAllGeneModelCreateUpdateSerializer
    update_serializer_class = ConcreteAllGeneModelCreateUpdateSerializer
    filter_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']

# gene/


def get_gene(request):
    try:
        obj_concreteAllGene = ConcreteAllGene.objects.all().values()
        concreteAllGene = list(obj_concreteAllGene)
        return JsonResponse({'code': 1, 'data': concreteAllGene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取混凝土基因信息出现异常，具体错误："+str(e)})

# gene/query/  只查询了ID字段（如果需要的话再查询其他的字段吧）


def query_gene(request):
    # 接受前端传递的查询关键字----axios默认是json的格式---decode解码变成一个字典
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_concreteAllGene = ConcreteAllGene.objects.filter(
            Q(id=data['inputstr'])).values()
        concreteAllGene = list(obj_concreteAllGene)
        return JsonResponse({'code': 1, 'data': concreteAllGene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询混凝土基因信息出现异常，具体错误：" + str(e)})

# gene_ID/check/    传入 concrete_ID 属性


def is_exsist_gene_ID(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_concreteAllGene = ConcreteAllGene.objects.filter(
            Q(id=data['concrete_ID']))
        if obj_concreteAllGene.count() == 0:
            return JsonResponse({'code': 1, 'exsist': False})
        else:
            return JsonResponse({'code': 1, 'exsist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询编号是否存在信息出现异常，具体错误：" + str(e)})

# gene/add/


def add_gene(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_concreteAllGene_new = ConcreteAllGene(
            id=data['concrete_ID'],
            concrete_strength=data['concrete_strength'],
            water_content=data['water_content'],
            water_ratio=data['water_ratio'],


            # 这里的cement以及下面的是一个外键，需要传入一个对象
            cement=data['cement'],
            water_res=data['water_res'],

        )
        obj_concreteAllGene_new.save()
        obj_concreteAllGene = ConcreteAllGene.objects.all().values()
        concreteAllGene = list(obj_concreteAllGene)
        return JsonResponse({'code': 1, 'data': concreteAllGene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "添加混凝土基因信息到数据库出现异常，具体错误：" + str(e)})

#########################################################################
# cement/


def get_cement(request):
    try:
        obj_cementgene = CementGene.objects.select_related(
            'oxide').all().values('cement_id', 'oxide__cao', 'oxide__sio2', 'oxide__al2o3', 'oxide__fe2o3', 'oxide__mgo', 'oxide__so3', 'cement_content', 'cement_strength')
        cementgene = list(obj_cementgene)
        # print(cementgene)
        return JsonResponse({'code': 1, 'data': cementgene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取水泥基因信息出现异常，具体错误："+str(e)})

# cement/query/
# 这里只查询了两个字段，可以根据需要查询更多字段


def query_cement(request):
    # 接受前端传递的查询关键字----axios默认是json的格式---decode解码变成一个字典
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_cementgene = CementGene.objects.filter(
            Q(cement_ID=data['inputstr']) | Q(cement_strength=data['inputstr'])).values()
        cementgene = list(obj_cementgene)
        return JsonResponse({'code': 1, 'data': cementgene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询水泥基因信息出现异常，具体错误：" + str(e)})

# cement_ID/check/


def is_exsist_cement_ID(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_cementgene = CementGene.objects.filter(
            Q(cement_ID=data['cement_ID']))
        if obj_cementgene.count() == 0:
            return JsonResponse({'code': 1, 'exsist': False})
        else:
            return JsonResponse({'code': 1, 'exsist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询编号是否存在信息出现异常，具体错误：" + str(e)})

# cement/add/


def add_cement(request):
    data = json.loads(request.body.decode('utf-8'))
    for key, value in data.items():
        if isinstance(value, str) and value.strip() == '':
            data[key] = None
    try:
        obj_cementgene_new = CementGene(
            cement_ID=data['cement_ID'],
            CaO=data['CaO'],
            SiO2=data['SiO2'],
            Al2O3=data['Al2O3'],
            Fe2O3=data['Fe2O3'],
            MgO=data['MgO'],
            SO3=data['SO3'],
            cement_content=data['cement_content'],
            cement_strength=data['cement_strength']
        )
        obj_cementgene_new.save()
        obj_cementgene = CementGene.objects.all().values()
        cementgene = list(obj_cementgene)
        return JsonResponse({'code': 1, 'data': cementgene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "添加水泥基因信息到数据库出现异常，具体错误：" + str(e)})

# cement/update/
# 找到对应id的数据，然后进行修改


def update_cement(request):
    data = json.loads(request.body.decode('utf-8'))
    for key, value in data.items():
        if isinstance(value, str) and value.strip() == '':
            data[key] = None
    # print(data)
    try:
        obj_cementgene_update = CementGene.objects.get(
            cement_ID=data['cement_ID'])
        obj_cementgene_update .CaO = data['CaO']
        obj_cementgene_update .SiO2 = data['SiO2']
        obj_cementgene_update .Al2O3 = data['Al2O3']
        obj_cementgene_update .Fe2O3 = data['Fe2O3']
        obj_cementgene_update .MgO = data['MgO']
        obj_cementgene_update .SO3 = data['SO3']
        obj_cementgene_update .cement_content = data['cement_content']
        obj_cementgene_update .cement_strength = data['cement_strength']
        obj_cementgene_update .save()

        obj_cementgene = CementGene.objects.all().values()
        cementgene = list(obj_cementgene)
        return JsonResponse({'code': 1, 'data': cementgene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "修改水泥基因信息到数据库出现异常，具体错误：" + str(e)})

# cement/delete/single/


def delete_single_cement(request):
    data = json.loads(request.body.decode('utf-8'))
    # for key, value in data.items():
    #     if isinstance(value, str) and value.strip() == '':
    #         data[key] = None
    # print(data)
    try:
        obj_cementgene_delete = CementGene.objects.get(
            cement_ID=data['cement_ID'])
        obj_cementgene_delete.delete()

        obj_cementgene = CementGene.objects.all().values()
        cementgene = list(obj_cementgene)
        return JsonResponse({'code': 1, 'data': cementgene})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除水泥基因信息到数据库出现异常，具体错误：" + str(e)})


def delete_multiple_cement(request):
    pass

# def get_random_str():
#     #获取uuid的随机数
#     uuid_val = uuid.uuid4()
#     #获取uuid的随机数字符串
#     uuid_str = str(uuid_val).encode('utf-8')
#     #获取md5实例
#     md5 = hashlib.md5()
#     #拿取uuid的md5摘要
#     md5.update(uuid_str)
#     #返回固定长度的字符串
#     return md5.hexdigest()

# def read_excel_dict(path:str):
#     work_book=openpyxl.load_workbook(path)
#     sheet=work_book['cement']
#     cement=[]
#     keys=['cement_ID','CaO','SiO2','Al2O3','Fe2O3','MgO','SO3','cement_content','cement_strength']

#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         temp_dict={}
#         for index,value in enumerate(row):
#             temp_dict[keys[index]] = value
#         cement.append(temp_dict)

#     return cement

# def write_to_excel(data:list, path:str):
#     """把数据库写入到Excel"""
#     # 实例化一个workbook
#     workbook = openpyxl.Workbook()
#     # 激活一个sheet
#     sheet = workbook.active
#     # 为sheet命名
#     sheet.title = 'student'
#     # 准备keys
#     keys = data[0].keys()
#     # 准备写入数据
#     for index, item in enumerate(data):
#         # 遍历每一个元素
#         for k,v in enumerate(keys):
#             sheet.cell(row=index + 1, column=k+ 1, value=str(item[v]))
#     # 写入到文件
#     workbook.save(path)

# def import_cement_excel(request):
#     # 接受excel文件保存到media文件夹
#     rev_file = request.FILES.get('excel')

#     if not rev_file:
#         return JsonResponse({'code': 0, 'msg': "excel文件不存在" })

#     new_name = get_random_str()
#     file_path = os.path.join(settings.MEDIA_ROOT,new_name + os.path.splitext(rev_file.name)[1])
#     try:
#         f = open(file_path,'wb')
#         for i in rev_file.chunks():
#             f.write(i)
#         f.close()
#     except Exception as e:
#         return JsonResponse({'code': 0, 'msg': str(e)})

#     ex_cement=read_excel_dict(file_path)
#     print(ex_cement)
#     success = 0
#     error = 0
#     error_ids = []

#     for data in ex_cement:
#         try:

#             obj_cementgene = CementGene.objects.create(
#             cement_ID=data['cement_ID'],
#             CaO=data['CaO'],
#             SiO2=data['SiO2'],
#             Al2O3=data['Al2O3'],
#             Fe2O3=data['Fe2O3'],
#             MgO=data['MgO'],
#             SO3=data['SO3'],
#             cement_content=data['cement_content'],
#             cement_strength=data['cement_strength']
#             )
#             # 计数
#             success += 1
#             print(success)
#         except:
#             # 如果失败了
#             error += 1
#             error_ids.append(data['cement_ID'])

#     obj_cementgene = CementGene.objects.all().values()
#     cementgene = list(obj_cementgene)

#     return JsonResponse({'code': 1, 'success': success, 'error': error, 'errors': error_ids, 'data': cementgene})

# def export_cement_excel(request):
#     obj_cementgene = CementGene.objects.all().values()
#     cementgene = list(obj_cementgene)
#     excel_name = get_random_str() + ".xlsx"
#     # 准备写入的路劲
#     path = os.path.join(settings.MEDIA_ROOT, excel_name)
#     # 写入到Excel
#     write_to_excel(cementgene, path)
#     # 返回
#     return JsonResponse({'code': 1, 'name': excel_name})

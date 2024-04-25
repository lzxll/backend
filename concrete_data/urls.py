from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ConcreteAllGeneModelViewSet, CementGeneModelViewSet, WaterResGeneModelViewSet, AeaGeneModelViewSet, AgregateFineGeneModelViewSet, AgregateCoarseGeneModelViewSet, AdmixtureGeneModelViewSet, FaGeneModelViewSet, SlagFineGeneModelViewSet, SlagFineGeneModelViewSet, SilicaFumeGeneModelViewSet, LspGeneModelViewSet, OxidePercentageModelViewSet, PoreGeneModelViewSet, ImpermeabilityGeneModelViewSet, CarbonizationGeneModelViewSet, FrostResistanceWaterGeneModelViewSet, PaperSourceModelViewSet

from . import views
router = SimpleRouter()
router.register("api/concrete_data", ConcreteAllGeneModelViewSet)
router.register("api/cement_data", CementGeneModelViewSet)
router.register("api/water_res_data", WaterResGeneModelViewSet)
router.register("api/aea_data", AeaGeneModelViewSet)
# 新
router.register("api/agregatefine_data", AgregateFineGeneModelViewSet)
router.register("api/agregatecoarse_data", AgregateCoarseGeneModelViewSet)
router.register("api/admixture_data", AdmixtureGeneModelViewSet)
router.register("api/fa_data", FaGeneModelViewSet)
router.register("api/slagfine_data", SlagFineGeneModelViewSet)
router.register("api/slagcoarse_data", SlagFineGeneModelViewSet)
router.register("api/silicafume_data", SilicaFumeGeneModelViewSet)
router.register("api/lsp_data", LspGeneModelViewSet)
router.register("api/oxidepercentage_data", OxidePercentageModelViewSet)
router.register("api/pore_data", PoreGeneModelViewSet)
router.register("api/impermeability_data", ImpermeabilityGeneModelViewSet)
router.register("api/carbonization_data", CarbonizationGeneModelViewSet)
router.register("api/frostresistancewater_data",
                FrostResistanceWaterGeneModelViewSet)
router.register("api/papersource_data", PaperSourceModelViewSet)


urlpatterns = [
    # 全息基因数据库表
    # path('gene/', views.get_gene),  # 获取所有
    # path('gene/query/', views.query_gene),  # 查询
    # path('gene_ID/check/', views.is_exsist_gene_ID),  # 校验编号是否存在
    # path('gene/add/', views.add_gene),  # 添加
    # path('gene/update/', views.update_gene),  # 修改
    # path('gene/delete/single/', views.delete_single_gene),  # 删除单个
    # path('gene/delete/multiple/', views.delete_multiple_gene),  # 删除多个
    # path('excel/import/', views.import_gene_excel),
    # path('excel/export/', views.export_gene_excel),

    # 剩下十七章表



    # path('api/concrete_data', views.get_cement),  # 获取所有
    # path('cement/query/', views.query_cement),  # 查询
    # path('cement_ID/check/', views.is_exsist_cement_ID),  # 校验编号是否存在
    # path('cement/add/', views.add_cement),  # 添加
    # path('cement/update/', views.update_cement),  # 修改
    # path('cement/delete/single/', views.delete_single_cement),  # 删除单个
    # path('cement/delete/multiple/', views.delete_multiple_cement),  # 删除多个
    # # path('excel/import/', views.import_cement_excel),
    # # path('excel/export/', views.export_cement_excel),
]
urlpatterns += router.urls

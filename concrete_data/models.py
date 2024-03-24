from django.db import models

# Create your models here.


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

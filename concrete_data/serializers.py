from .models import ConcreteAllGene, CementGene, WaterResGene, AeaGene, AgregateCoarseGene, AgregateFineGene, AdmixtureGene, FaGene, SlagGene, SlagFineGene, SilicaFumeGene, LspGene, OxidePercentage, PoreGene, ImpermeabilityGene, CarbonizationGene, FrostResistanceWaterGene, PaperSource
from dvadmin.utils.serializers import CustomModelSerializer
# 文献信息表


class PaperSourceModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = PaperSource
        fields = "__all__"


class PaperSourceModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = PaperSource
        fields = '__all__'
# 抗冻性基因表


class FrostResistanceWaterGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = FrostResistanceWaterGene
        fields = "__all__"


class FrostResistanceWaterGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = FrostResistanceWaterGene
        fields = '__all__'
# 碳化深度基因表


class CarbonizationGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = CarbonizationGene
        fields = "__all__"


class CarbonizationGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = CarbonizationGene
        fields = '__all__'
# 氯离子渗透性基因表


class ImpermeabilityGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = ImpermeabilityGene
        fields = "__all__"


class ImpermeabilityGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = ImpermeabilityGene
        fields = '__all__'
# 孔隙率基因表


class PoreGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = PoreGene
        fields = "__all__"


class PoreGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = PoreGene
        fields = '__all__'

# 氧化物百分比表(硅灰表SilicaFumeGene，超细矿渣表SlagFineGene，矿渣表SlagGene，粉煤灰表FaGene，水泥表CementGene，石灰石表LspGene)


class OxidePercentageModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = OxidePercentage
        fields = "__all__"


class OxidePercentageModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = OxidePercentage
        fields = '__all__'


# 石灰石基因表
class LspGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = LspGene
        fields = "__all__"


class LspGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = LspGene
        fields = '__all__'

# 硅灰基因表


class SilicaFumeGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = SilicaFumeGene
        fields = "__all__"


class SilicaFumeGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = SilicaFumeGene
        fields = '__all__'

# 超细矿渣基因表


class SlagFineGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = SlagFineGene
        fields = "__all__"


class SlagFineGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = SlagFineGene
        fields = '__all__'

# 矿渣基因表


class SlagGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = SlagGene
        fields = "__all__"


class SlagGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = SlagGene
        fields = '__all__'

# 粉煤灰基因表


class FaGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = FaGene
        fields = "__all__"


class FaGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = FaGene
        fields = '__all__'

# 掺合料基因表（粉煤灰，矿渣，超细矿渣，硅灰，石灰石）


class AdmixtureGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = AdmixtureGene
        fields = "__all__"


class AdmixtureGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = AdmixtureGene
        fields = '__all__'


# 粗骨料基因表

class AgregateCoarseGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = AgregateCoarseGene
        fields = "__all__"


class AgregateCoarseGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = AgregateCoarseGene
        fields = '__all__'

# 细骨料基因表


class AgregateFineGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = AgregateFineGene
        fields = "__all__"


class AgregateFineGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = AgregateFineGene
        fields = '__all__'


# 全息基因表


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

# 水泥表


class CementGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = CementGene
        fields = "__all__"


class CementGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = CementGene
        fields = '__all__'

# 减水剂


class WaterResGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = WaterResGene
        fields = "__all__"


class WaterResGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = WaterResGene
        fields = '__all__'

# AeaGene引气剂


class AeaGeneModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = AeaGene
        fields = "__all__"


class AeaGeneModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = AeaGene
        fields = '__all__'

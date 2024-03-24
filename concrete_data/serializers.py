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

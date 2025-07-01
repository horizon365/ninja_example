from typing import Optional, List
from ninja import Schema, ModelSchema, FilterSchema
from gene.models import Gene
from pydantic import Field, validator
from .input import GeneFilterSchema, FileTypeEnum, OptionsTypeEnum
from .output import GeneAggregateSchema, CoExpressionSchema

class GeneSchema(ModelSchema):
    class Meta:
        model = Gene
        fields = '__all__'

class GeneListSchema(ModelSchema):
    coordinates: str
    class Meta:
        model = Gene
        exclude = ('start', 'end')
    @staticmethod
    def resolve_coordinates(obj):
        return f'{obj.start} - {obj.end}'

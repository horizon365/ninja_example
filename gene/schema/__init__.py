from typing import Optional, List
from ninja import Schema, ModelSchema, FilterSchema
from gene.models import Gene
from pydantic import Field, validator
from .input import GeneFilterSchema, FileTypeEnum
from .output import GeneAggregateSchema, CoExpressionSchema

class GeneSchema(ModelSchema):
    class Meta:
        model = Gene
        fields = '__all__'

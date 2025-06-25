from typing import List, Dict
from ninja import Schema, ModelSchema, FilterSchema
from gene.models import Gene, CoExpression


# 定义单个对象的 Schema
class ItemSchema(Schema):
    name: str
    count: int

class GeneAggregateSchema(Schema):
    gene_id: List[ItemSchema]
    chrom: List[str]
    start: Dict[str, int]
    end: Dict[str, int]

class CoExpressionSchema(ModelSchema):
    class Meta:
        model = CoExpression
        fields = '__all__'


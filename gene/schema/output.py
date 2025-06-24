from typing import List
from ninja import Schema, ModelSchema, FilterSchema
from gene.models import Gene, CoExpression


class GeneAggregateSchema(Schema):
    gene_id: List[str]
    chrom: List[str]
    start: int
    end: int

class CoExpressionSchema(ModelSchema):
    class Meta:
        model = CoExpression
        fields = '__all__'


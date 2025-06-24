from typing import List
from ninja import Schema, ModelSchema

from genefamily.models import GeneFamily


class GeneFamilySchema(ModelSchema):
    gene_list: List[str]
    class Meta:
        model = GeneFamily
        fields = '__all__'

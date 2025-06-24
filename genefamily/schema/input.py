from typing import Optional
from ninja import Schema, FilterSchema, Field

from genefamily.models import GeneFamily


class GeneFamilyFilterSchema(FilterSchema):
    query: Optional[str] = Field(None, q=GeneFamily.get_query_field())

    class Meta:
        model = GeneFamily
        fields = '__all__'

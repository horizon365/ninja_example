from enum import Enum

from typing import Optional, List
from ninja import Schema, ModelSchema, FilterSchema
from gene.models import Gene
from pydantic import Field, validator


class GeneFilterSchema(FilterSchema):
    # 多字段联合模糊搜索
    query: Optional[str] = Field(None, q=Gene.get_query_field())
    # 以下为单字段列表内搜索
    gene_id: Optional[str] = Field(None, q='gene_id__in')
    chrom: Optional[str] = Field(None, q='chrom')
    start: Optional[int] = Field(None, gt=0, q='start')
    end: Optional[int] = Field(None, q='end')

    @validator('gene_id')
    @classmethod
    def validator_field(cls, value_data: str):
        """将传参 'lung,heart' 转化为 ['lung', 'heart']"""
        if isinstance(value_data, str):
            if ',' in value_data:
                return [item.strip() for item in value_data.split(',') if item.strip()]
            return [value_data]
        return value_data


class FileTypeEnum(str, Enum):
    GENE_EXPRESSION = "gene_expression"
    CO_EXPRESSION = "co-expression"

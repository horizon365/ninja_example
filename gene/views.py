from typing import List
from ninja import Router, Query, Path
from ninja.pagination import paginate
from gene.models import Gene, CoExpression
from genefamily.models import GeneFamily

from gene.schema import GeneSchema, GeneFilterSchema, GeneAggregateSchema, CoExpressionSchema, FileTypeEnum

from ninja_example.api import PGPagination
# Create your views here.

router = Router()

@router.get('/list_gene/', tags=['v0.1'], response=List[GeneSchema])
@paginate(PGPagination)
def list_gene(request, filters: GeneFilterSchema = Query(...)):
    queryset = Gene.objects.all()
    queryset = filters.filter(queryset).distinct()
    return queryset

@router.get('/get_aggregations/', tags=['v0.1'], response=GeneAggregateSchema)
def get_aggregations(request, filters: GeneFilterSchema = Query(...)):
    queryset = Gene.objects.all()
    queryset = filters.filter(queryset).distinct()
    return Gene.get_aggregations(queryset)


@router.get('/get_gene/{gene_id}', tags=['v0.1'], response=GeneSchema)
def get_gene(request, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    queryset = Gene.objects.filter(gene_id=gene_id)
    return queryset

@router.get('/get_coexpression/{gene_id}', tags=['v0.1'], response=List[CoExpressionSchema])
@paginate(PGPagination)
def get_coexpression(request, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    queryset  =CoExpression.objects.filter(gene_id=gene_id)
    return queryset

@router.get('/get_file/{gene_id}', tags=['v0.1'], response=List[str])
def get_file(request, type: FileTypeEnum, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    pass

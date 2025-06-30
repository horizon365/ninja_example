import pdb
from typing import List
from django.db.models import Max, Min
from ninja import Router, Query, Path
from ninja.pagination import paginate
from gene.models import Gene, CoExpression
from genefamily.models import GeneFamily

from gene.schema import GeneSchema,GeneListSchema,  GeneFilterSchema, GeneAggregateSchema, CoExpressionSchema, FileTypeEnum

from ninja_example.api import PGPagination
# Create your views here.

router = Router()

@router.get('/list_gene/', tags=['v0.1'], response=List[GeneListSchema])
@paginate(PGPagination)
def list_gene(request, filters: GeneFilterSchema = Query(...)):
    queryset = Gene.objects.all()
    queryset = filters.filter(queryset).distinct()
    return queryset

@router.get('/get_aggregations/', tags=['v0.1'], response=GeneAggregateSchema)
def get_aggregations(request, filters: GeneFilterSchema = Query(...)):
    queryset = Gene.objects.all()
    queryset = filters.filter(queryset).distinct()
    data =dict(
        gene_id=Gene.get_aggregations(queryset)['gene_id'],
        chrom=list(queryset.values_list('chrom', flat=True)),
        start=queryset.aggregate(min=Min('start'),max=Max('start')),
        end=queryset.aggregate(min=Min('end'),max=Max('end')),
    )
    return data

@router.get('/get_gene/{gene_id}', tags=['v0.1'], response=GeneSchema)
def get_gene(request, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    queryset = Gene.objects.filter(gene_id=gene_id)
    return queryset

@router.get('/get_coexpression/{gene_id}', tags=['v0.1'], response=List[CoExpressionSchema])
@paginate(PGPagination)
def get_coexpression(request, option: str, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    queryset  =CoExpression.objects.filter(gene1=gene_id)
    return queryset


@router.get('/get_options', tags=['v0.1'], response=List[str])
def get_file(request, type: FileTypeEnum):
    return ['a','b']

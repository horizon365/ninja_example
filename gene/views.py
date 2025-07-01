import pdb
from typing import List
from django.db.models import Max, Min
from django.http import HttpResponse
from ninja import Router, Query, Path
from ninja.pagination import paginate
from gene.models import Gene, CoExpression
from genefamily.models import GeneFamily

from gene.schema import GeneSchema,GeneListSchema,  GeneFilterSchema, GeneAggregateSchema, CoExpressionSchema, FileTypeEnum, OptionsTypeEnum

from ninja_example.api import PGPagination
# Create your views here.

router = Router()

@router.get('/list_gene/', tags=['v0.1'], response=List[GeneListSchema])
@paginate(PGPagination)
def list_gene(request, filters: GeneFilterSchema = Query(...)):
    """
    检索页右侧选项
    :param request:
    :param filters:
    :return:
    """
    queryset = Gene.objects.all()
    queryset = filters.filter(queryset).distinct()
    return queryset

@router.get('/get_aggregations/', tags=['v0.1'], response=GeneAggregateSchema)
def get_aggregations(request, filters: GeneFilterSchema = Query(...)):
    """
    检索页左侧选项
    :param request:
    :param filters:
    :return:
    """
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
    """
    gene 详情页字段信息
    :param request:
    :param gene_id:
    :return:
    """
    queryset = Gene.objects.filter(gene_id=gene_id)
    return queryset

@router.get('/get_coexpression/{gene_id}', tags=['v0.1'], response=List[CoExpressionSchema])
@paginate(PGPagination)
def get_coexpression(request, option: str, gene_id: str=Path(..., example='TraesCS4A02G24260')):
    """
    gene 详情页 CO expression表格信息
    :param request:
    :param option:
    :param gene_id:
    :return:
    """
    queryset  =CoExpression.objects.filter(gene1=gene_id)
    return queryset


@router.get('/get_options', tags=['v0.1'], response=List[str])
def get_options(request, type: OptionsTypeEnum):
    """
    gene 详情页所有的下拉选项接口
    :param request:
    :param type:
    :return:
    """
    return ['a','b']

@router.get('/get_txtfile', tags=['v0.1'])
def get_txtfile(request, type: FileTypeEnum):
    """
    gene 详情页下载 txt 文件接口
    :param request:
    :param type:
    :return:
    """
    text_content = "这是要下载的文本内容。\n第二行内容。\n第三行内容。"
    # 创建 HTTP 响应对象，并指定内容类型为文本文件
    response = HttpResponse(text_content, content_type='text/plain')
    # 设置 Content-Disposition 头以触发浏览器下载
    response['Content-Disposition'] = f'attachment; filename="{type.value}.txt"'
    return response


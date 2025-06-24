from gene.models import Gene
from typing import List
import tablib
from django.http import HttpResponse
from django.db import models

from genefamily.models import GeneFamily
from gene.models import Gene
from ninja import Router, Query
from ninja.pagination import paginate
from gene.schema import GeneSchema
from ninja_example.api import PGPagination
from .schema import GeneFamilySchema, GeneFamilyFilterSchema

router = Router()

@router.get('/list_genefamily', tags=['v0.1'], response=List[GeneFamilySchema])
@paginate(PGPagination)
def list_gene_family(request, filters: GeneFamilyFilterSchema = Query(None)):
    queryset = GeneFamily.objects.all()
    queryset = filters.filter(queryset).distinct()
    for q in queryset:
        q.gene_list = [x.gene_id for x in q.gene_set.all()]
    return queryset

@router.get('/get_genefamilly', tags=['v0.1'], response=List[GeneSchema])
@paginate(PGPagination)
def get_gene_family(request, name: str):
    model = GeneFamily.objects.get(name=name)
    return model.gene_set.all()


@router.get('/down_all_table', tags=['v0.1'])
def down_all_table(request, name: str):
    model = GeneFamily.objects.get(name=name)
    queryset = model.gene_set.all()
    dataset = tablib.Dataset()
    field_names = [field.name for field in Gene._meta.fields if not isinstance(field, models.ForeignKey)]
    dataset.headers = field_names

    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        dataset.append(row)

    # 导出为 CSV 格式
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Sample.csv"'
    response.write(dataset.export('csv'))
    return response

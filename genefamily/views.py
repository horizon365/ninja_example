from gene.models import Gene
from typing import List
from genefamily.models import GeneFamily
from gene.models import Gene
from ninja import Router
from ninja.pagination import paginate
from gene.schema import GeneSchema
from ninja_example.api import PGPagination
from .schema import GeneFamilySchema

router = Router()

@router.get('/list_genefamily', tags=['v0.1'], response=List[GeneFamilySchema])
@paginate(PGPagination)
def list_gene_family(request, query: str):
    pass

@router.get('/get_genefamilly', tags=['v0.1'], response=List[GeneSchema])
@paginate(PGPagination)
def get_gene_family(request, name: str):
    pass

@router.get('/down_all_table', tags=['v0.1'])
def down_all_table(request):
    pass

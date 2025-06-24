from django.db import models
from django.db.models import Count

from genefamily.models import GeneFamily


# Create your models here.
class Gene(models.Model):
    gene_id = models.CharField(max_length=120, unique=True, db_index=True, primary_key=True, verbose_name='基因ID')
    species = models.CharField(max_length=120, db_index=True, verbose_name='物种')
    chrom = models.CharField(max_length=120, db_index=True, verbose_name='染色体')
    start = models.BigIntegerField(verbose_name='起始位置')
    end = models.BigIntegerField(verbose_name='终止位置')
    gene_family = models.ForeignKey(GeneFamily, on_delete=models.CASCADE, verbose_name='基因家族名称')
    cds_sequence = models.TextField(verbose_name='CDS序列')
    protein_length = models.BigIntegerField(verbose_name='蛋白序列长度')
    protein_sequence = models.TextField(verbose_name='蛋白质序列')
    mature_protein_sequence = models.TextField(verbose_name='蛋白质成熟序列')
    function = models.TextField(verbose_name='功能注释结果')
    uniprot_kb = models.CharField(max_length=120, db_index=True, verbose_name='关联UniProtKB  ID')
    ensembl_url = models.CharField(max_length=1024, db_index=True, verbose_name='关联ensemble地址')
    gene_network_url = models.CharField(max_length=1024, db_index=True, verbose_name='关联基因网络地址')
    subcellular_localization = models.CharField(max_length=1024, db_index=True, verbose_name='关联亚细胞定位地址')

    @staticmethod
    def get_query_field():
        """获取供query查询的参数
        """
        query = ['gene_id']
        foreign_fields = []
        own_field = ['species', 'chrom', 'gene_family']

        for field in foreign_fields:
            query.append(field)
        for field in own_field:
            query.append(field + '__icontains')

        return query

    @staticmethod
    def get_aggregations(queryset) -> dict:
        fields = ['gene_id', 'chrom', 'start', 'end']
        result = {}
        for field in fields:
            grouped = queryset.values(field).annotate(count=Count('gene_id', distinct=True))
            result[field] = [{'name': item[field], 'count': item['count']}
                             for item in grouped if item['count'] is not None]
        return result

class CoExpression(models.Model):
    gene1 = models.ForeignKey(Gene, on_delete=models.CASCADE, verbose_name='Gene1')
    gene2 = models.CharField(max_length=120, db_index=True, verbose_name='Gene2')
    pcc = models.CharField(max_length=120, db_index=True, verbose_name='PCC')
    mr = models.CharField(max_length=120, db_index=True, verbose_name='MR')

from django.db import models

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

class CoExpression(models.Model):
    gene1 = models.ForeignKey(Gene, on_delete=models.CASCADE, verbose_name='Gene1')
    gene2 = models.CharField(max_length=120, db_index=True, verbose_name='Gene2')
    pcc = models.CharField(max_length=120, db_index=True, verbose_name='PCC')
    mr = models.CharField(max_length=120, db_index=True, verbose_name='MR')



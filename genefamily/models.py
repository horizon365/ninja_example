from django.db import models

# Create your models here.
class GeneFamily(models.Model):
    name = models.CharField(max_length=120, primary_key=True, db_index=True, verbose_name='基因家族名称')
    gene_number = models.BigIntegerField(verbose_name='基因数量')
    gene_list = models.JSONField(default=list, verbose_name='基因列表')

from django.db import models


# Create your models here.
class GeneFamily(models.Model):
    name = models.CharField(max_length=120, primary_key=True, db_index=True, verbose_name='基因家族名称')
    gene_number = models.BigIntegerField(verbose_name='基因数量')

    @staticmethod
    def get_query_field():
        """获取供query查询的参数
        """
        query = []
        foreign_fields = ['gene__gene_id']
        own_field = ['name']

        for field in foreign_fields:
            query.append(field)
        for field in own_field:
            query.append(field + '__icontains')

        return query

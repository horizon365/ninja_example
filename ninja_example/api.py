"""ninja 的api入口"""
import json
from typing import Any, Mapping, Type
from django.http import HttpRequest
from django.conf import settings
from ninja import Schema, Field, NinjaAPI
from ninja.renderers import BaseRenderer
from ninja.responses import NinjaJSONEncoder
from ninja.pagination import PaginationBase
from gene.models import Gene
from genefamily.models import GeneFamily

class CustomRenderer(BaseRenderer):
    """
    在原版的基础上给外层包裹'data'
    """
    media_type = 'application/json'
    encoder_class: Type[json.JSONEncoder] = NinjaJSONEncoder
    json_dumps_params: Mapping[str, Any] = {}

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        if response_status == 200:
            response_content = {'data': data}
        elif response_status in (400, 422, 404):
            # 确保data是字典格式
            if not isinstance(data, dict):
                data = {'detail': data}
            data['errorCode'] = response_status
            response_content = {'error': data}
        else:
            # 其他错误状态的处理或者默认错误处理
            response_content = {'error': {'detail': 'An error occurred', 'errorCode': response_status}}

            # 返回JSON响应
        return json.dumps(response_content, cls=self.encoder_class, **self.json_dumps_params)


class PGPagination(PaginationBase):
    """
    自定义符合组内规范的适用于PG的分页器
    """

    class Input(Schema):
        """url parameters中的参数"""
        page: int = Field(1, ge=1)
        per_page: int = Field(10, ge=1)

    class Output(Schema):
        """自定义分页输出的格式"""
        page: int
        per_page: int
        total: int
        items: list[Any]  # `items` is a default attribute

    def paginate_queryset(self, queryset, pagination: Input, **params):
        """
        分页函数
        """
        page = pagination.page
        per_page = pagination.per_page
        offset = (page - 1) * per_page
        total = queryset.count()
        items = queryset[offset: offset + per_page]
        return {
            'items': items,
            'page': page,
            'per_page': per_page,
            'total': total,
        }


ninja_api = NinjaAPI(
    title=f'{settings.PROJECT_CODE} 文档中心',
    renderer=CustomRenderer(),
    version='v0.1.0',
    description='小麦数据库',
    docs_url='/docs' if settings.DEBUG else None,  # 在线文档线上不可用
    openapi_url='/openapi.json' if settings.DEBUG else None,  # open.json线上不可用
    openapi_extra={
    },
)


@ninja_api.get('/home/count')
def home(request):
    return dict(gene=Gene.objects.count(),
                genefamily=GeneFamily.objects.count())

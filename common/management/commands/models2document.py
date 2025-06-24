"""转model为文档"""
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.apps import apps
from django.db import models
from ninja.management.utils import command_docstring


def export_to_markdown(fields_info, model_name):
    """组织md格式"""
    markdown_table = f'### 表： {model_name} \n\n'
    markdown_table += '| 字段名称 | 数据类型 | 描述 | 数据库约束 | 业务功能约束 | 备注 |\n'
    markdown_table += '| --- | --- | --- | --- | --- | --- |\n'

    for field in fields_info:
        markdown_table += (
            f'| {field["字段名称"]} '
            f'| {field["数据类型"]} '
            f'| {field["描述"]} '
            f'| {field["数据库约束"]} '
            f'| {field["业务功能约束"]} '
            f'| {field["备注"]} |\n'
        )

    return markdown_table


def get_model_info(model: models.Model):
    """获取模型信息"""
    fields_info = []
    for field in model._meta.get_fields():
        # 跳过反向关系字段
        if field.auto_created and isinstance(field, models.ManyToOneRel):
            continue

        # 字段名称
        field_name = field.name

        # 数据类型
        data_type = type(field).__name__

        # 描述（如果定义了 verbose_name）
        description = getattr(field, 'verbose_name', '未定义')

        # 数据库约束（如主键、唯一、外键等）
        db_constraints = []
        if hasattr(field, 'primary_key') and field.primary_key:
            db_constraints.append('主键')
        if hasattr(field, 'unique') and field.unique:
            db_constraints.append('唯一')
        if hasattr(field, 'null') and not field.null:
            db_constraints.append('非空')
        if hasattr(field, 'auto_created') and field.auto_created:
            db_constraints.append('自增')
        if isinstance(field, models.ForeignKey):
            db_constraints.append('外键')
        if hasattr(field, 'default') and field.default != models.fields.NOT_PROVIDED:
            db_constraints.append('默认')

        # 业务功能约束（需要手动定义或注释中提取）
        business_constraints = '<br>'.join(['搜索字段', '过滤字段', '展示字段'])

        # 备注（可以是注释或其他自定义属性）
        notes = getattr(field, 'help_text', '无')

        fields_info.append({
            '字段名称': field_name,
            '数据类型': data_type,
            '描述': description,
            '数据库约束': '<br>'.join(db_constraints),
            '业务功能约束': business_constraints,
            '备注': notes
        })
    return fields_info


def save_markdown_to_file(markdown_table, file_path='output'):
    """保存 Markdown"""
    file_path += '.md'
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_table)
        print(f'Markdown 表格已成功保存到 {file_path}')
    except Exception as exc:  # pylint: disable=broad-except
        print(f'保存 Markdown 表格时出错: {exc}')


class Command(BaseCommand):
    """
    Example:

        ```terminal
        python manage.py export_openapi_schema
        ```

        ```terminal
        python manage.py export_openapi_schema --api project.urls.api
        ```
    """

    help = 'Exports Open API schema'

    def _introspect_model(self, model_class):
        field_data = []

        for field in model_class._meta.get_fields():
            if field.auto_created and not field.concrete:
                continue  # 跳过 ManyToOneRel、GenericForeignKey 等关系型字段

            field_info = {
                'name': field.name,
                'type': field.get_internal_type(),
                'verbose_name': getattr(field, 'verbose_name', ''),
                'null': getattr(field, 'null', False),
                'blank': getattr(field, 'blank', False),
                'unique': getattr(field, 'unique', False),
                'max_length': getattr(field, 'max_length', None),
                'choices': getattr(field, 'choices', None),
                'help_text': getattr(field, 'help_text', ''),
                'default': field.default if field.has_default() else None,
            }

            field_data.append(field_info)

        return field_data

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--output',
            dest='output',
            default=None,
            type=str,
            help='Output models to a file (outputs to stdout if omitted).',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        # 获取当前项目中所有的模型
        all_models = apps.get_models()

        # 遍历并打印模型名称
        for model in all_models:
            if model._meta.app_label in ('admin', 'auth', 'contenttypes', 'sessions'):
                continue
            print(f'应用名称: {model._meta.app_label}, 模型名称: {model.__name__}')
            fields_info = get_model_info(model)
            markdown_table = export_to_markdown(fields_info, model.__name__)
            # result = json.dumps(info)

            if options['output']:
                save_markdown_to_file(markdown_table,
                                      file_path=str(Path(options['output'], f'{model.__name__}（model）'))
                                      )
            else:
                save_markdown_to_file(markdown_table, file_path=f'{model.__name__}（model）')


__doc__ = command_docstring(Command)

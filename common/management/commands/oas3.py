"""
把 OpenAPI Specification 的格式转换为符合组内技术文档规范的 SOP 文档（markdown格式）。

支持的最小版本为 3.1.0 , 官方定义如下： https://spec.openapis.org/oas/v3.1.0

**必要条件**：

* **oas 版本 >= v3.1.0**
* **django-ninja >= 1.1.0**

如需使用此模块，请先执行命令 ``pip install 'mdutils>=1.6.0' 'openapi3-parser>=1.1.21'`` 安装按需依赖。
"""

try:
    from mdutils.mdutils import MdUtils
    from openapi_parser import parse
    from openapi_parser.specification import Array
except ImportError:
    raise Exception(
        'Please execute command `pip install "mdutils>=1.6.0" "openapi3-parser>=1.1.21"` '
        'to install required packages first before using pycngbdb.utils.oas3 module.'
    ) from ImportError

# pylint: disable=line-too-long
REQUEST_STRING = '''[1]字段名称。对于“数据类型”为  `string`  的JSON序列化字符串时，必须以  `field_name[*][field_name]`  和  `field_name[field_name]`  的字段名称逐层详细说明下属的元素和键值对。\n
[2]字段是否必填。应填写 `Y`  、  `N`  或  `Y：条件说明。N：条件说明。` 。  `Y`  表示必填，不支持对应数据类型的空值，必须发送此字段；  `N`  表示选填，支持对应数据类型的空值；条件说明则应具体描述什么条件下为必填或者选填。\n
[3]字段数据类型。只允许填写：  `string`  、  `integer`  、  `float`  、  `number`  （  `integer`  和  `float`  的并集）、  `boolean`  、  `file`。\n
[4]字段值域以及取值说明。每个取值必须符合“数据类型”列的声明。以格式  `取值：说明。`  逐一对取值或取值区间进行说明。对于“数据类型”为  `integer`  、  `float`  、  `number`  且值域为一个连续范围时，应当使用区间表示法。没有值域限制则填写  `无`。\n
[5]字段内容的格式限制。包括但不限于文本长度、文本格式等的说明。格式限制将影响和决定400状态码的响应。\n
[6]字段说明。说明此字段是什么，有什么用途，等等。\n'''  # noqa: E501

# pylint: disable=line-too-long
RESPONSE_STRING = '''[7]字段名称。对于“数据类型”为  `array[object]`  和  `object`  的字段，必须进一步以  `field_name[*][field_name]`  和  `field_name[field_name]`  的字段名称逐层说明下属的元素和键值对。\n
[8]字段是否必定不为空值。应填写  `Y`  、  `N`  或  `Y：条件说明。N：条件说明。`  。  `Y`  表示必定不为空值；  `N`  表示可能为空值；条件说明则应具体描述什么条件下为空值或者不为空值。\n
[9]字段数据类型。只允许填写：  `string`  、  `integer`  、  `float`  、  `number`  （  `integer`  和  `float`  的并集）、  `boolean`  、  `array[数据类型]`  、  `object`。\n
[10]字段值域以及取值说明。每个取值必须符合“数据类型”列的声明。如需对取值进行说明，以格式  `取值：说明。`  逐一对取值或取值区间进行说明。对于“数据类型”为  `integer`  、  `float`  、  `number`  且值域为一个连续范围时，应当使用区间表示法。没有值域范围则填写  `无`。\n
[11]字段说明。说明此字段是什么，是什么内容格式，有什么特殊限制，等等。    '''  # noqa: E501

RESPONSE_405 = '''- 描述
使用了本文档中“HTTP方法”章节之外的方法。
- 数据体
无数据体要求，如响应了数据体都应当忽略。
- 示例
无    '''

RESPONSE_500 = '''- 描述
 服务器发生了错误。
- 数据体
 无数据体要求，如响应了数据体都应当忽略。
- 示例
 无。    '''

RESPONSE_200 = '''- 描述
 请求成功。
- 数据体
 无数据体要求，如响应了数据体都应当忽略。
- 示例
 无。    '''

RESPONSE_TABLE_HEADER = ('名称7', '是否非空8', '数据类型9', '值域10', '说明11')
REQUEST_TABLE_HEADER = ('名称1', '是否必填2', '数据类型3', '值域4', '格式限制5', '说明6')


class OAS3:
    """转换 oas3 的格式为符合组内技术文档规范的 SOP 文档。"""

    @staticmethod
    def _any_of(prop):
        """返回 anyOf 类型的联合值"""
        if prop.schema.type.value == 'anyOf':
            type_value = ','.join(
                [sch.type.value for sch in prop.schema.schemas if sch.type.value != 'null'])
        else:
            type_value = prop.schema.type.value
        return type_value

    def _common_method_in(self, operation):
        """除了options 和 other 之外的方法的传入参数"""
        # 有些参数是在 operation.parameters ,有些是在 operation.request_body.content
        if operation.request_body:
            content = operation.request_body.content[0]
            list_of_strings = list(REQUEST_TABLE_HEADER)
            for param in content.schema.properties:
                print(f'输入：{param.name}')
                if param.name in content.schema.required:
                    required = '是'
                else:
                    required = '否'
                list_of_strings.extend(
                    [param.name, required, self._any_of(param), param.schema.enum,
                     f'默认值: {param.schema.default}， 示例值：{param.schema.example}',
                     param.schema.description])
            result = {
                'title': operation.method.name,
                'permission_text': '没有任何权限限制。',
                'data_line': list_of_strings,
                'data_rows': len(content.schema.properties) + 1,
                'example_text': '无。'
            }
        else:
            list_of_strings = list(REQUEST_TABLE_HEADER)
            for param in operation.parameters:
                print(f'输入：{param.name}')
                list_of_strings.extend(
                    [param.name, param.required, self._any_of(param), param.schema.enum,
                     f'默认值: {param.schema.default}， 示例值：{param.schema.example}',
                     param.schema.description])
            result = {
                'title': operation.method.name,
                'permission_text': '没有任何权限限制。',
                'data_line': list_of_strings,
                'data_rows': len(operation.parameters) + 1,
                'example_text': '无。'
            }
        return result

    def _common_method_out(self, operation):
        """除了options 和 other 之外的方法的传出参数"""
        data = {
            'r_data_line': [],
            'r_data_rows': 0,
        }
        r_list_of_strings = list(RESPONSE_TABLE_HEADER)
        content = operation.responses[0].content  # 响应基本只有1个
        if content:
            schema = content[0].schema  # content 基本只有1个
            try:
                properties = schema.items.properties
            except AttributeError:
                try:
                    properties = schema.properties
                except AttributeError:
                    return data
            r_rows = len(properties) + 1
            for prop in properties:
                type_value = prop.schema.type.value
                items_properties = getattr(getattr(prop.schema, 'items', {}), 'properties', None)
                schema_properties = getattr(prop.schema, 'properties', None)
                items_or_schema_properties = items_properties or schema_properties
                print(f'输出：{prop.name}, {type_value}')
                if items_or_schema_properties:
                    r_rows -= 1  # 这种模式下items本身多一行，需要减掉
                    for inner_prop in items_or_schema_properties:
                        print('->', inner_prop.name)
                        r_rows += 1
                        r_list_of_strings.extend(
                            [
                                f'data[{prop.name}][{inner_prop.name}]',
                                ' ',
                                self._any_of(inner_prop),
                                ' ',
                                ' '
                            ]
                        )
                else:
                    r_list_of_strings.extend(
                        [
                            f'data[{prop.name}]',
                            ' ',
                            type_value,
                            ' ',
                            ' '
                        ]
                    )
            data = {
                'r_data_line': r_list_of_strings,
                'r_data_rows': r_rows,
            }
        return data

    def _method_factory(self, mdf, method=None):
        """
        书写 markdown, mdutils 官方示例： https://mdutils.readthedocs.io/en/latest/examples/Example_Python.html
        实现 HTTP 方法大块： 通常为 OPTIONS + 任意  + 其他方法
        :param mdf:
        :param method:
        :return:
        """
        if method == 'options':
            data = {
                'title': 'OPTIONS',
                'permission_text': '没有任何权限限制。',
                'data_text': '无数据要求，以任何形式发送的任何数据都将被忽略。',
                'example_text': '无。'
            }
        elif method == 'other':
            data = {
                'title': '其它方法',
                'permission_text': '没有任何权限限制。',
                'data_text': '无数据要求，以任何形式发送的任何数据都将被忽略。',
                'example_text': '无。'
            }
        else:
            # 获取输出参数
            data = self._common_method_out(method)
            # 获取输入参数
            data.update(self._common_method_in(method))

        # 1.权限
        mdf.new_header(level=3, title=data['title'])
        mdf.new_header(level=4, title='权限')
        mdf.new_line(data['permission_text'])
        # 2.请求
        mdf.new_header(level=4, title='请求')
        # 2.1 数据
        mdf.new_header(level=5, title='数据')
        if data.get('data_text'):
            mdf.new_line(data['data_text'])
        if data.get('data_line'):
            mdf.new_line()
            mdf.new_table(columns=len(REQUEST_TABLE_HEADER), rows=data.get('data_rows'), text=data.get('data_line'),
                          text_align='center')
            mdf.new_line(REQUEST_STRING)
        # 2.2 示例
        mdf.new_header(level=5, title='示例')
        mdf.new_line(data['example_text'])
        # 3.响应
        mdf.new_header(level=4, title='响应')
        # 3.1 200(响应状态）
        if data['title'].lower() == 'other':
            mdf.new_header(level=5, title='405')
            mdf.new_line(RESPONSE_405)
        elif data['title'].lower() == 'options':
            mdf.new_header(level=5, title='200')
            mdf.new_line(RESPONSE_200)
        else:
            mdf.new_header(level=5, title='200')
            if data.get('r_data_rows'):
                mdf.new_line(RESPONSE_200)
                mdf.new_line()
                mdf.new_table(columns=len(RESPONSE_TABLE_HEADER), rows=data.get('r_data_rows'),
                              text=data.get('r_data_line'),
                              text_align='center')
                mdf.new_line(RESPONSE_STRING)

    def to_sop(self, *args, **kwargs):
        """
        支持多种传参，示例如下：

        ::

          from pycngbdb.utils.oas3 import to_sop

          to_sop('http://dbdev.cngb.org/genebank_rice/api/openapi.json')

          to_sop('~/Downloads/openapi-3.1.0.json')

          to_sop(spec_string=json.dumps(openapi_310))
        """
        specification = parse(*args, **kwargs)
        # assert specification == ninja_api.get_openapi_schema()
        for path in specification.paths:
            supported_methods = ','.join([ope.method.value for ope in path.operations])
            print(f'Operation: {path.url}, methods: {supported_methods}')
            operation = path.operations[0]
            mdf = MdUtils(file_name=operation.operation_id, title=operation.summary)
            mdf.new_header(level=1, title=path.url)
            # 1 描述 #
            mdf.new_header(level=2, title='描述')
            mdf.new_paragraph(operation.description or '')
            # 2 URL #
            mdf.new_header(level=2, title='URL')
            mdf.new_line(path.url)
            mdf.new_line('协议和域名视具体部署的环境而异。')
            # 3 内容类型 #
            mdf.new_header(level=2, title='内容类型')

            if operation.request_body:
                para_type = 'application/json'
            elif operation.parameters:
                para_type = 'multipart/form-data'
            else:
                para_type = 'None'
            mdf.new_line(f'  - {para_type}')
            # 4 HTTP 方法 #
            mdf.new_header(level=2, title='HTTP方法')
            self._method_factory(mdf, 'options')

            self._method_factory(mdf, operation)

            self._method_factory(mdf, 'other')

            # 5 通用响应 #
            mdf.new_header(level=2, title='通用响应')
            mdf.new_line('所有HTTP方法都支持以下响应。')
            mdf.new_header(level=3, title='500')
            mdf.new_line(RESPONSE_500)

            mdf.create_md_file()


to_sop = OAS3().to_sop

to_sop('http://127.0.0.1:8000/api/openapi.json')

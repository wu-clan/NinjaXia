#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def handling_assertions(response, assert_text) -> str:
    """
    **处理断言**

    - 断言格式：像pytest断言一样使用它 -> assert 期望值 条件 比较值

    比较值说明：

    - 仅有 {{response}}.get(''), ${response}.get(''), @response.get('') 三种情况

    示例:

    - assert 200 == {{response}}.get('status_code')
    - assert 200 != $response.get('status_code')
    - assert 'OK' in @(response).get('url')

    get('')取值范围::

    {"url": None, "status_code": 200,"elapsed": 0,"headers": {},"cookies": {},
    "result": None,"content": None,"text": None}

    你只能在这些范围中取值, 其中result, content, text是扩展值,根据请求结果自动扩展取值范围

    :param response:
    :param assert_text:
    :return:
    """
    if not assert_text.startswith('assert'):
        raise Exception('断言内容格式错误，必须以assert开头')
    if '{{response}}.' in assert_text and '$(response).' in assert_text:
        raise Exception('断言内容格式错误，不能同时使用{{response}}、$(response)、@response')
    if '{{response}}.' in assert_text and '@response.' in assert_text:
        raise Exception('断言内容格式错误，不能同时使用{{response}}、$(response)、@response')
    if '$(response).' in assert_text and '@response.' in assert_text:
        raise Exception('断言内容格式错误，不能同时使用{{response}}、$(response)、@response')
    if '{{response}}.' in assert_text:
        new_assert_text = assert_text.replace('{{response}}', str(response))
    elif '$(response).' in assert_text:
        new_assert_text = assert_text.replace('$(response)', str(response))
    elif '@response.' in assert_text:
        new_assert_text = assert_text.replace('@response', str(response))
    else:
        raise Exception('断言内容格式错误, 缺少比较值条件')
    get_code = ''.join(assert_text).split('.')[1:]
    use_code = None
    if len(get_code) < 1:
        raise Exception('断言内容格式错误，缺少比较值条件')
    if len(get_code) == 1:
        use_code = get_code[0]
    if len(get_code) > 1:
        use_code = '.'.join(get_code)
    if use_code.startswith('get('):
        try:
            r_text = eval(f'{response}.{use_code}')
        except Exception as e:
            err = str(e.args).replace("\'", '"').replace('\\', '')
            raise Exception(f'断言内容格式错误, {use_code}不是一个有效的取值代码, 详情:{err}')
    else:
        r_text = '断言内容格式错误, 请检查比较值获取条件'
    try:
        exec(new_assert_text)
    except AssertionError as e:
        if e.args:
            return f"FAIL, {str(e)}"
        else:
            a_text = new_assert_text.split(' ')
            if a_text[2] == '==':
                return f"FAIL, {a_text[1]} != {r_text}"
            elif a_text[2] == '!=':
                return f"FAIL, {a_text[1]} == {r_text}"
            elif a_text[2] == '>':
                return f"FAIL, {a_text[1]} <= {r_text}"
            elif a_text[2] == '<':
                return f"FAIL, {a_text[1]} >= {r_text}"
            elif a_text[2] == '>=':
                return f"FAIL, {a_text[1]} < {r_text}"
            elif a_text[2] == '<=':
                return f"FAIL, {a_text[1]} > {r_text}"
            elif a_text[2] == 'in':
                return f"FAIL, {a_text[1]} not in {r_text}"
            elif a_text[2] == 'not in':
                return f"FAIL, {a_text[1]} in {r_text}"
            else:
                return f"FAIL, {a_text[2]}"
    except Exception as e:
        raise Exception(f'断言格式错误，错误信息: {e}')
    else:
        return 'PASS'


if __name__ == '__main__':
    a = handling_assertions('{"status_code": 200, "msg": "success"}', "assert 20 == {{response}}.get('status_code')")
    print(a)
    a = handling_assertions('{"status_code": 20, "msg": "success"}', "assert 'fail' not in @response.get('msg'), 'err'")
    print(a)
    a = handling_assertions('{"status_code": 2', "assert 2 == $(response).get('status_code').get('test')")
    print(a)

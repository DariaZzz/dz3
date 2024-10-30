# import re
#
#
# def parse_config(config_text):
#     # Удаляем комментарии
#     config_text = remove_comments(config_text)
#
#     # Обработка словарей
#     return parse_dict(config_text)
#
# def parse_id(text):
#     pattern = r'def [a-zA-Z_]\w*'
#     matches = re.findall(pattern, text, re.DOTALL)
#     result = {}
#
#
#
# def remove_comments(text):
#     # Удаляем однострочные комментарии
#     text = re.sub(r'\|\|.*', '', text)
#     # Удаляем многострочные комментарии
#     text = re.sub(r'%\{.*?%\}', '', text, flags=re.DOTALL)
#     return text
#
#
# def parse_dict(text):
#     pattern = r'dict\(\s*(.*?)\s*\)'
#     matches = re.findall(pattern, text, re.DOTALL)
#     result = {}
#
#     for match in matches:
#         items = match.split(',')
#         for item in items:
#             key_value = item.split('=')
#             if len(key_value) != 2:
#                 raise SyntaxError(f"Invalid key-value pair: {item}")
#             key = key_value[0].strip()
#             value = key_value[1].strip()
#             result[key] = parse_value(value)
#
#     return result
#
#
# def parse_value(value):
#     value = value.strip()
#     if re.match(r'^[0-9]+$', value):
#         return int(value)
#     elif re.startswith('def'):
#         # Преобразуем в число
#     elif value.startswith('dict'):
#         return parse_dict(value)  # Рекурсивный вызов
#     else:
#         raise SyntaxError(f"Invalid value: {value}")

##########################################################################
# import re
#
# variables = {}
#
#
# def parse_config(config_text):
#     global variables
#     variables = {}  # Сброс глобальных переменных
#     # Удаляем комментарии
#     config_text = remove_comments(config_text)
#
#     # Обработка определений переменных
#     parse_definition(config_text)
#
#     # Обработка словарей
#     return parse_dict(config_text)
#
#
# def remove_comments(text):
#     # Удаляем однострочные комментарии
#     text = re.sub(r'\|\|.*', '', text)
#     # Удаляем многострочные комментарии
#     text = re.sub(r'%\{.*?%\}', '', text, flags=re.DOTALL)
#     return text
#
#
# def parse_dict(text):
#     pattern = r'dict\(\s*(.*?)\s*\)'
#     matches = re.findall(pattern, text, re.DOTALL)
#     result = {}
#
#     for match in matches:
#         items = match.split(',')
#         for item in items:
#             key_value = item.split('=')
#             if len(key_value) != 2:
#                 raise SyntaxError(f"Invalid key-value pair: {item}")
#             key = key_value[0].strip()
#             value = key_value[1].strip()
#             result[key] = parse_value(value)
#
#     return result
#
#
# def parse_value(value):
#     value = value.strip()
#
#     # Обработка чисел
#     if re.match(r'^[0-9]+$', value):
#         return int(value)  # Преобразуем в число
#
#     # Проверка на имена переменных
#     elif is_valid_variable_name(value):
#         if value in variables:
#             return variables[value]  # Возвращаем значение переменной
#         else:
#             raise SyntaxError(f"Undefined variable: {value}")
#
#     raise SyntaxError(f"Invalid value: {value}")
#
#
# def is_valid_variable_name(name):
#     """Проверяет, является ли имя переменной допустимым."""
#     return bool(re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name))
#
#
# def parse_definition(definition):
#     global variables
#     pattern = r'def\s+([_a-zA-Z][_a-zA-Z0-9]*)\s*=\s*(.+?);'
#     matches = re.findall(pattern, definition)
#
#     for name, value in matches:
#         if not is_valid_variable_name(name.strip()):
#             raise SyntaxError(f"Invalid variable name: {name.strip()}")
#         variables[name.strip()] = parse_value(value.strip())
##############################################################
import re
from inspect import stack

variables = {}
service_words = ['dict(', ')', 'abs(', 'max(']
dict_stack = []


def parse_config(config_text):
    global variables
    variables = {}  # Сброс глобальных переменных
    # Удаляем комментарии
    config_text = remove_comments(config_text)

    config_text = parse(config_text)
    # Обработка определений переменных
    # parse_definition(config_text)

    # Обработка словарей
    # return parse_dict(config_text)

def parse(config_text):
    string = ""
    for symbol in config_text:
        if symbol != '\n':
            string += symbol
        if symbol == ';':
            if re.match(r'\s*def\s*', string):
                parse_definition(string)
                string = ''
        elif symbol == ')':
            if re.match(r'\s*dict\((.+?)\)', string):
                parse_dict(string)
                string = ''


def remove_comments(text):
    # Удаляем однострочные комментарии
    text = re.sub(r'\|\|.*', '', text)
    # Удаляем многострочные комментарии
    text = re.sub(r'%\{.*?%\}', '', text, flags=re.DOTALL)
    return text


def parse_dict(text):
    pattern = r'\s*dict\(\s*(.*?)\s*\)'
    matches = re.findall(pattern, text, re.DOTALL)
    result = {}

    for match in matches:
        items = match.split(',')
        for item in items:
            new_item = item
            if re.match(r'(.*?)dict\(\s*(.*?)\s*', item):
                if re.match(r'\s*[_a-zA-Z]\w+\s*=\s*dict\(\s*(.*?)\s*', item):
                    my_var = re.findall(r'[_a-zA-Z]\w+', item)[0]
                    # dict_stack.append(my_var)
                    result[my_var] = parse_dict(item + ')')
                    # new_item = re.findall(r'\s*dict\(\s*(.*?)\s*', item)
                    # string = re.findall(r'dict\(\s*(.*?)\s*', item)
                else:
                    raise SyntaxError("Wrong name of var in dict")
                # parse_dict(re.findall('\s*dict\(\s*(.*?)\s*', item))
            key_value = new_item.split('=')
            if len(key_value) != 2:
                raise SyntaxError(f"Invalid key-value pair: {item.strip()}")
            key = key_value[0].strip()
            value = key_value[1].strip()
            result[key] = parse_value(value)

    return result


def parse_value(value):
    value = value.strip()

    # Обработка чисел
    if re.match(r'^[0-9]+$', value):
        return int(value)  # Преобразуем в число

    # Проверка на имена переменных
    elif is_valid_variable_name(value):
        if value in variables:
            return variables[value]  # Возвращаем значение переменной
        else:
            raise SyntaxError(f"Undefined variable: {value}")

    raise SyntaxError(f"Invalid value: {value}")


def is_valid_variable_name(name):
    """Проверяет, является ли имя переменной допустимым."""
    return bool(re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name))


def parse_definition(definition):
    global variables
    pattern1 = r'def\s+([_a-zA-Z]\w*)\s*=\s*(.+?);'
    # pattern2 = r'def\s+([_a-zA-Z]\w*)\s*=\s*(dict\()(.+)(\));'
    # pattern2 = r'def\s+([_a-zA-Z][_a-zA-Z0-9]*)\s*=\s*dict\((.+?)\);\s*'

    # pattern3 = r'def\s+([_a-zA-Z][_a-zA-Z0-9]*)\s*=\s*([_a-zA-Z][_a-zA-Z0-9]*)'

    matches1 = re.findall(pattern1, definition)
    for name, value in matches1:
        if not is_valid_variable_name(name.strip()):
            raise SyntaxError(f"Invalid variable name: {name.strip()}")
        variables[name.strip()] = parse_value(value.strip())


    # matches2 = re.findall(pattern2, definition)
    # for name, value in matches2:
    #     if not is_valid_variable_name(name.strip()):
    #         raise SyntaxError(f"Invalid variable name: {name.strip()}")
    #     variables[name.strip()] = parse_value(value.strip())




    # matches3 = re.findall(pattern3, definition)


    # for name, value in matches1:
    #     if not is_valid_variable_name(name.strip()):
    #         raise SyntaxError(f"Invalid variable name: {name.strip()}")
    #     variables[name.strip()] = parse_value(value.strip())
    #
    # for name, value in matches2:
    #     if not is_valid_variable_name(name.strip()):
    #         raise SyntaxError(f"Invalid variable name: {name.strip()}")
    #     variables[name.strip()] = parse_value(value.strip())
    #
    # for name, value in matches3:
    #     if not is_valid_variable_name(name.strip()):
    #         raise SyntaxError(f"Invalid variable name: {name.strip()}")
    #     variables[name.strip()] = parse_value(value.strip())



# Пример использования:
config_text = """
def item1 = 1;
dict(
    subitem1 = 2,
    subitem2 = dict(
        inner_item = 3
    )
)
"""

try:
    result = parse_config(config_text)
    print(result)
except SyntaxError as e:
    print(f"Syntax error: {e}")

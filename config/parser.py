import re


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
#         return int(value)
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
from importlib.resources import read_text

variables = {}
service_words = ['dict(', ')', 'abs(', 'max(']
dict_stack = []

def parse(config_text):
    global variables
    variables = {}
    string = ""
    try:
        string = config_text.read(1)
        symbol = string
    except:
        raise SyntaxError("Файл пустой")
    while symbol != '':
        symbol = config_text.read(1)
        # string += symbol
        if symbol == ';':
            if re.match(r'\s*def\s*(.*?)\s*=\s*(.*?);', string + symbol, re.DOTALL):
                variables.update(parse_definition(string + symbol))
                string = ''
        elif symbol == ')':
            while symbol == ')' or symbol == '\n' or symbol == ' ':
                string += symbol
                symbol = config_text.read(1)
            if re.match(r'\s*dict\((.+?)\)', string + symbol, re.DOTALL):
                variables.update(parse_dict(string))
                string = ''
        else:
            string += symbol
    return variables


def parse_dict(text):
    pattern1 = r'\s*dict\(\s*(.*?)\s*(\))+\s*'
    matches1 = re.findall(pattern1, text, re.DOTALL)
    print(matches1)
    # pattern2 = r'([_a-zA-Z]\w*)'
    # matches2 = re.findall(pattern2, text, re.DOTALL)
    # pattern3 = r'def\s+([_a-zA-Z]\w*)\s*=\s*(.+?);'
    # matches3 = re.findall(pattern3, text, re.DOTALL)

    result = {}

    for match in matches1:
        items = match.split('\n')

        for item in items:
            if re.match(r'\s*([_a-zA-Z]\w*)\s*=\s*(.+?)',item):
                 if re.match(r'\s*[_a-zA-Z]\w+\s*=\s*dict\(\s*(.*?)\s*', item):

                    dict_stack.append(re.findall(r'[_a-zA-Z]\w+', item)[0])
                    result[dict_stack.pop()] = parse_dict(item)
                    return result
                 else:
                     result.update(parse_assignment(item))
            elif re.match(r'\s*dict\(\s*(.*?)\s*', item):
                result.update(parse_dict(item + ')'))
            else:
                raise SyntaxError("Убедитесь в правильности содержимого словаря")
                    # if re.findall(r'\s*dict\(\s*(.*?)\s*', item)[0] != '':
                    #     new_item = re.findall(r'\s*dict\(\s*(.*?)\s*', item)[0]
                    # string = re.findall(r'dict\(\s*(.*?)\s*', item)
                # parse_dict(re.findall('\s*dict\(\s*(.*?)\s*', item))
                # key_value = new_item.split('=')
                # if len(key_value) != 2:
                #     raise SyntaxError(f"Invalid key-value pair: {item.strip()}")
                # key = key_value[0].strip()
                # value = key_value[1].strip()
                # result[key] = parse_value(value)

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

    elif re.match(r'\s*dict\(\s*(.*?)\s*', value, re.DOTALL):
        parse


    raise SyntaxError(f"Invalid value: {value}")


def is_valid_variable_name(name):
    """Проверяет, является ли имя переменной допустимым."""
    return bool(re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name))


def parse_definition(definition):
    # global variables
    result = {}
    pattern1 = r'def\s+([_a-zA-Z]\w*)\s*=\s*(.+?);'

    matches1 = re.findall(pattern1, definition)
    for name, value in matches1:
        if not is_valid_variable_name(name.strip()):
            raise SyntaxError(f"Invalid variable name: {name.strip()}")
        result[name.strip()] = parse_value(value.strip())
    return result


def parse_assignment(definition):
    # global variables
    result = {}
    pattern = r'\s*([_a-zA-Z]\w*)\s*=\s*(.+?)'

    matches = re.findall(pattern, definition)
    for name, value in matches:
        if not is_valid_variable_name(name.strip()):
            raise SyntaxError(f"Invalid variable name: {name.strip()}")
        result[name.strip()] = parse_value(value.strip())
    return result



# Пример использования:
file = open('example.txt', 'r')
# config_text = file.read()

try:
    result = parse(file)
    print(result)
except SyntaxError as e:
    print(f"Syntax error: {e}")

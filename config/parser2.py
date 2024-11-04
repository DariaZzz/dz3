import re
from importlib.resources import read_text

dicts = []
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
        if symbol == ';':
            if re.match(r'\s*def\s*(.*?)\s*=\s*(.*?);', string + symbol, re.DOTALL):
                variables.update(parse_definition(string + symbol))
                string = ''
        elif symbol == ')':
            string += symbol
            while symbol != '' and string.count('(') != string.count(')'):
                try:
                    symbol = config_text.read(1)
                    string += symbol
                except:
                    raise SyntaxError("Не хватает закрывающихся скобок")
            if re.match(r'\s*dict\(\s*(.+?)\s*\)$', string + symbol, re.DOTALL):
                dicts.append(parse_dict(string))
                string = ''
        else:
            string += symbol
    return variables, dicts

def parse_dict(text):
    pattern = r'\s*dict\(\s*(.*?)\s*\)$'
    config_text = re.findall(pattern, text, re.DOTALL)[0]
    # print(config_text)

    result = {}
    try:
        string = config_text[0]
        symbol = string
        config_text = config_text[1:]
    except:
        raise SyntaxError("Файл пустой")
    while config_text != '':
        symbol = config_text[0]
        config_text = config_text[1:]
        if symbol == ',' or config_text == '':
            if symbol != ',':
                string += symbol
            if string.count('dict') == 0 and re.match(r'\s*(.+?)\s*=\s*(.+?)', string, re.DOTALL):
                new_var = parse_assignment(string)
                result.update(new_var)
                variables.update(new_var)
                string = ''
            elif symbol == ',':
                string += symbol
        elif symbol == ')':
            string += symbol
            while config_text != '' and string.count('(') != string.count(')'):
                try:
                    symbol = config_text[0]
                    config_text = config_text[1:]
                    string += symbol
                except:
                    print(string)
                    raise SyntaxError("Не хватает закрывающихся скобок")
            if re.match(r'\s*(.+?)\s*=\s*dict\((.+?)\)$', string, re.DOTALL):
                name = re.findall(r'[a-zA-Z_]\w+', string, re.DOTALL)[0]
                if name == 'inner_item2':
                    print()
                new_dict = re.findall(r'\s*[a-zA-Z_]\w+\s*=\s*(.+?)$', string, re.DOTALL)[0]
                result[name] = parse_dict(new_dict)
                string = ''
        else:
            string += symbol
    return result

def parse_value(value):
    value = value.strip()

    # Обработка чисел
    if re.match(r'^[+-]?[0-9]+$', value):
        return int(value)  # Преобразуем в число

    # Проверка на имена переменных
    elif is_valid_variable_name(value):
        if value in variables:
            return variables[value]  # Возвращаем значение переменной
        else:
            raise SyntaxError(f"Undefined variable: {value}")

    elif re.match(r'\s*dict\(\s*(.*?)\s*\)', value, re.DOTALL):
        parse_dict(value)


    raise SyntaxError(f"Invalid value: {value}")


def is_valid_variable_name(name):
    """Проверяет, является ли имя переменной допустимым."""
    return bool(re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name))


def parse_definition(definition):
    # global variables
    result = {}
    pattern = r'def\s+([_a-zA-Z]\w*)\s*=\s*(.*?);'

    matches = re.findall(pattern, definition)
    for name, value in matches:
        if not is_valid_variable_name(name.strip()):
            raise SyntaxError(f"Invalid variable name: {name.strip()}")
        result[name.strip()] = parse_value(value.strip())
    return result


def parse_assignment(definition):
    # global variables
    result = {}
    pattern = r'\s*([_a-zA-Z]\w*)\s*=\s*(.+?)$'

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

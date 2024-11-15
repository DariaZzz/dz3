import re
# from importlib.resources import read_text
import argparse
from pathlib import Path

import yaml

comments = []
dicts = []
variables = {}

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
            if re.match(r'^\s*def\s*(.*?)\s*=\s*(.*?);$', string + symbol, re.DOTALL):
                new_def = parse_definition(string + symbol)
                dicts.append(dict({next(iter(new_def)): next(iter(new_def.values()))}))
                variables.update(new_def)
                string = ''
            else:
                raise SyntaxError(f"Неправильный формат определения в строке '{string}'")
        elif symbol == ')':
            string += symbol
            while symbol != '' and string.count('(') != string.count(')'):
                symbol = config_text.read(1)
                string += symbol
            if string.count('(') != string.count(')'):
                raise SyntaxError("Не хватает закрывающихся скобок")

            if re.match(r'^\s*dict\(\s*(.+?)\s*\)$', string + symbol, re.DOTALL):
                new_d = parse_dict(string)
                dicts.append(new_d)
                variables.update(new_d)
                string = ''
        elif symbol == ']':
            string += symbol
            if re.match(r'\s*\^\[(.+?)]\s*$', string):
                dicts.append(calculation(string))
                string = ''
        elif '||' in string:
            while symbol != '\n':
                string += symbol
                symbol = config_text.read(1)
            comment = re.findall(r'^\|\|\s*(.*?)\s*$', string, re.DOTALL)[0]
            comments.append(comment)
            string = ''
        elif '{%' in string:
            while '%}' not in string:
                string += symbol
                symbol = config_text.read(1)
                if symbol == '':
                    raise SyntaxError("Комментарий не закрыт")
            comment = re.findall(r'^\s*\{\%\s*(.*?)\s*\%\}$', string, re.DOTALL)[0]
            list_of_comments = comment.split('\n')
            for comm in list_of_comments:
                comments.append(comm)
            string = ''
        elif '%}' in string and '{%' not in string:
            raise SyntaxError("Комментарий не открыт")
        elif symbol == '\n' and re.match(r'^\s*def\s*(.*?)\s*=\s*(.*?)\s*$', string, re.DOTALL):
            raise SyntaxError(f"Не хватает ';' в строке '{string}'")
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
        if string != '' and (symbol == ',' or config_text == '') and string.count('dict') == 0:
            if string.count('subitem1') != 0:
                print()
            if symbol != ',':
                string += symbol
            if re.match(r'\s*(.+?)\s*=\s*(.+?)\s*', string, re.DOTALL):
                new_var = parse_assignment(string)
                result.update(new_var)
                variables.update(new_var)
                string = ''
            elif symbol != ',':
                string += symbol
        elif string != '' and (symbol == ')' or config_text == '') and string.count('dict') != 0:
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
                new_dict = re.findall(r'\s*[a-zA-Z_]\w+\s*=\s*(.+?)$', string, re.DOTALL)[0]
                parsed_dict = parse_dict(new_dict)
                variables[name] = parsed_dict
                result[name] = parsed_dict

                check_string = ''

                while config_text != '' and symbol != '\n':
                        symbol = config_text[0]
                        config_text = config_text[1:]
                        check_string += symbol
                if symbol == '\n' and config_text != '' and  check_string.count(',') == 0:
                    raise SyntaxError(f"Не хватает ',' после '{string}'")
                string = ''

        elif string != '' and symbol == '\n' and re.match(r'\s*([_a-zA-Z]\w*)\s*=\s*(.+?)\s*$', string, re.DOTALL)\
              and string.count('dict') == 0 and config_text != '':
            raise SyntaxError(f"Не хватает ',' в строке '{string}'")
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
        result[name.strip()] = parse_value(value.strip())
    return result

def calculation(text):
    pattern = r'\s*\^\[(.+?)\]\s*$'
    compute = re.findall(pattern, text, re.DOTALL)[0]

    pattern1 = r'^\s*(.+?)\s*(.+?)\s*\+\s*$'
    pattern2 = r'^\s*(.+?)\s*(.+?)\s*max\s*$'
    pattern3 = r'^\s*(.+?)\s*abs\s*$'

    if re.match(pattern1, compute, re.DOTALL):
        operation = '+'
    elif re.match(pattern2, compute, re.DOTALL):
        operation = 'max'
    elif re.match(pattern3, compute, re.DOTALL):
        operation = 'abs'
    else:
        raise SyntaxError(f"Неправильный формат операции {compute}")
    my_list = compute.split()
    res = ''
    match operation:
        case '+':
            operand1 = my_list[0]
            operand2 = my_list[1]
            num1 = parse_value(operand1)
            num2 = parse_value(operand2)
            res = num1+num2
        case 'max':
            operand1 = my_list[0]
            operand2 = my_list[1]
            num1 = parse_value(operand1)
            num2 = parse_value(operand2)
            res = max(num1, num2)
        case 'abs':
            operand = my_list[0]
            num = parse_value(operand)
            res = abs(num)
    return res

# # Пример использования:
# file = open('example.txt', 'r', encoding='utf8')
# # config_text = file.read()
#
# try:
#     result = parse(file)
#     print(result[1])
#     yaml_data = yaml.dump(result[1], allow_unicode=True, default_flow_style=False)
#     print(yaml_data)
# except SyntaxError as e:
#     print(f"Syntax error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсинг файла конфигурации.")
    parser.add_argument("filepath", type=str, help="Путь до файла конфигурации")

    args = parser.parse_args()
    file_path = Path(args.filepath)

    # Проверка существования файла
    if not file_path.is_file():
        print(f"Файл {file_path} не найден.")
    else:
        with file_path.open("r", encoding='utf8') as file:
            try:
                result = parse(file)
                # print(result[1])
                yaml_data = yaml.dump(result[1], allow_unicode=True, default_flow_style=False)
                for comment in comments[::-1]:
                    yaml_data = f'# {comment} \n' + yaml_data
                print(yaml_data)
            except SyntaxError as e:
                print(f"Ошибка синтаксиса: {e}")

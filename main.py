import argparse
import re
import sys
import yaml


class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.output = {}

    def parse(self, lines):
        for line in lines:
            line = line.strip()
            if not line or line.startswith('||'):
                continue  # Пропустить однострочные комментарии
            if line.startswith('%{'):
                continue  # Пропустить многострочные комментарии
            if line.startswith('%}'):
                continue  # Конец многострочного комментария
            self.parse_line(line)

    def parse_line(self, line):
        # Обработка объявления константы
        match = re.match(r'defs+([_a-zA-Z][_a-zA-Z0-9]*)s*=s*(.+);', line)
        if match:
            name = match.group(1)
            value = self.evaluate_expression(match.group(2))
            self.constants[name] = value
            return

        # Обработка словарей
        match = re.match(r'dict((.+))', line)
        if match:
            items = match.group(1).split(',')
            dictionary = {}
            for item in items:
                key_value = item.split('=')
                if len(key_value) != 2:
                    raise ValueError(f"Invalid dictionary entry: {item}")
                key = key_value[0].strip()
                value = self.evaluate_expression(key_value[1].strip())
                dictionary[key] = value
            self.output.update(dictionary)
            return

        raise ValueError(f"Syntax error: {line}")

    def evaluate_expression(self, expr):
        # Упрощенная обработка выражений
        expr = expr.strip()
        if expr.isdigit():
            return int(expr)
        elif expr in self.constants:
            return self.constants[expr]
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
            return self.constants.get(expr, None)

        # Обработка операций
        if '+' in expr:
            parts = expr.split('+')
            return sum(self.evaluate_expression(part.strip()) for part in parts)

        raise ValueError(f"Invalid expression: {expr}")


def main():
    parser = argparse.ArgumentParser(description='Convert custom config language to YAML.')
    parser.add_argument('input_file', help='Path to the input configuration file')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf8') as file:
            lines = file.readlines()

        config_parser = ConfigParser()
        config_parser.parse(lines)

        # Вывод результата в формате YAML
        print(yaml.dump(config_parser.output, default_flow_style=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()

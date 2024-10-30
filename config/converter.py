import argparse
import yaml
from parser import parse_config

def main():
    parser = argparse.ArgumentParser(description="Convert custom config language to YAML.")
    parser.add_argument('input_file', type=str, help='Path to the input config file')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        config_text = file.read()

    try:
        yaml_output = parse_config(config_text)
        print(yaml.dump(yaml_output, default_flow_style=False))
    except SyntaxError as e:
        print(f"Syntax error: {e}")

if __name__ == "__main__":
    main()

from configparser import ConfigParser
import os


CONFIG_FILE_PATH = 'config.ini'


def read_config(config_file=CONFIG_FILE_PATH):
    config = ConfigParser()
    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f'Config file not found: {config_file}')
        config.read(config_file)
    except FileNotFoundError:
        raise KeyError("Cannot find the config file.")
    return config


def get_config(section, option, config_file=CONFIG_FILE_PATH):
    config = read_config(config_file)
    try:
        value = config.get(section, option)
    except ConfigParser.NoSectionError:
        raise KeyError(f"The section, '{section}', does not exist in the config file.")
    except ConfigParser.NoOptionError:
        raise KeyError(f"The option, '{option}', does not exist in the section, '{section}'.")
    return value


if __name__ == "__main__":
    # Example usage
    source_file = get_config('INPUTS', 'SOURCE_FILE')
    print(f"The source file: {source_file}.")

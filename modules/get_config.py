from configparser import ConfigParser
import os


CONFIG_FILE_PATH = 'config.ini'


def read_config(config_file=CONFIG_FILE_PATH):
    """
    Reads the configuration file and returns a ConfigParser object.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        ConfigParser: The configuration parser object.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """

    config = ConfigParser()
    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f'Config file not found: {config_file}')
        config.read(config_file)
    except FileNotFoundError:
        raise KeyError("Cannot find the config file.")
    return config


def get_config(section, option, config_file=CONFIG_FILE_PATH):
    """
    Retrieves the value of the given option in the specified section from the configuration file.

    Args:
        section (str): The section in the config file.
        option (str): The option within the section to retrieve.
        config_file (str): The path to the configuration file.

    Returns:
        str: The value of the specified option.

    Raises:
        KeyError: If the section or option is not found in the config file.
    """
    
    config = read_config(config_file)
    try:
        value = config.get(section, option)
    except ConfigParser.NoSectionError:
        raise KeyError(f"The section, '{
                       section}', does not exist in the config file.")
    except ConfigParser.NoOptionError:
        raise KeyError(f"The option, '{
                       option}', does not exist in the section, '{section}'.")
    return value


if __name__ == "__main__":
    # Example usage
    source_file = get_config('INPUTS', 'SOURCE_FILE')
    print(f"The source file: {source_file}.")

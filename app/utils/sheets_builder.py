"""Build the sheets from the YAML files."""

import os
import re
from collections import OrderedDict
from pprint import pprint

import yaml

yaml.add_representer(OrderedDict, yaml.representer.SafeRepresenter.represent_dict)


def remove_prefix(filename):
    """Remove a prefix of the format 'XX_' where XX are digits, but keep it if it's part of the main name.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The filename without the prefix.
    """
    match = re.match(r'^\d{2}_(.+)', filename)
    if match:
        # Remove the 'XX_' prefix if found
        return match.group(1)
    return filename


def get_directory_structure(path):
    """Return a directory structure as a nested dictionary.

    Args:
        path (str): The path to the directory.

    Returns:
        str: The directory structure as yml string.
    """
    structure = OrderedDict()
    for entry in sorted(os.listdir(path)):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            # Apply remove_prefix to directories as well
            entry_name = remove_prefix(entry)
            structure[entry_name] = get_directory_structure(full_path)
        else:
            # If it's a YAML file, load its content
            if entry.endswith('.yml') or entry.endswith('.yaml'):
                # Remove file extension
                entry_name, _ = os.path.splitext(entry)
                entry_name = remove_prefix(entry_name)
                # Load content as YAML
                with open(full_path) as yml_file:
                    structure[entry_name] = yaml.safe_load(yml_file)
    return structure


def get_directory_as_yml_string(path):
    """Parse a directory and return its structure as a YAML string.

    Args:
        path (str): The path to the directory.

    Returns:
        str: The directory structure as yml string.
    """
    structure_dict = get_directory_structure(path)
    return yaml.dump(structure_dict, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    # Test the function with the current directory
    sheets = get_directory_as_yml_string('app/config/sheets')
    sheets = yaml.safe_load(sheets)
    pprint(sheets)

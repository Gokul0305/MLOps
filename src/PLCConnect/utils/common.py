import toml
from box import Box
import pathlib


def read_toml_to_box(file_path: pathlib.Path):
    """
    Read a TOML file and return its contents as a Box object.

    Args:
    - file_path (str): Path to the TOML file.

    Returns:
    - Box: Box object containing the contents of the TOML file.
    """
    if isinstance(file_path, pathlib.Path):
        try:
            # Read the TOML file
            with open(file_path, "r") as file:
                toml_data = toml.load(file)

            # Convert TOML data to Box
            box_data = Box(toml_data)

            return box_data
        except Exception as e:
            print(f"Error occurred while reading TOML file: {e}")
            return None
    else:
        raise Exception(f"Invalid Path {file_path}")

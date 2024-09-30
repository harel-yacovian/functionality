import re
import json
import pandas as pd
from typing import Union, Optional
from logs.logger import setup_logger, log_decorator, session_gid_var


@log_decorator(show_args_calling=False, show_args_returning=False)
def rcsv_file_pandas(filepath: str) -> str:
    return pd.read_csv(filepath)

@log_decorator(show_args_calling=False, show_args_returning=False)
def rtxt_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

@log_decorator(show_args_calling=False, show_args_returning=False)
def extract_json_from_string(input_str: str) -> Optional[Union[dict, list]]:
    """
    Extracts and parses a JSON object or array from a given string.

    Parameters:
    - input_str: A string that potentially contains a JSON object or array.

    Returns:
    - A Python dictionary or list if a valid JSON object or array is found and successfully parsed.
      Returns None if no valid JSON is found or if parsing fails.
    """
    # First, find the start of the JSON structure
    start_match = re.search(r'[{[]', input_str)
    if not start_match:
        print("No JSON found in the string.")
        return None

    # Find the last occurrence of } or ] to determine the end of the JSON structure
    end_match_object = input_str.rfind('}')
    end_match_array = input_str.rfind(']')

    # Use the later of the two positions
    end_pos = max(end_match_object, end_match_array) + 1

    # Extract the substring that is likely to be JSON
    json_str = input_str[start_match.start():end_pos]

    try:
        # Attempt to parse the extracted string into a Python object
        json_ret = json.loads(json_str)
        return json_ret
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

@log_decorator(show_args_calling=False, show_args_returning=False)
def rjson_file(filepath: str) -> dict:
    # Load the dictionary back from the file with UTF-8 encoding
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data_loaded = json.load(json_file)
    return data_loaded

@log_decorator(show_args_calling=False, show_args_returning=False)
def save_txt(text: str, file_path: str):
    """
    Saves a given string into a text file.

    Args:
    - text (str): The string to be saved.
    - file_path (str): The path of the file where the string will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

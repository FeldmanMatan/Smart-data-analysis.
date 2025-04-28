import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV or Excel file.

    Args:
        file_path (str): The path to the file.

    Returns:
        pd.DataFrame: The loaded data.

    Raises:
        ValueError: If the file type is not supported.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension == '.xlsx' or file_extension == '.xls':
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")
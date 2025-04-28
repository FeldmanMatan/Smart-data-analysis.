import pandas as pd

def sort_by(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """
    Sorts the data by the specified column.
    """
    if df is None:
        raise ValueError("No data loaded")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    filtered_df = df.sort_values(by=column, ascending=ascending)
    return filtered_df

def apply_filter(df: pd.DataFrame, column: str, filter_type, value) -> pd.DataFrame:
    """
    Applies a filter to the data.
    """
    if df is None:
        raise ValueError("No data loaded")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    if filter_type == "greater":
        col_type = df[column].dtype
        if col_type == int:
            filtered_df = df[df[column] > int(value)]
        elif col_type == float:
            filtered_df = df[df[column] > float(value)]
        else:
            filtered_df = df[df[column] > value]
    elif filter_type == "less":
        col_type = df[column].dtype
        if col_type == int:
            filtered_df = df[df[column] < int(value)]
        elif col_type == float:
            filtered_df = df[df[column] < float(value)]
        else:
            filtered_df = df[df[column] < value]
    elif filter_type == "equal":
        filtered_df = df[df[column] == value]
    elif filter_type == "contains":
        filtered_df = df[df[column].astype(str).str.contains(value, case=False)]
    else:
        raise ValueError("Invalid filter type")

    return filtered_df

# def count_occurrences(df: pd.DataFrame, conditions: dict) -> int:
#     """
#     Counts the number of rows that match the given conditions.
#
#     Args:
#         conditions: A dictionary where keys are column names and values are the
#                     values to match in those columns.
#
#     Returns:
#         The number of rows that satisfy all conditions.
#     """
#     if df is None:
#         raise ValueError("No data loaded")
#
#     query_string = " & ".join([f"`{col}` == '{value}'" for col, value in conditions.items()])
#     return len(df.query(query_string))
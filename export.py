import pandas as pd


def export_to_excel(df, path="export_data.xlsx"):
    """
    Exports DataFrame to Excel file.

    Args:
        df (DataFrame): The data to export
        path (str): Path for the Excel file

    Returns:
        str: Path to the exported file
    """
    df.to_excel(path, index=False)
    return path


def export_to_json(df, path="export_data.json"):
    """
    Exports DataFrame to JSON file.

    Args:
        df (DataFrame): The data to export
        path (str): Path for the JSON file

    Returns:
        str: Path to the exported file
    """
    df.to_json(path, orient="records")
    return path


def export_to_html(df ,graph=None, path=None): #,path=None
    """
    Exports DataFrame and optional graph to HTML files.

    Args:
        df (DataFrame): The data to export
        graph (plotly.Figure, optional): The graph to export

    Returns:
        tuple: Paths to the exported files
    """
    # Export DataFrame to HTML table
    table_path = path + "table_output.html"
    df.to_html(table_path)

    # Export graph if provided
    graph_path = None
    if graph:
        graph_path = "graph_output.html"
        graph.write_html(graph_path)

    return table_path, graph_path


def export_to_csv(df, path="export_data.csv"):
    """
    Exports DataFrame to CSV file.

    Args:
        df (DataFrame): The data to export
        path (str): Path for the CSV file

    Returns:
        str: Path to the exported file
    """
    df.to_csv(path, index=False)
    return path
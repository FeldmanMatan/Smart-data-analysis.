import pandas as pd
import plotly.express as px


def show_graph(df, query):
    """
    Creates a graph based on two columns specified by the user.

    Args:
        df (DataFrame): The data source
        query (str): User query in format "plot with X and Y"

    Returns:
        plotly.Figure: The generated graph object

    Raises:
        ValueError: If the query format is invalid or columns don't exist
    """
    try:
        # Identify graph type
        graph_type = "bar"  # default
        if "line" in query.lower():
            graph_type = "line"
        elif "scatter" in query.lower():
            graph_type = "scatter"
        elif "pie" in query.lower() and "with" in query:
            graph_type = "pie"

        # Check that query contains "with"
        if "with" not in query:
            raise ValueError("Query must contain the word 'with' followed by column names.")

        columns_str = query.split("with")[1].strip()
        if "and" not in columns_str:
            raise ValueError("Query must specify two columns separated by 'and'.")

        columns = [col.strip() for col in columns_str.split("and")]
        if len(columns) != 2:
            raise ValueError("Query must include exactly 2 columns.")

        x, y = columns

        # Check column existence with detailed error message
        if x not in df.columns:
            raise ValueError(f"Column '{x}' not found in dataframe. Available columns: {', '.join(df.columns)}")
        if y not in df.columns:
            raise ValueError(f"Column '{y}' not found in dataframe. Available columns: {', '.join(df.columns)}")

        # Create graph based on selected type
        fig = None
        if graph_type == "bar":
            fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")
        elif graph_type == "line":
            fig = px.line(df, x=x, y=y, title=f"{y} over {x}")
        elif graph_type == "scatter":
            fig = px.scatter(df, x=x, y=y, title=f"{y} vs {x}")
        elif graph_type == "pie":
            fig = px.pie(df, names=x, values=y, title=f"{y} distribution by {x}")

        fig.write_html('plot_output.html')
        return fig  # Return the figure object for further use

    except Exception as e:
        # Preserve original error info
        raise ValueError(f"Error generating graph: {str(e)}")


def show_average(df, query):
    """
    Calculates the average of a specified column.

    Args:
        df (DataFrame): The data source
        query (str): User query in format "average of X"

    Returns:
        str: The result message with the average value

    Raises:
        ValueError: If column doesn't exist or query format is invalid
    """
    try:
        if "average of" not in query.lower():
            raise ValueError("Query must contain 'average of' followed by column name.")

        column = query.split("average of")[1].strip()

        # Check column existence
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe. Available columns: {', '.join(df.columns)}")

        # Check if column is numeric
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"Column '{column}' is not numeric. Cannot calculate average.")

        avg = df[column].mean()
        return f"The average of {column} is: {avg:.2f}"
    except Exception as e:
        raise ValueError(f"Error calculating average: {str(e)}")


def show_count(df, columns):
    """
    Shows the count of values in a specified column.

    Args:
        df (DataFrame): The data source
        columns (list): List of column names to count

    Returns:
        str: The result message with counts

    Raises:
        ValueError: If no columns specified or columns don't exist
    """
    try:
        if not columns:
            raise ValueError("No column specified for counting.")

        column = columns[0]

        # Check column existence
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe. Available columns: {', '.join(df.columns)}")

        counts = df[column].value_counts()
        result = f"Counts in '{column}':\n\n"
        result += "\n".join(f"{val}: {count}" for val, count in counts.items())
        return result
    except Exception as e:
        raise ValueError(f"Error counting values: {str(e)}")


def show_dates(df, columns):
    """
    Shows dates related to values in a specified column.

    Args:
        df (DataFrame): The data source
        columns (list): List of column names to find dates for

    Returns:
        str: The result message with dates for each value

    Raises:
        ValueError: If no columns specified or no date column found
    """
    try:
        if not columns:
            raise ValueError("No column specified for timing.")

        date_column = None
        for col in df.columns:
            if "date" in col.lower():
                date_column = col
                break

        if not date_column:
            raise ValueError("No date column found in dataframe.")

        column = columns[0]

        # Check column existence
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe. Available columns: {', '.join(df.columns)}")

        filtered = df[[column, date_column]].dropna()
        output = f"Event dates for values in column '{column}':\n\n"
        for _, row in filtered.iterrows():
            output += f"{row[date_column]} - {row[column]}\n"
        return output
    except Exception as e:
        raise ValueError(f"Error finding dates: {str(e)}")
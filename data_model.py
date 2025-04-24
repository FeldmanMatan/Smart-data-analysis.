import pandas as pd
from intent_parser import parse_query


class DataModel:
    """Class for managing data and business logic"""

    def __init__(self):
        self.df = None
        self.filtered_df = None
        self.query_history = []

    def load_data(self, file_path):
        """
        Loads data from file.

        Args:
            file_path (str): Path to the data file

        Returns:
            DataFrame: The loaded data

        Raises:
            ValueError: If file format is unsupported
        """
        if file_path.endswith(".csv"):
            self.df = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            self.df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel.")

        self.filtered_df = self.df.copy()
        return self.df

    def apply_filter(self, column, filter_type, value):
        """
        Applies filter to the data.

        Args:
            column (str): Column to filter
            filter_type (str): Type of filter (greater, less, equal, contains)
            value: Value to filter by

        Returns:
            DataFrame: The filtered data

        Raises:
            ValueError: If no data loaded or filter type is unknown
        """
        if self.df is None:
            raise ValueError("No data loaded")

        # Convert to numeric if possible
        try:
            numeric_value = float(value)
            value = numeric_value
        except ValueError:
            pass  # Value remains as string

        # Apply filter
        if filter_type == "greater":
            self.filtered_df = self.df[self.df[column] > value]
        elif filter_type == "less":
            self.filtered_df = self.df[self.df[column] < value]
        elif filter_type == "equal":
            self.filtered_df = self.df[self.df[column] == value]
        elif filter_type == "contains":
            self.filtered_df = self.df[
                self.df[column].astype(str).str.contains(str(value), case=False, na=False)]
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")

        return self.filtered_df

    def clear_filters(self):
        """
        Clears all filters.

        Returns:
            DataFrame: The unfiltered data
        """
        if self.df is not None:
            self.filtered_df = self.df.copy()
        return self.filtered_df

    def add_to_history(self, query):
        """
        Adds query to history.

        Args:
            query (str): The query to add

        Returns:
            list: The updated history list
        """
        self.query_history.append(query)
        # Keep only the 20 most recent queries
        self.query_history = self.query_history[-20:]
        return self.query_history

    def get_history(self):
        """
        Returns query history.

        Returns:
            list: The history list
        """
        return self.query_history

    def process_query(self, query):
        """
        Processes a user query.

        Args:
            query (str): The query text

        Returns:
            tuple: (intent, columns) - the identified intent and columns
        """
        if self.df is None:
            raise ValueError("No data loaded")

        intent, columns = parse_query(query, self.df.columns)
        self.add_to_history(query)
        return intent, columns

    def sort_by(self, column, ascending=True):
        """
        Sorts the data by a column.

        Args:
            column (str): Column to sort by
            ascending (bool): Sort order (True for ascending)

        Returns:
            DataFrame: The sorted data
        """
        if self.df is None:
            raise ValueError("No data loaded")

        self.filtered_df = self.filtered_df.sort_values(by=column, ascending=ascending)
        return self.filtered_df
import pandas as pd
from intent_parser import parse_query
import json  # Import json for handling lists/dicts in SQLite

class FileProfile:
    """
    Represents a file profile, containing metadata about the file.
    """
    def __init__(self, file_name: str, columns: list, data_types: list, statistics: dict):
        self.file_name = file_name
        self.columns = columns
        self.data_types = data_types
        self.statistics = statistics

class AnalysisRecord:
    """
    Represents a record of a performed analysis.
    """
    def __init__(self, file_name: str, query: str, analysis_type: str, columns: list, settings: dict, results):
        self.file_name = file_name
        self.query = query
        self.analysis_type = analysis_type
        self.columns = columns
        self.settings = settings
        self.results = results

class DataModel:
    """
    Manages data operations and analysis history.
    """

    def __init__(self):
        self.df = None
        self.filtered_df = None
        self.query_history = []
        self.file_profiles = {}  # Dictionary to store FileProfiles
        self.analysis_history = []  # List to store AnalysisRecords

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads data from a CSV or Excel file.

        Args:
            file_path: The path to the file.

        Returns:
            The loaded DataFrame.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if file_path.endswith(".csv"):
            self.df = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            self.df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel.")

        self.filtered_df = self.df.copy()
        self.create_file_profile(file_path)  # Create profile after loading
        return self.df

    def create_file_profile(self, file_path: str) -> None:
        """
        Creates a FileProfile for the given file.

        Args:
            file_path: The path to the file.
        """
        file_name = file_path.split('/')[-1]
        columns = list(self.df.columns)
        data_types = [str(self.df[col].dtype) for col in columns]
        statistics = self.calculate_statistics()

        profile = FileProfile(file_name, columns, data_types, statistics)
        self.file_profiles[file_name] = profile

    def calculate_statistics(self) -> dict:
        """
        Calculates basic statistics for numeric columns.
        """
        statistics = {}
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                statistics[col] = {
                    "mean": self.df[col].mean(),
                    "median": self.df[col].median(),
                    "min": self.df[col].min(),
                    "max": self.df[col].max()
                }
        return statistics

    def add_analysis_record(self, record: AnalysisRecord) -> None:
        """
        Adds an AnalysisRecord to the analysis history.

        Args:
            record: The AnalysisRecord to add.
        """
        self.analysis_history.append(record)

    def get_file_profile(self, file_name: str) -> FileProfile:
        """
        Retrieves the FileProfile for a given file name.

        Args:
            file_name: The name of the file.

        Returns:
            The FileProfile, or None if not found.
        """
        return self.file_profiles.get(file_name)

    def apply_filter(self, column: str, filter_type: str, value) -> pd.DataFrame:
        """
        Applies a filter to the data.
        """
        if self.df is None:
            raise ValueError("No data loaded")

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        if filter_type == "greater":
            self.filtered_df = self.df[self.df[column] > value]
        elif filter_type == "less":
            self.filtered_df = self.df[self.df[column] < value]
        elif filter_type == "equal":
            self.filtered_df = self.df[self.df[column] == value]
        elif filter_type == "contains":
            self.filtered_df = self.df[self.df[column].astype(str).str.contains(value, case=False)]
        else:
            raise ValueError("Invalid filter type")

        return self.filtered_df

    def add_to_history(self, query: str) -> list:
        """
        Adds a query to the query history.
        """
        self.query_history.append(query)
        self.query_history = self.query_history[-20:]  # Keep last 20 queries
        return self.query_history

    def get_history(self) -> list:
        """
        Returns the query history.
        """
        return self.query_history

    def process_query(self, query: str) -> tuple:
        """
        Processes a user query to determine intent and columns.
        """
        if self.df is None:
            raise ValueError("No data loaded")

        intent, columns = parse_query(query, self.df.columns)
        self.add_to_history(query)
        return intent, columns

    def sort_by(self, column: str, ascending: bool = True) -> pd.DataFrame:
        """
        Sorts the data by the specified column.
        """
        if self.df is None:
            raise ValueError("No data loaded")

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        self.filtered_df = self.df.sort_values(by=column, ascending=ascending)
        return self.filtered_df

    def count_occurrences(self, conditions: dict) -> int:
        """
        Counts the number of rows that match the given conditions.

        Args:
            conditions: A dictionary where keys are column names and values are the
                        values to match in those columns.

        Returns:
            The number of rows that satisfy all conditions.
        """
        if self.df is None:
            raise ValueError("No data loaded")

        query_string = " & ".join([f"`{col}` == '{value}'" for col, value in conditions.items()])
        return len(self.df.query(query_string))
import pandas as pd
from Domain.data_loader import load_data
from Domain.data_model import DataModel
from data_access.file_profile_repository import FileProfileRepository  # Import the Repository
import json  # Import json for handling lists/dicts in SQLite


class FileProfile:  # Define the FileProfile class (can be moved to a separate file)
    def __init__(self, file_path, columns, data_types, statistics):
        self.file_path = file_path
        self.columns = columns
        self.data_types = data_types
        self.statistics = statistics


class FileProfileService:

    def __init__(self, data_model: DataModel, file_profile_repository: FileProfileRepository):  # Add the Repository
        self.data_model = data_model
        self.file_profile_repository = file_profile_repository  # Store the Repository

    def calculate_statistics(self, df: pd.DataFrame) -> dict:  # Change: Accepts DataFrame as argument
        """
        Calculates comprehensive statistics for each column in the DataFrame.

        Returns:
            dict: A dictionary where keys are column names and values are dictionaries
                  of statistics.
        """
        if df is None or df.empty:
            return {}  # Return empty dict if no DataFrame

        statistics = {}
        for col in df.columns:
            col_stats = {}
            col_type = df[col].dtype
            col_stats['type'] = str(col_type)  # Store column data type

            if pd.api.types.is_numeric_dtype(col_type):
                col_stats['mean'] = df[col].mean()
                col_stats['median'] = df[col].median()
                col_stats['min'] = df[col].min()
                col_stats['max'] = df[col].max()
                col_stats['std'] = df[col].std()
                col_stats['variance'] = df[col].var()

            col_stats['unique_count'] = df[col].nunique()
            col_stats['missing_count'] = df[col].isnull().sum()
            col_stats['mode'] = df[col].mode().tolist()

            if not pd.api.types.is_numeric_dtype(col_type):
                # Call count_occurrences through the data_model
                col_stats['value_counts'] = self.data_model.count_occurrences(
                    {col: df[col].tolist()}
                )

            statistics[col] = col_stats
        return statistics

    def create_file_profile(self, file_path: str) -> FileProfile:  # Change: Returns FileProfile
        """
        Creates a FileProfile for the given file.

        Args:
            file_path: The path to the file.
        """
        df = load_data(file_path)
        file_name = file_path.split('/')[-1]
        columns = list(df.columns)
        data_types = [str(df[col].dtype) for col in columns]
        statistics = self.calculate_statistics(df)

        file_profile = FileProfile(file_name, columns, data_types, statistics)
        self.file_profile_repository.save_file_profile(file_profile)  # Save the profile to the database
        return file_profile

    def get_file_profile(self, file_path: str) -> FileProfile:
        """
        Retrieves a FileProfile from the database.

        Args:
            file_path: The path to the file.

        Returns:
            FileProfile: The FileProfile object, or None if not found.
        """
        return self.file_profile_repository.get_file_profile(file_path)

    # Additional functions for saving, retrieving, comparing, etc. (if needed)
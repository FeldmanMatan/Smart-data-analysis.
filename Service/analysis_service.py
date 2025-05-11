from data_access.analysis_record_repository import AnalysisRecordRepository
import json


class AnalysisRecord:  # Define the AnalysisRecord class (can be moved to a separate file)
    def __init__(self, file_path: str, query: str, analysis_type: str, columns: list, settings: dict, results):
        self.file_path = file_path
        self.query = query
        self.analysis_type = analysis_type
        self.columns = columns
        self.settings = settings
        self.results = results


class AnalysisService:

    def __init__(self, analysis_record_repository: AnalysisRecordRepository):
        self.analysis_record_repository = analysis_record_repository

    def save_analysis_record(self, analysis_record: 'AnalysisRecord'):  # Use forward reference
        """
        Saves an AnalysisRecord to the database.

        Args:
            analysis_record: The AnalysisRecord object to save.
        """
        self.analysis_record_repository.save_analysis_record(analysis_record)

    def get_analysis_record(self, file_path: str, query: str) -> 'AnalysisRecord':  # Use forward reference
        """
        Retrieves an AnalysisRecord from the database.

        Args:
            file_path: The path to the file.
            query: The query used for the analysis.

        Returns:
            AnalysisRecord: The AnalysisRecord object, or None if not found.
        """
        return self.analysis_record_repository.get_analysis_record(file_path, query)

    def create_analysis_record(self, file_path: str, query: str, analysis_type: str, columns: list, settings: dict, results) -> 'AnalysisRecord':
        """
        Creates a new AnalysisRecord object.

        Args:
            file_path (str): The path to the file that was analyzed.
            query (str): The query that was used for the analysis.
            analysis_type (str): The type of analysis performed (e.g., "graph", "average").
            columns (list): The columns involved in the analysis.
            settings (dict): Any settings used for the analysis.
            results: The results of the analysis.

        Returns:
            AnalysisRecord: The newly created AnalysisRecord object.
        """
        analysis_record = AnalysisRecord(file_path, query, analysis_type, columns, settings, results)
        return analysis_record

    # Additional functions for retrieving, updating, deleting, etc. (if needed)
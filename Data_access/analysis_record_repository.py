from data_access.database_handler import DatabaseHandler
import json


class AnalysisRecordRepository:

    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def save_analysis_record(self, analysis_record: 'AnalysisRecord'):  # Use forward reference
        """
        Saves an AnalysisRecord to the database.

        Args:
            analysis_record: The AnalysisRecord object to save.
        """
        query = """
        INSERT INTO analysis_records (file_path, query, analysis_type, columns, settings, results)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            analysis_record.file_path,
            analysis_record.query,
            analysis_record.analysis_type,
            json.dumps(analysis_record.columns),
            json.dumps(analysis_record.settings),
            json.dumps(analysis_record.results)
        )
        self.db_handler.execute_query(query, values)

    def get_analysis_record(self, file_path: str, query: str) -> 'AnalysisRecord':  # Use forward reference
        """
        Retrieves an AnalysisRecord from the database.

        Args:
            file_path: The path to the file.
            query: The query used for the analysis.

        Returns:
            AnalysisRecord: The AnalysisRecord object, or None if not found.
        """
        query = "SELECT * FROM analysis_records WHERE file_path = ? AND query = ?"
        result = self.db_handler.execute_query(query, (file_path, query))
        if result:
            row = result[0]
            return AnalysisRecord(
                row[1],  # file_path
                row[2],  # query
                row[3],  # analysis_type
                json.loads(row[4]),  # columns
                json.loads(row[5]),  # settings
                json.loads(row[6])   # results
            )
        return None

    # Additional functions for retrieving, updating, deleting, etc. (if needed)
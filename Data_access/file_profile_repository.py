from data_access.database_handler import DatabaseHandler
import json


class FileProfileRepository:

    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def save_file_profile(self, file_profile: 'FileProfile'):  # Use forward reference for FileProfile
        """
        Saves a FileProfile to the database.

        Args:
            file_profile: The FileProfile object to save.
        """
        query = """
        INSERT INTO file_profiles (file_path, columns, data_types, statistics)
        VALUES (?, ?, ?, ?)
        """
        values = (
            file_profile.file_path,
            json.dumps(file_profile.columns),  # Use json.dumps to store lists/dicts
            json.dumps(file_profile.data_types),
            json.dumps(file_profile.statistics)
        )
        self.db_handler.execute_query(query, values)

    def get_file_profile(self, file_path: str) -> 'FileProfile':  # Use forward reference
        """
        Retrieves a FileProfile from the database.

        Args:
            file_path: The path to the file.

        Returns:
            FileProfile: The FileProfile object, or None if not found.
        """
        query = "SELECT * FROM file_profiles WHERE file_path = ?"
        result = self.db_handler.execute_query(query, (file_path,))
        if result:
            row = result[0]
            return FileProfile(
                row[1],  # file_path
                json.loads(row[2]),  # columns (load from JSON string)
                json.loads(row[3]),  # data_types (load from JSON string)
                json.loads(row[4])   # statistics (load from JSON string)
            )
        return None

    # פונקציות נוספות לעדכון ומחיקה (אם יש צורך)
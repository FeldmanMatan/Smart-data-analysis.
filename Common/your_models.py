
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
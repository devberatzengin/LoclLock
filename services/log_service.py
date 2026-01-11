from models.log import Log

class LogService:

    def __init__(self, storage_service):
        self.storage = storage_service

    def info(self, action: str, detail: str = ""):
        self._write(Log(id=None, level="INFO", action=action, message=detail))

    def warning(self, action: str, detail: str = ""):
        self._write(Log(id=None, level="WARNING", action=action, message=detail))

    def error(self, action: str, detail: str = ""):
        self._write(Log(id=None, level="ERROR", action=action, message=detail))

    def security(self, action: str, detail: str = ""):
        self._write(Log(id=None, level="SECURITY", action=action, message=detail))

    def _write(self, log: Log):
        query = """
        INSERT INTO logs (action, detail, level, created_at)
        VALUES (?, ?, ?, ?)
        """
        self.storage.execute(query, log.to_db_params(), commit=True)
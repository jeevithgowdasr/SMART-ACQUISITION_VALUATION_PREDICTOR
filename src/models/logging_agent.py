import json
import datetime
import os
from typing import Dict, Any, List


class LoggingAgent:
    def __init__(self):
        """
        Initialize LoggingAgent with no arguments.
        """
        self.logs: List[Dict[str, Any]] = []
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
    
    def log(self, entry_type: str, data: Dict[str, Any]) -> None:
        """
        Log an entry with type, data, and timestamp.
        
        Args:
            entry_type: Type of log entry (e.g., "input", "features", "prediction")
            data: Data to log
        """
        # Validate entry_type
        if not isinstance(entry_type, str) or len(entry_type) == 0:
            entry_type = "unknown"
        
        # Validate data
        if not isinstance(data, dict):
            data = {"value": str(data)}
        
        # Generate timestamp
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Create log entry
        log_entry = {
            "type": entry_type,
            "data": data,
            "timestamp": timestamp
        }
        
        # Append to in-memory logs
        self.logs.append(log_entry)
        
        # Append to persistent file
        try:
            with open("logs/app_logs.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            # Silently continue if file writing fails
            pass
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """
        Get all in-memory log entries.
        
        Returns:
            List of all log entries
        """
        return self.logs.copy()
    
    @staticmethod
    def load() -> 'LoggingAgent':
        """
        Static method to create and return a LoggingAgent instance.
        
        Returns:
            LoggingAgent: A new LoggingAgent instance
        """
        return LoggingAgent()
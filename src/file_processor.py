import re
from pathlib import Path

class FileProcessor:
    """Handles the core logic for processing files"""
        
    def _parse_number_file(self, file_path: Path) -> list[str]:
        if not file_path or not file_path.exists():
            return []
        
        try:
            content = file_path.read_text()
            numbers = [num for num in re.split(r'[,\s]+', content) if num]
            return numbers
        except Exception as e:
            return []
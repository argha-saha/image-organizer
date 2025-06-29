import logging
import re
import shutil
from pathlib import Path

class FileProcessor:
    """Handles the core logic for processing files"""
        
    def _parse_number_file(self, file_path: Path) -> list[str]:
        """Extracts numbers from a file."""
        
        if not file_path or not file_path.exists():
            return []
        
        try:
            content = file_path.read_text()
            # Split the content by commas or whitespace
            numbers = [num for num in re.split(r'[,\s]+', content) if num]
            return numbers
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return []
        
    
    def process(
        self,
        operation_type: str,
        source_folder: str,
        destination_folder: str,
        prefix: str,
        extension: str,
        number_file: str
    ) -> bool:
        """Organizes files based on the parameters."""
        
        source_dir = Path(source_folder)
        destination_dir = Path(destination_folder)
        number_file_path = Path(number_file)
        
        if not source_dir.is_dir() or not destination_dir.is_dir() or not number_file_path.is_file():
            logging.error("Invalid input, output folder, or number list file path.")
            return False
        
        numbers = self._parse_number_file(number_file_path)
        if not numbers:
            logging.error("No valid numbers found in the number list file.")
            return False
        
        success_count = 0
        fail_count = 0
        
        for num in numbers:
            ext = f".{extension.lstrip('.')}" if extension else ''
            filename = f"{prefix}{num}{ext}"
            src_path = source_dir / filename
            dest_path = destination_dir / filename
            
            if src_path.exists():
                try:
                    if operation_type == 'copy':
                        shutil.copy2(src_path, dest_path)
                        logging.info(f"Copied {src_path} to {dest_path}")
                    elif operation_type == 'move':
                        shutil.move(src_path, dest_path)
                        logging.info(f"Moved {src_path} to {dest_path}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"Error processing {src_path}: {e}")
                    fail_count += 1
            else:
                logging.warning(f"File {src_path} does not exist.")
                fail_count += 1
            
        logging.info(f"SUMMARY: Success: {success_count}, Failures: {fail_count}")
        return True
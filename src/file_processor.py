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
        
        
    def get_files_to_process(self, source_folder, prefix, extension, number_file, destination_folder=None):
        found = []
        missing = []
        overwrite = []
        source_dir = Path(source_folder)
        number_file_path = Path(number_file)
        dest_dir = Path(destination_folder) if destination_folder else None
        
        if not source_dir.is_dir() or not number_file_path.is_file():
            return found, missing, overwrite
        
        with open(number_file_path, 'r') as f:
            numbers = [num for num in re.split(r'[\s,]+', f.read()) if num]
        
        ext = f".{extension.lstrip('.')}" if extension else ''
        for num in numbers:
            filename = f"{prefix}{num}{ext}"
            file_path = source_dir / filename
            if file_path.exists():
                found.append(str(file_path))
                # Check for overwrite if destination_folder is provided
                if dest_dir and (dest_dir / filename).exists():
                    overwrite.append(str(dest_dir / filename))
            else:
                missing.append(str(file_path))
        return found, missing, overwrite
    
    
    def process(
        self,
        operation_type: str,
        source_folder: str,
        destination_folder: str,
        prefix: str,
        extension: str,
        number_file: str,
        progress_callback=None
    ) -> int:
        """Organizes files based on the parameters. Returns the number of files successfully processed."""
        
        source_dir = Path(source_folder)
        destination_dir = Path(destination_folder)
        number_file_path = Path(number_file)
        
        if not source_dir.is_dir() or (operation_type != 'delete' and not destination_dir.is_dir()) or not number_file_path.is_file():
            logging.error("Invalid input, output folder, or number list file path.")
            return 0
        
        numbers = self._parse_number_file(number_file_path)
        if not numbers:
            logging.error("No valid numbers found in the number list file.")
            return 0
        
        success_count = 0
        fail_count = 0
        
        for idx, num in enumerate(numbers, 1):
            ext = f".{extension.lstrip('.')}" if extension else ''
            filename = f"{prefix}{num}{ext}"
            src_path = source_dir / filename
            dest_path = destination_dir / filename
            
            if operation_type == 'delete':
                if src_path.exists():
                    try:
                        src_path.unlink()
                        logging.info(f"Deleted {src_path}")
                        success_count += 1
                    except Exception as e:
                        logging.error(f"Error deleting {src_path}: {e}")
                        fail_count += 1
                else:
                    logging.warning(f"File {src_path} does not exist.")
                    fail_count += 1
            elif operation_type == 'rename':
                # For renaming, destination_folder is used as the new prefix
                new_filename = f"{destination_folder}{num}{ext}"
                new_path = source_dir / new_filename
                
                if src_path.exists():
                    try:
                        src_path.rename(new_path)
                        logging.info(f"Renamed {src_path} to {new_path}")
                        success_count += 1
                    except Exception as e:
                        logging.error(f"Error renaming {src_path}: {e}")
                        fail_count += 1
                else:
                    logging.warning(f"File {src_path} does not exist.")
                    fail_count += 1
            else:
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
            
            if progress_callback:
                progress_callback(idx)
            
        logging.info(f"SUMMARY: Success: {success_count}, Failures: {fail_count}")
        return success_count
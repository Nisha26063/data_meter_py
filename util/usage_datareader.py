from model.usage_record import UsageRecord
from typing import List, Iterator
import re
from exceptions import DataProcessingException

class UsageDataReader:
    # util/usage_datareader.py
    @staticmethod
    def read_file(file_path: str) -> List[UsageRecord]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return list(UsageDataReader.generate_records(file))
        except FileNotFoundError as e:
            raise DataProcessingException(f"File not found: {file_path}") from e
    @staticmethod
    def generate_records(file: Iterator[str]) -> Iterator[UsageRecord]:
        """Generator that yields UsageRecords from file lines."""
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            parts = re.split(r'\s*\|\s*', line.strip())
            if len(parts) != 5:
                continue
                
            try:
                g4 = 0 if parts[2].lower() == 'o' else int(parts[2])
                g5 = 0 if parts[3].lower() == 'o' else int(parts[3])
                roaming = parts[4].lower() == 'yes'
                
                yield UsageRecord(
                    mobile_number=parts[0],
                    g4_usage=g4,
                    g5_usage=g5,
                    is_roaming=roaming
                )
            except (ValueError, IndexError) as e:
                print(f"Skipping invalid record: {line} ({str(e)})")
                continue
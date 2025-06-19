from collections import defaultdict
from exceptions import DataProcessingException
from model.user_data import UserData
from model.usage_record import UsageRecord

class DataProcessor:
    def __init__(self):
        self._user_map = {}

    def process_record(self, record: UsageRecord) -> None:
    
        try:
            if not isinstance(record, UsageRecord):
                raise DataProcessingException("Invalid record type")
                
            mobile = str(record.mobile_number).strip()
            if mobile not in self._user_map:
                self._user_map[mobile] = UserData(mobile_number=mobile)
            self._user_map[mobile].add_usage(record)
        except Exception as e:
            raise DataProcessingException(f"Invalid record: {str(e)}") from e

    def get_user_data(self) -> dict[str, UserData]:
        """Return a copy of the processed user data."""
        return dict(self._user_map)

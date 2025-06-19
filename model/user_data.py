from exceptions import InvalidArgumentError
from model.usage_record import UsageRecord

class UserData:
    def __init__(self, mobile_number: str):
        self._mobile_number = mobile_number
        self._g4_home = 0
        self._g5_home = 0
        self._g4_roaming = 0
        self._g5_roaming = 0

    def add_usage(self, record: UsageRecord) -> None:
        """Add usage data from a record."""
        #print(f"DEBUG: self.mobile_number = '{self.mobile_number}', record.mobile_number = '{record.mobile_number}'")
        if self._mobile_number != record.mobile_number:  # Direct attribute access
            raise InvalidArgumentError("Mobile number mismatch")
        
        # Direct attribute access for usage values
        if record.is_roaming:
            self._g4_roaming += record.g4_usage
            self._g5_roaming += record.g5_usage
        else:
            self._g4_home += record.g4_usage
            self._g5_home += record.g5_usage

    # Property accessors for internal state
    @property
    def mobile_number(self) -> str:
        return self._mobile_number
    
    @property
    def g4_home(self) -> int:
        return self._g4_home
    
    @property
    def g5_home(self) -> int:
        return self._g5_home
    
    @property
    def g4_roaming(self) -> int:
        return self._g4_roaming
    
    @property
    def g5_roaming(self) -> int:
        return self._g5_roaming
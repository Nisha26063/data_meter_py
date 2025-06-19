from dataclasses import dataclass
from exceptions import InvalidArgumentError

@dataclass
class UsageRecord:
    
    mobile_number: str  
    g4_usage: int       
    g5_usage: int       
    is_roaming: bool    

    def __post_init__(self):
        # Validation
        if not (self.mobile_number and self.mobile_number.isdigit() and len(self.mobile_number) == 10):
            raise InvalidArgumentError("Mobile number must be 10 digits")
        if self.g4_usage < 0 or self.g5_usage < 0:
            raise InvalidArgumentError("Usage values cannot be negative")

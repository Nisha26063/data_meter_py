from configparser import ConfigParser
from exceptions import BillingException
from model.user_data import UserData

class BillingService:
    def __init__(self, config: ConfigParser) -> None:
        """Initialize with validated rates from config."""
        self.g4_rate = config.getfloat('DEFAULT', 'g4.rate')
        self.g5_rate = config.getfloat('DEFAULT', 'g5.rate')
        self.roaming_g4_multiplier = config.getfloat('DEFAULT', 'roaming.g4.multiplier')
        self.roaming_g5_multiplier = config.getfloat('DEFAULT', 'roaming.g5.multiplier')
        self.overage_multiplier = config.getfloat('DEFAULT', 'overage.multiplier')
        self.overage_threshold = config.getfloat('DEFAULT', 'overage.threshold')

    def calculate_bill(self, user: UserData) -> float:
        """Calculate total bill with roaming and overage charges."""
        try:
            home_charge = (user.g4_home * self.g4_rate) + (user.g5_home * self.g5_rate)
            roaming_charge = (
                (user.g4_roaming * self.g4_rate * self.roaming_g4_multiplier) +
                (user.g5_roaming * self.g5_rate * self.roaming_g5_multiplier)
            )
            total = home_charge + roaming_charge
            
            if self._total_usage(user) > self.overage_threshold:
                total *= self.overage_multiplier
                
            return round(total, 2)
            
        except (ValueError, TypeError) as e:
            raise BillingException("Invalid billing calculation") from e

    def _total_usage(self, user: UserData) -> int:
        """Helper method to calculate total usage in MB."""
        return user.g4_home + user.g5_home + user.g4_roaming + user.g5_roaming
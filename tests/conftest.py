import pytest
from configparser import ConfigParser
from model.usage_record import UsageRecord
from model.user_data import UserData

@pytest.fixture
def sample_config():
    """Fixture providing a sample configuration"""
    config = ConfigParser()
    config['DEFAULT'] = {
        'g4.rate': '0.05',
        'g5.rate': '0.08',
        'roaming.g4.multiplier': '1.10',
        'roaming.g5.multiplier': '1.15',
        'overage.multiplier': '1.05',
        'overage.threshold': '1000000'
    }
    return config

@pytest.fixture
def sample_usage_record():
    """Fixture providing a sample UsageRecord"""
    return UsageRecord(
        mobile_number="9000600600",
        g4_usage=1000,
        g5_usage=2000,
        is_roaming=False
    )

@pytest.fixture
def sample_user_data():
    """Fixture providing sample UserData with pre-populated usage"""
    user = UserData("9000600600")
    user.add_usage(UsageRecord("9000600600", 1000, 2000, False))
    user.add_usage(UsageRecord("9000600600", 500, 1000, True))
    return user
import pytest
from exceptions import InvalidArgumentError
from model.usage_record import UsageRecord
from model.user_data import UserData

class TestUserData:
    def test_add_home_usage(self):
        """Test adding home usage"""
        user = UserData("9000600600")
        record = UsageRecord("9000600600", 1000, 2000, False)
        user.add_usage(record)
        assert user.g4_home == 1000
        assert user.g5_home == 2000
        assert user.g4_roaming == 0
        assert user.g5_roaming == 0

    def test_add_roaming_usage(self):
        """Test adding roaming usage"""
        user = UserData("9000600600")
        record = UsageRecord("9000600600", 500, 1000, True)
        user.add_usage(record)
        assert user.g4_home == 0
        assert user.g5_home == 0
        assert user.g4_roaming == 500
        assert user.g5_roaming == 1000

    def test_mobile_number_mismatch(self):
        """Test adding usage for wrong mobile number"""
        user = UserData("9000600600")
        record = UsageRecord("9000600601", 1000, 2000, False)
        with pytest.raises(InvalidArgumentError):
            user.add_usage(record)

    def test_accumulate_usage(self):
        """Test usage accumulation across multiple records"""
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 1000, 2000, False))
        user.add_usage(UsageRecord("9000600600", 500, 1000, True))
        user.add_usage(UsageRecord("9000600600", 2000, 3000, False))
        
        assert user.g4_home == 3000
        assert user.g5_home == 5000
        assert user.g4_roaming == 500
        assert user.g5_roaming == 1000
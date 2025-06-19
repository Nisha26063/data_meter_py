import pytest
from exceptions import InvalidArgumentError
from model.usage_record import UsageRecord

class TestUsageRecord:
    def test_valid_record_creation(self):
        """Test creating a valid usage record"""
        record = UsageRecord("9000600600", 1000, 2000, False)
        assert record.mobile_number == "9000600600"
        assert record.g4_usage == 1000
        assert record.g5_usage == 2000
        assert record.is_roaming is False

    @pytest.mark.parametrize("number", ["123", "", "90006006001", "ABCDEFGHIJ"])
    def test_invalid_mobile_numbers(self, number):
        """Test invalid mobile number formats"""
        with pytest.raises(InvalidArgumentError):
            UsageRecord(number, 1000, 2000, False)

    def test_negative_usage(self):
        """Test negative usage values"""
        with pytest.raises(InvalidArgumentError):
            UsageRecord("9000600600", -100, 200, False)
        with pytest.raises(InvalidArgumentError):
            UsageRecord("9000600600", 100, -200, False)

    def test_zero_usage(self):
        """Test zero usage values are allowed"""
        record = UsageRecord("9000600600", 0, 0, False)
        assert record.g4_usage == 0
        assert record.g5_usage == 0
import pytest
from model.usage_record import UsageRecord
from service.data_processor import DataProcessor
from exceptions import DataProcessingException

class TestDataProcessor:
    def test_process_valid_record(self):
        """Test processing a valid record"""
        processor = DataProcessor()
        record = UsageRecord("9000600600", 1000, 2000, False)
        processor.process_record(record)
        
        user_data = processor.get_user_data()
        assert "9000600600" in user_data
        assert user_data["9000600600"].g4_home == 1000
        assert user_data["9000600600"].g5_home == 2000

    # tests/test_service/test_data_processor.py
    def test_process_invalid_record(self):
        processor = DataProcessor()
        with pytest.raises(DataProcessingException):
            processor.process_record(None)  # Test with None instead of string
    def test_accumulate_records(self):
        """Test record accumulation"""
        processor = DataProcessor()
        processor.process_record(UsageRecord("9000600600", 1000, 2000, False))
        processor.process_record(UsageRecord("9000600600", 500, 1000, True))
        
        user = processor.get_user_data()["9000600600"]
        assert user.g4_home == 1000
        assert user.g5_home == 2000
        assert user.g4_roaming == 500
        assert user.g5_roaming == 1000

    def test_multiple_users(self):
        """Test handling multiple users"""
        processor = DataProcessor()
        processor.process_record(UsageRecord("9000600600", 1000, 2000, False))
        processor.process_record(UsageRecord("9000600601", 500, 1000, True))
        
        user_data = processor.get_user_data()
        assert len(user_data) == 2
        assert "9000600600" in user_data
        assert "9000600601" in user_data
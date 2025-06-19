import pytest
import os
import tempfile
from util.usage_datareader import UsageDataReader
from exceptions import DataProcessingException

class TestUsageDataReader:
    def test_read_valid_file(self):
        """Test reading a valid input file"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("9000600600|TOWER1|1000|2000|No\n")
            tmp.write("9000600601|TOWER2|500|1000|Yes\n")
            tmp_path = tmp.name
        
        try:
            records = UsageDataReader.read_file(tmp_path)
            assert len(records) == 2
            assert records[0].mobile_number == "9000600600"
            assert records[1].mobile_number == "9000600601"
            assert records[1].is_roaming is True
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_skip_invalid_lines(self):
        """Test handling invalid lines"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("invalid|data|format\n")
            tmp.write("9000600600|TOWER1|1000|2000|No\n")
            tmp_path = tmp.name
        
        try:
            records = UsageDataReader.read_file(tmp_path)
            assert len(records) == 1
            assert records[0].mobile_number == "9000600600"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_file_not_found(self):
        """Test handling missing files"""
        with pytest.raises(DataProcessingException):
            UsageDataReader.read_file("nonexistent_file.txt")
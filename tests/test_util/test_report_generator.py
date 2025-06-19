import pytest
import os
import tempfile
from model.user_data import UserData
from model.usage_record import UsageRecord
from service.billing_service import BillingService
from util.report_generator import ReportGenerator
from configparser import ConfigParser

class TestReportGenerator:
    def test_generate_report(self, sample_config):
        """Test report generation"""
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 10000, 20000, False))
        user_data = {"9000600600": user}
        
        billing_service = BillingService(sample_config)
        generator = ReportGenerator()
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            output_path = tmp.name
        
        try:
            generator.generate_report(
                output_path=output_path,
                user_data=user_data,
                billing_service=billing_service
            )
            
            with open(output_path, 'r') as f:
                content = f.read()
                assert "9000600600" in content
                assert "10000" in content
                assert "20000" in content
                assert "2100.00" in content
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


    
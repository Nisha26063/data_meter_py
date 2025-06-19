import pytest
from model.user_data import UserData
from model.usage_record import UsageRecord
from service.billing_service import BillingService

class TestBillingService:
    def test_home_usage_only(self, sample_config):
        """Test billing for home usage only"""
        service = BillingService(sample_config)
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 10000, 20000, False))
        
        # 10000*0.05 + 20000*0.08 = 500 + 1600 = 2100.00
        assert service.calculate_bill(user) == 2100.00

    def test_with_roaming_surcharge(self, sample_config):
        """Test roaming surcharges"""
        service = BillingService(sample_config)
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 10000, 0, False))  # Home
        user.add_usage(UsageRecord("9000600600", 0, 10000, True))   # Roaming
        
        # 10000*0.05 + (10000*0.08*1.15) = 500 + 920 = 1420.00
        assert service.calculate_bill(user) == 1420.00

    def test_overage_charge(self, sample_config):
        """Test overage charges"""
        service = BillingService(sample_config)
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 1000001, 0, False))
        
        # (1000001*0.05)*1.05 = 52500.0525
        assert service.calculate_bill(user) == pytest.approx(52500.05, 0.01)

    def test_exact_threshold(self, sample_config):
        """Test usage exactly at threshold"""
        service = BillingService(sample_config)
        user = UserData("9000600600")
        user.add_usage(UsageRecord("9000600600", 1000000, 0, False))
        
        # 1000000*0.05 = 50000.00 (no overage)
        assert service.calculate_bill(user) == 50000.00
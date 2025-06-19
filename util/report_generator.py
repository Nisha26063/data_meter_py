import csv
import logging
from pathlib import Path
from typing import Dict
from model.user_data import UserData
from service import BillingService
from exceptions import BillingException

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ReportGenerator:
       
    def generate_report(
        self,
        output_path: str,
        user_data: Dict[str, UserData],
        billing_service: BillingService,
        delimiter: str = "|"
    ) -> None:
        """
        Generates a detailed billing report in CSV format.
        
        """
        try:
            # Create parent directories if needed
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)
                
                # Write header
                writer.writerow([
                    "Mobile Number", 
                    "4G (MB)", 
                    "5G (MB)", 
                    "4G Roaming (MB)", 
                    "5G Roaming (MB)", 
                    "Cost ($)"
                ])
                
                # Process each user
                for mobile_number, user in user_data.items():
                    try:
                        cost = billing_service.calculate_bill(user)
                        writer.writerow([
                            mobile_number,
                            user.g4_home,
                            user.g5_home,
                            user.g4_roaming,
                            user.g5_roaming,
                            f"{cost:.2f}"
                        ])
                    except BillingException as e:
                        logger.warning(
                            f"Skipping invalid billing for {mobile_number}: {str(e)}"
                        )
                        writer.writerow([
                            mobile_number,
                            user.g4_home,
                            user.g5_home,
                            user.g4_roaming,
                            user.g5_roaming,
                            "ERROR"
                        ])
                        
        except IOError as e:
            logger.error(f"Failed to write report to {output_path}")
            raise IOError(f"Report generation failed for {output_path}") from e
        except Exception as e:
            logger.error(f"Unexpected error during report generation: {str(e)}")
            raise ValueError("Invalid report data") from e
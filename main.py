import configparser
from model.usage_record import UsageRecord
from service.data_processor import DataProcessor
from service.billing_service import BillingService
from util.report_generator import ReportGenerator
from util.usage_datareader import UsageDataReader
from exceptions import DataProcessingException
import logging

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config = configparser.ConfigParser()
        files=config.read('resources/config.ini')  # Python typically uses .ini instead of .properties
        print("Files read:", files)
        # Initialize services
        processor = DataProcessor()
        billing_service = BillingService(config)
        usage_data_reader = UsageDataReader()
        report_generator = ReportGenerator()

        # Process input files
        records = usage_data_reader.read_file("input/data.txt")
        for record in records:
            try:
                processor.process_record(record)
            except DataProcessingException as e:
                logger.error(f"Failed to process record: {str(e)}", exc_info=True)

        # Generate report
        report_generator.generate_report(
            output_path="output/report.txt",
            user_data=processor.get_user_data(),
            billing_service=billing_service
        )

        logger.info("Report generated successfully!")

    except IOError as e:
        logger.error(f"I/O error occurred: {str(e)}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
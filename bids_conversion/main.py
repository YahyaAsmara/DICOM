from src.converter import DicomConverter
from src.validator import ConfigValidator
import logging
import sys

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conversion.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Paths
    config_path = 'config/config.json'
    dicom_dir = 'data/raw_dicoms'
    output_dir = 'data/bids_output'
    
    # Validate configuration
    logger.info("Validating configuration")
    validator = ConfigValidator(config_path)
    issues = validator.validate()
    
    if issues:
        logger.error("Configuration validation failed:")
        for issue in issues:
            logger.error(f"- {issue}")
        return
    
    # Initialize converter
    converter = DicomConverter(
        config_path=config_path,
        dicom_dir=dicom_dir,
        output_dir=output_dir
    )
    
    # Convert subjects
    subjects = ['sub-01']  # Add more subjects as needed
    for subject in subjects:
        try:
            converter.convert_subject(subject)
        except Exception as e:
            logger.error(f"Error processing subject {subject}: {str(e)}")

if __name__ == "__main__":
    main()

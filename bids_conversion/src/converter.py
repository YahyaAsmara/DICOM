from pathlib import Path
import subprocess
import json
import logging

class DicomConverter:
    def __init__(self, config_path, dicom_dir, output_dir):
        self.config_path = Path(config_path)
        self.dicom_dir = Path(dicom_dir)
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(__name__)
        
        self.setup_logging()
        self.validate_paths()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def validate_paths(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        if not self.dicom_dir.exists():
            raise FileNotFoundError(f"DICOM directory not found: {self.dicom_dir}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def convert_subject(self, subject_id, session=None):
        self.logger.info(f"Converting subject: {subject_id}")
        cmd = [
            'dcm2bids',
            '-d', str(self.dicom_dir),
            '-p', subject_id,
            '-c', str(self.config_path),
            '-o', str(self.output_dir)
        ]
        if session:
            cmd.extend(['-s', session])
        
        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"Successfully converted data for subject {subject_id}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error converting subject {subject_id}: {str(e)}")
            raise
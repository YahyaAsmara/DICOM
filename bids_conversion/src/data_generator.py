import os
from pathlib import Path
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
import datetime
import numpy as np

class DicomDataGenerator:
    def __init__(self, base_path):
        """
        Initialize the DICOM data generator
        
        Args:
            base_path (str): Base directory for generating data
        """
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / 'raw_dicoms'
        self.bids_path = self.base_path / 'bids_output'
        
    def setup_directories(self):
        """Create the basic directory structure"""
        # Create main directories
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.bids_path.mkdir(parents=True, exist_ok=True)
        
    def create_sample_dicom(self, path, series_desc, patient_name, study_date=None):
        """
        Create a sample DICOM file
        
        Args:
            path (Path): Output path for the DICOM file
            series_desc (str): Series description
            patient_name (str): Patient name
            study_date (str): Study date (YYYYMMDD)
        """
        # File meta info dataset
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = '1.2.3'
        file_meta.ImplementationClassUID = '1.2.3.4'
        
        # Main dataset
        ds = FileDataset(path, {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        # Add required DICOM fields
        ds.PatientName = patient_name
        ds.PatientID = f"ID_{patient_name.split('^')[0]}"
        ds.StudyDate = study_date or datetime.datetime.now().strftime('%Y%m%d')
        ds.SeriesDescription = series_desc
        ds.Modality = 'MR'
        ds.SeriesNumber = '1'
        
        # Create a small fake image
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.Rows = 16
        ds.Columns = 16
        ds.BitsStored = 16
        ds.BitsAllocated = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.PixelData = np.zeros((16, 16), dtype=np.uint16).tobytes()
        
        # Save the file
        ds.save_as(path, write_like_original=False)
        
    def generate_subject_data(self, subject_id, num_sessions=1):
        """
        Generate complete subject data
        
        Args:
            subject_id (str): Subject identifier
            num_sessions (int): Number of sessions to generate
        """
        subject_dir = self.raw_path / f'sub-{subject_id}'
        
        # Sample scan parameters
        scan_types = [
            ('T1_SAG', 'Sagittal T1-weighted'),
            ('T1_AX', 'Axial T1-weighted'),
            ('T2_SAG', 'Sagittal T2-weighted'),
            ('T2_AX', 'Axial T2-weighted'),
            ('PD_SAG', 'Sagittal PD-weighted'),
            ('PD_AX', 'Axial PD-weighted')
        ]
        
        for session in range(1, num_sessions + 1):
            session_dir = subject_dir / f'ses-{session:02d}'
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate a unique study date for each session
            study_date = (datetime.datetime.now() - 
                         datetime.timedelta(days=session)).strftime('%Y%m%d')
            
            # Create DICOM files for each scan type
            for idx, (scan_type, desc) in enumerate(scan_types, 1):
                scan_dir = session_dir / f'scan_{idx:02d}'
                scan_dir.mkdir(exist_ok=True)
                
                # Create multiple DICOM files per scan
                for slice_idx in range(1, 4):  # 3 slices per scan
                    dicom_path = scan_dir / f'slice_{slice_idx:02d}.dcm'
                    self.create_sample_dicom(
                        dicom_path,
                        series_desc=scan_type,
                        patient_name=f'TEST^Subject{subject_id}',
                        study_date=study_date
                    )

def main():
    """Main function to generate sample data"""
    # Initialize generator
    generator = DicomDataGenerator('data')
    
    # Setup directory structure
    generator.setup_directories()
    
    # Generate data for multiple subjects
    for subject_id in range(1, 4):  # 3 subjects
        print(f"Generating data for subject {subject_id}")
        generator.generate_subject_data(
            subject_id=f'{subject_id:02d}',
            num_sessions=2  # 2 sessions per subject
        )
        
    print("\nSample data generation complete!")
    print("\nDirectory structure:")
    os.system('tree data')

if __name__ == "__main__":
    main()
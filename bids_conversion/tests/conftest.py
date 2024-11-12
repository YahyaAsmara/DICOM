import pytest
import json
import tempfile
from pathlib import Path
import shutil
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset

@pytest.fixture
def sample_config():
    return {
        "searchMethod": "re",
        "descriptions": [
            {
                "dataType": "anat",
                "criteria": {
                    "SeriesDescription": "((?=T1).+SAG|(?=SAG).+T1)"
                },
                "modalityLabel": "acq-sag_T1"
            },
            {
                "dataType": "anat",
                "criteria": {
                    "SeriesDescription": "((?=T2).+AX|(?=AX).+T2)"
                },
                "modalityLabel": "acq-axial_T2"
            }
        ]
    }

@pytest.fixture
def config_file(tmp_path, sample_config):
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as f:
        json.dump(sample_config, f)
    return config_path

@pytest.fixture
def sample_dicom(tmp_path):
    """Create a sample DICOM file"""
    dicom_path = tmp_path / "sample.dcm"
    
    # Create minimal DICOM dataset
    file_meta = FileMetaDataset()
    ds = FileDataset(dicom_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    
    # Add required DICOM fields
    ds.PatientName = "Test^Patient"
    ds.SeriesDescription = "T1_SAG"
    ds.StudyDate = "20240101"
    
    ds.save_as(dicom_path)
    return dicom_path

@pytest.fixture
def dicom_directory(tmp_path, sample_dicom):
    """Create a sample DICOM directory structure"""
    dicom_dir = tmp_path / "raw_dicoms"
    sub_dir = dicom_dir / "sub-01" / "ses-01"
    sub_dir.mkdir(parents=True)
    
    # Copy sample DICOM to subject directory
    shutil.copy(sample_dicom, sub_dir / "sample.dcm")
    return dicom_dir
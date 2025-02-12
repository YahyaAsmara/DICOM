from pathlib import Path
import boto3
import json
import pandas as pd
from src.converter import DicomConverter
from src.validator import ConfigValidator
import streamlit as st
import pydicom
import logging

class AWSDicomVisualizer:
    def __init__(self, bucket_name, region='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')
        self.athena = boto3.client('athena')
        self.logger = logging.getLogger(__name__)
        
    def process_dicom_data(self, dicom_dir, config_path):
        """
        Process DICOM data using your existing converter
        and upload metadata to AWS
        """
        # Use your existing converter
        converter = DicomConverter(
            config_path=config_path,
            dicom_dir=dicom_dir,
            output_dir='data/bids_output'
        )
        
        # Extract metadata for visualization
        metadata = []
        dicom_path = Path(dicom_dir)
        
        for dcm_file in dicom_path.glob('**/*.dcm'):
            ds = pydicom.dcmread(dcm_file, stop_before_pixels=True)
            metadata.append({
                'subject_id': ds.PatientID,
                'study_date': ds.StudyDate,
                'series_desc': ds.SeriesDescription,
                'modality': ds.Modality,
                'file_path': str(dcm_file)
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(metadata)
        
        # Upload to S3
        csv_buffer = df.to_csv(index=False).encode()
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key='processed_data/dicom_metadata.csv',
            Body=csv_buffer
        )
        
        return df

def create_streamlit_app():
    """
    Create Streamlit visualization app
    """
    st.title("DICOM Data Visualization")
    
    # Initialize AWS connection
    visualizer = AWSDicomVisualizer('your-bucket-name')
    
    # Query Athena for data
    query = """
    SELECT 
        subject_id,
        series_desc,
        COUNT(*) as scan_count
    FROM dicom_database.dicom_metadata
    GROUP BY subject_id, series_desc
    """
    
    # Execute query and get results
    response = visualizer.athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': 's3://your-bucket-name/athena_results/'
        }
    )
    
    # Display visualizations
    st.header("Scan Distribution by Subject")
    # Add visualization code here using st.bar_chart(), st.line_chart(), etc.
    
    st.header("Series Types Overview")
    # Add more visualizations

if __name__ == "__main__":
    create_streamlit_app()

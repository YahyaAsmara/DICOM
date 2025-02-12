# DICOM to NIfTI Converter with AWS Visualization

This project converts DICOM files to NIfTI format and provides visualization capabilities using AWS services.

## Basic Setup (DICOM Conversion)

### Step 1: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 2: Generate Sample Data
```bash
python data_generator.py
```
Generated data will be in: `data/raw_dicoms`

### Step 3: Run Converter
```bash
python main.py
```
Converted data will be in: `data/bids_output`

## AWS Visualization Setup (for Beginners)

### Step 1: AWS Account Setup
1. Create an AWS account if you don't have one
   - Go to aws.amazon.com
   - Click "Create an AWS Account"
   - Follow the sign-up process
   - ⚠️ You'll need a credit card, but there's a free tier

### Step 2: Install AWS Tools
```bash
pip install boto3 streamlit
```

### Step 3: Set Up AWS Credentials
1. Get your AWS credentials
   - Log into AWS Console
   - Click your name in top right
   - Click "Security credentials"
   - Create new access key
   - ⚠️ Save both the Access Key ID and Secret Access Key

2. Set up credentials on your computer
```bash
# Option 1: Set environment variables
export AWS_ACCESS_KEY_ID='your-key-here'
export AWS_SECRET_ACCESS_KEY='your-secret-here'

# Option 2: Create AWS credentials file
mkdir ~/.aws
touch ~/.aws/credentials
```
Then add to credentials file:
```
[default]
aws_access_key_id = your-key-here
aws_secret_access_key = your-secret-here
```

### Step 4: Run the Visualization
```bash
streamlit run visualization_app.py
```
Then open your browser to: `http://localhost:8501`

## How It All Works (Simple Version)

```
Step 1: DICOM Processing
Your DICOM Files → Convert to NIfTI → Save Locally

Step 2: AWS Storage
Local Files → Upload to AWS → Safe Storage in the Cloud

Step 3: Visualization
Cloud Data → Process → Show Pretty Charts
```

## Common Issues & Solutions

1. "AWS credentials not found"
   - Double-check your credentials are set up correctly
   - Make sure you copied the full key/secret

2. "Cannot connect to AWS"
   - Check your internet connection
   - Verify your AWS account is active

3. "Visualization not showing"
   - Make sure Streamlit is running
   - Check if your browser blocked the page

## Cost Management (Important!)

To keep AWS costs low:
1. Use small sample data when testing
2. Delete unused AWS resources
3. Monitor your AWS billing dashboard
4. Set up billing alerts in AWS console

## Need Help?

1. For DICOM conversion issues:
   - Check the conversion.log file
   - Verify your DICOM files are valid

2. For AWS issues:
   - Check AWS Console for error messages
   - Verify your permissions are correct

3. For visualization issues:
   - Check Streamlit console output
   - Verify data was uploaded to AWS

## Data Flow Diagram

```
DICOM Files
    ↓
Data Generator
    ↓
Converter
    ↓
AWS Upload
    ↓
Visualization
```

⚠️ Remember: Always be careful with medical data and follow proper data privacy procedures!

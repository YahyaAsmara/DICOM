import json
import re
from pathlib import Path
import pydicom
import pandas as pd

class BidsConfigValidator:
    def __init__(self, config_path):
        """
        Initialize the BIDS configuration validator
        
        Args:
            config_path (str): Path to the dcm2bids configuration file
        """
        self.config_path = Path(config_path)
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def validate_regex_patterns(self):
        """Validate all regex patterns in the configuration"""
        issues = []
        for idx, desc in enumerate(self.config['descriptions']):
            try:
                pattern = desc['criteria']['SeriesDescription']
                re.compile(pattern)
            except re.error as e:
                issues.append(f"Invalid regex in description {idx}: {str(e)}")
            except KeyError:
                issues.append(f"Missing SeriesDescription in description {idx}")
        return issues
    
    def analyze_dicom_directory(self, dicom_dir):
        """
        Analyze DICOM files to check if they match the configuration patterns
        
        Args:
            dicom_dir (str): Directory containing DICOM files
        """
        dicom_dir = Path(dicom_dir)
        series_descriptions = []
        
        # Collect all unique SeriesDescriptions from DICOM files
        for dcm_file in dicom_dir.glob('**/*.dcm'):
            try:
                ds = pydicom.dcmread(dcm_file, stop_before_pixels=True)
                if hasattr(ds, 'SeriesDescription'):
                    series_descriptions.append(ds.SeriesDescription)
            except:
                continue
                
        series_descriptions = list(set(series_descriptions))
        
        # Check which descriptions match our patterns
        matches = []
        for desc in series_descriptions:
            matching_patterns = []
            for config_desc in self.config['descriptions']:
                pattern = config_desc['criteria']['SeriesDescription']
                if re.search(pattern, desc):
                    matching_patterns.append({
                        'pattern': pattern,
                        'modality': config_desc['modalityLabel'],
                        'dataType': config_desc['dataType']
                    })
            
            matches.append({
                'series_desc': desc,
                'matches': matching_patterns
            })
            
        return pd.DataFrame(matches)
    
    def optimize_config(self):
        """Suggest optimizations for the configuration"""
        suggestions = []
        
        # Check for duplicate patterns
        patterns = {}
        for idx, desc in enumerate(self.config['descriptions']):
            pattern = desc['criteria']['SeriesDescription']
            if pattern in patterns:
                suggestions.append(f"Duplicate pattern found: {pattern}")
            patterns[pattern] = idx
            
        # Suggest combining similar patterns
        for desc in self.config['descriptions']:
            pattern = desc['criteria']['SeriesDescription']
            if 'SAG' in pattern and 'Sag' in pattern:
                suggestions.append(f"Consider combining SAG and Sag patterns using (?i)Sag")
            if 'AX' in pattern and 'Ax' in pattern:
                suggestions.append(f"Consider combining AX and Ax patterns using (?i)Ax")
                
        return suggestions
    
    def export_optimized_config(self, output_path):
        """
        Export an optimized version of the configuration
        
        Args:
            output_path (str): Path to save the optimized configuration
        """
        optimized_config = {
            "searchMethod": "re",
            "descriptions": []
        }
        
        # Combine case-insensitive patterns
        patterns_seen = set()
        for desc in self.config['descriptions']:
            pattern = desc['criteria']['SeriesDescription']
            base_pattern = pattern.lower()
            
            if base_pattern not in patterns_seen:
                # Create case-insensitive pattern
                new_pattern = pattern.replace('SAG|Sag', '(?i)Sag')
                new_pattern = new_pattern.replace('AX|Ax', '(?i)Ax')
                new_pattern = new_pattern.replace('COR', '(?i)Cor')
                
                optimized_config['descriptions'].append({
                    "dataType": desc['dataType'],
                    "criteria": {
                        "SeriesDescription": new_pattern
                    },
                    "modalityLabel": desc['modalityLabel']
                })
                patterns_seen.add(base_pattern)
                
        with open(output_path, 'w') as f:
            json.dump(optimized_config, f, indent=2)

def main():
    # Example usage
    validator = BidsConfigValidator('config.json')
    
    # Validate regex patterns
    issues = validator.validate_regex_patterns()
    if issues:
        print("Found issues:")
        for issue in issues:
            print(f"- {issue}")
            
    # Get optimization suggestions
    suggestions = validator.optimize_config()
    if suggestions:
        print("\nOptimization suggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
            
    # Export optimized config
    validator.export_optimized_config('config_optimized.json')
    
if __name__ == "__main__":
    main()
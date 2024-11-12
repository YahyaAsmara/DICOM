from pathlib import Path
import json
import re
import logging

class ConfigValidator:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        
        with open(self.config_path) as f:
            self.config = json.load(f)
    
    def validate(self):
        """Validate the entire configuration"""
        self.logger.info("Starting configuration validation")
        issues = []
        issues.extend(self.validate_regex_patterns())
        issues.extend(self.validate_structure())
        return issues
    
    def validate_regex_patterns(self):
        """Validate all regex patterns in the configuration"""
        issues = []
        for idx, desc in enumerate(self.config.get('descriptions', [])):
            try:
                pattern = desc.get('criteria', {}).get('SeriesDescription')
                if pattern:
                    re.compile(pattern)
                else:
                    issues.append(f"Missing SeriesDescription in description {idx}")
            except re.error as e:
                issues.append(f"Invalid regex in description {idx}: {str(e)}")
            except Exception as e:
                issues.append(f"Error in description {idx}: {str(e)}")
        return issues
    
    def validate_structure(self):
        """Validate the basic structure of the configuration"""
        issues = []
        
        # Check required top-level keys
        if 'searchMethod' not in self.config:
            issues.append("Missing 'searchMethod' in configuration")
        if 'descriptions' not in self.config:
            issues.append("Missing 'descriptions' in configuration")
            
        # Check each description
        for idx, desc in enumerate(self.config.get('descriptions', [])):
            if 'dataType' not in desc:
                issues.append(f"Missing 'dataType' in description {idx}")
            if 'criteria' not in desc:
                issues.append(f"Missing 'criteria' in description {idx}")
            if 'modalityLabel' not in desc:
                issues.append(f"Missing 'modalityLabel' in description {idx}")
                
        return issues
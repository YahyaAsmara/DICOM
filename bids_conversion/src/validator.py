from pathlib import Path
import json
import re
import logging
import pandas as pd

class ConfigValidator:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        
        with open(self.config_path) as f:
            self.config = json.load(f)
    
    def validate(self):
        self.logger.info("Starting configuration validation")
        issues = []
        issues.extend(self.validate_regex_patterns())
        issues.extend(self.check_duplicates())
        return issues
    
    def validate_regex_patterns(self):
        issues = []
        for idx, desc in enumerate(self.config['descriptions']):
            try:
                pattern = desc['criteria']['SeriesDescription']
                re.compile(pattern)
            except re.error as e:
                issues.append(f"Invalid regex in description {idx}: {str(e)}")
        return issues
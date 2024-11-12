import pytest
from src.validator import ConfigValidator
import json

def test_validator_initialization(config_file):
    """Test validator initialization"""
    validator = ConfigValidator(config_file)
    assert validator.config is not None
    assert "descriptions" in validator.config

def test_validate_regex_patterns(config_file):
    """Test regex pattern validation"""
    validator = ConfigValidator(config_file)
    issues = validator.validate_regex_patterns()
    assert len(issues) == 0

def test_validate_invalid_regex(tmp_path):
    """Test validation with invalid regex pattern"""
    config = {
        "searchMethod": "re",
        "descriptions": [{
            "dataType": "anat",
            "criteria": {
                "SeriesDescription": "((invalid regex"  # Invalid regex pattern
            },
            "modalityLabel": "T1w"
        }]
    }
    
    config_path = tmp_path / "invalid_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
    
    validator = ConfigValidator(config_path)
    issues = validator.validate_regex_patterns()
    assert len(issues) > 0
    assert "Invalid regex" in issues[0]

def test_check_duplicates(config_file):
    """Test duplicate pattern detection"""
    validator = ConfigValidator(config_file)
    duplicates = validator.check_duplicates()
    assert len(duplicates) == 0

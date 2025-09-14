# src/tests/test_quality.py

import pandas as pd
import pandera as pa
from pandera import Column, Check
import re

# Define schema with row value + timestamp validation
nba_event_schema = pa.DataFrameSchema(
    {
        "team": Column(str, nullable=False),
        "player": Column(str, nullable=False),
        "action": Column(
            str,
            nullable=False,
            checks=Check.isin(["rebound", "assist", "3pt_shot", "2pt_shot", "block", "turnover", "steal"])
        ),
        "outcome": Column(str, nullable=True),
        "timestamp": Column(
            str,
            nullable=False,
            checks=Check.str_matches(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")  # ISO 8601 basic check
        ),
    },
    strict=True
)

def test_schema_validation():
    """Test that valid data matches expected schema"""
    data = pd.DataFrame([
        {"team": "LAL", "player": "LeBron James", "action": "3pt_shot", "outcome": "made", "timestamp": "2025-09-13T00:22:43"}
    ])
    nba_event_schema.validate(data)

def test_missing_required_column():
    """Test failure when column is missing"""
    bad_data = pd.DataFrame([
        {"team": "LAL", "player": "LeBron James", "action": "3pt_shot"}  # missing outcome, timestamp
    ])
    try:
        nba_event_schema.validate(bad_data)
        assert False, "Validation should have failed but passed"
    except pa.errors.SchemaError:
        assert True

def test_row_count():
    """Basic row count sanity check"""
    data = pd.DataFrame([
        {"team": "NYK", "player": "Julius Randle", "action": "rebound", "outcome": "missed", "timestamp": "2025-09-13T01:00:00"}
    ])
    assert len(data) > 0, "Row count should be > 0"

def test_invalid_action_value():
    """Test failure when action contains invalid value"""
    bad_data = pd.DataFrame([
        {"team": "BOS", "player": "Jayson Tatum", "action": "dunk", "outcome": "made", "timestamp": "2025-09-13T01:00:00"}  # "dunk" not allowed
    ])
    try:
        nba_event_schema.validate(bad_data)
        assert False, "Validation should have failed for invalid action value"
    except pa.errors.SchemaError:
        assert True

def test_invalid_timestamp_format():
    """Test failure when timestamp is not ISO 8601"""
    bad_data = pd.DataFrame([
        {"team": "MIA", "player": "Jimmy Butler", "action": "assist", "outcome": "made", "timestamp": "09/13/2025 01:00"}  # wrong format
    ])
    try:
        nba_event_schema.validate(bad_data)
        assert False, "Validation should have failed for invalid timestamp"
    except pa.errors.SchemaError:
        assert True

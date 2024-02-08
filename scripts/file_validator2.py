#!/usr/bin/env python

import sys
import os
import yaml
import json
from cerberus import Validator


def load_schema(schema_path):
    """Load Cerberus schema from YAML file."""
    with open(schema_path, 'r') as f:
        schema = yaml.safe_load(f)
    return Validator(schema)


def validate_data(data, validator):
    """Validate data against the provided Cerberus validator."""
    if validator.validate(data):
        return True
    else:
        print("Validation errors:")
        for field, error in validator.errors.items():
            print(f"Field '{field}': {error}")
        return False


def save_validated_data(data, save_path):
    """Save validated data to JSON file."""
    with open(save_path, 'w') as f:
        json.dump(data, f, indent=4)


def main(schema_path, data_path, save_path):
    # Load schema
    validator = load_schema(schema_path)

    # Read and validate data
    with open(data_path, 'r') as f:
        data = yaml.safe_load(f)
    if validate_data(data, validator):
        # Save validated data with the same filename as the input file
        base_name, _ = os.path.splitext(os.path.basename(data_path))
        save_file_path = os.path.join(save_path, f"{base_name}.json")
        save_validated_data(data, save_file_path)
        print(f"Data validated successfully. Saved to {save_file_path}")
    else:
        print("Data validation failed. File not saved.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python validate_and_save.py <schema_path> <data_path> <save_path>")
        sys.exit(1)

    schema_path = sys.argv[1]
    data_path = sys.argv[2]
    save_path = sys.argv[3]
    main(schema_path, data_path, save_path)

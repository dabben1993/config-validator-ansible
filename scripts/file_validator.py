import json
import os

from structlog import get_logger
import cerberus
import yaml

log = get_logger()


class FileValidator:

    def __init__(self, schema_path, file_path, destination=None, file_name=None):
        self.schema_path = schema_path
        self.file_path = file_path
        self.destination = destination
        self.file_name = file_name
        self.validator = self.load_schema()
        self.debug()
        self.process_configuration()

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            log.info("Schema loaded", schema=schema)
            print("schema loaded")
            return cerberus.Validator(schema)

    def process_configuration(self):
        config_data = self.read_yaml()
        if config_data:
            log.info("Config data exists", config_data=config_data)
            if self.validator.validate(config_data):
                log.info("Configuration is valid")
                self.save_as_json(data=json.dumps(config_data, indent=2),
                                  file_name=os.path.splitext(os.path.basename(self.file_path)))

                log.info("File saved")

            else:
                for error in self.validator.errors:
                    log.warning("Invalid configuration:", f"  - {error}: {self.validator.errors[error]}")

    def save_as_json(self, data, file_name):
        try:
            os.makedirs(self.destination, exist_ok=True)
            json_output_path = os.path.join(self.destination, file_name + ".json")
            with open(json_output_path, 'w') as json_output_file:
                json.dump(data, json_output_file, indent=2)
            print("saved")
            log.info("File saved as JSON", data=data, file_path=json_output_path)
        except Exception as e:
            log.error("Error saving JSON file", error=str(e))

    def read_yaml(self):
        try:
            with open(self.file_path, 'r') as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            log.error("Error reading YAML file", error=str(e))
            return None

    def debug(self):
        print("debugging")

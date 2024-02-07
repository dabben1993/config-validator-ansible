import json
import os

from structlog import get_logger
import cerberus
import yaml
import file_helper

log = get_logger()


class FileValidator:

    def __init__(self, schema_path, file_path, destination=None, file_name=None):
        self.schema_path = schema_path
        self.file_path = file_path
        self.destination = destination
        self.file_name = file_name
        self.validator = self.load_schema()
        self.process_configuration()

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            log.info("Schema loaded", schema=schema)
            return cerberus.Validator(schema)

    def process_configuration(self):
        config_data = file_helper.read_yaml(self.file_path)
        if config_data:
            log.info("Config data exists", config_data=config_data)
            if self.validator.validate(config_data):
                log.info("Configuration is valid")
                file_helper.save_as_json(data=json.dumps(config_data, indent=2),
                                         file_name=os.path.splitext(os.path.basename(self.file_path))[0],
                                         output_directory=self.destination)
                log.info("File saved")

            else:
                for error in self.validator.errors:
                    log.warning("Invalid configuration:", f"  - {error}: {self.validator.errors[error]}")

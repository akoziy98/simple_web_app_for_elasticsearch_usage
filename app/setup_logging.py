"""
Provides functionality to set up the logger config
"""

import logging
import logging.config
import yaml

def setup_logging(logging_yaml_config_fpath):
    """
    setup logging via YAML
    :param logging_yaml_config_fpath: filepath to logger config
    :return: None
    """
    if logging_yaml_config_fpath:
        with open(logging_yaml_config_fpath) as config_fin:
            logging.config.dictConfig(yaml.safe_load(config_fin))
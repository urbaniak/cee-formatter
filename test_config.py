"""Send a message to a remote syslog server"""

import sys
import logging.config
import yaml

try:
    config_file = sys.argv[1]
except IndexError:
    config_file = 'remote_syslog.conf'

with open(config_file) as f:
    logging.config.dictConfig(yaml.load(f))

logging.warning("Powered by dictConfig")

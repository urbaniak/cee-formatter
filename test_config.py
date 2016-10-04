"""Send a message to a remote syslog server"""

import logging.config
import yaml

with open('remote_syslog.conf') as f:
    logging.config.dictConfig(yaml.load(f))

logging.warning("Powered by dictConfig")

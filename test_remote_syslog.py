"""Send a message to a remote syslog server"""

import logging
import logging.handlers
import socket

import cee_formatter

# Log to a remote syslog using the TCP protocol
syshandler = logging.handlers.SysLogHandler(
		address=('127.0.0.1', 13514), socktype = socket.SOCK_STREAM)

# The newline terminator is required if we use TCP
fmt = cee_formatter.CEEFormatter(terminate=True)
syshandler.setFormatter(fmt)

logging.getLogger().addHandler(syshandler)

logging.error("unhelpful error message")

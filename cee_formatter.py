import json
import logging
import traceback
from datetime import date, datetime

IGNORED_FIELDS = (
    'args',
    'asctime',
    'created',
    'exc_info',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName',
)


class CEEFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        """The following keyword arguments are specifi to CEEFormatter:
            ignored_fields: list of strings. This fields will not be written to the
                            json record.
            terminate: If True, the output string is newline-terminated. This is necessary
                       when using the syslog protocol over TCP, or else the messages will
                       not be received correctly. Default: False.
            colon_start: If True, the the string ": " is prepended to the @cee cookie. this
                       is neccesary for the correct parsing of the message by rsyslog/mmjsonparse.
                       if it is missing, you will get a message about a missing JSON cookie.
                       (default: True)
        The rest of the arguments are passed to logging.Formatter.

        The formatTime method is overriden to report time in UTC and
        in RFC3339 format.
        """
        _kwargs = dict(kwargs)

        self.ignored_fields = _kwargs.pop('ignored_fields', IGNORED_FIELDS)

        terminate = _kwargs.pop('terminate', False)
        colon_start = _kwargs.pop('colon_start', True)

        self._template = ((': ' if colon_start else '')
                           + '@cee: %s'
                           + ('\n' if terminate else '')
                         )

        super(CEEFormatter, self).__init__(*args, **_kwargs)

    def jsonhandler(self, obj):
        try:
            return str(obj)
        except Exception:
            return '<object of type \'{}\' cannot be converted to str>'.format(
                type(obj).__name__
            )

    def formatTime(self, log_record):
        return datetime.utcfromtimestamp(log_record.created).isoformat()

    def format(self, log_record):
        # see https://fedorahosted.org/lumberjack/wiki/FieldList
        # extra fields are dumped into the "app" dictionary.
        app_data = {k: v for k, v in log_record.__dict__.items()
                         if k not in IGNORED_FIELDS}

        app_data.update({
            'module': log_record.module,
            'function': log_record.funcName,
            'logger': log_record.name,
            })

        if log_record.exc_info:
            app_data['exception'] = '\n'.join(
                traceback.format_exception(*log_record.exc_info)
                )

        record = {
            'time': self.formatTime(log_record),
            'msg': log_record.getMessage(),
            'pri': log_record.levelname,
            'sev': log_record.levelno,
            'proc': {
                'pid': log_record.process,
                'tid': log_record.thread,
                'name': log_record.processName,
                'tname': log_record.threadName
            },
            'file': {
                'line': log_record.lineno,
                'name': log_record.filename,
                'path': log_record.pathname
            },
            'app': app_data
        }

        return self._template % (
            json.dumps(record, default=self.jsonhandler)
        )

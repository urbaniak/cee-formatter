import datetime
import json
import logging
import traceback
from collections import OrderedDict

IGNORED_FIELDS = (
    'args',
    'asctime',
    'created',
    'exc_info',
    'levelno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'relativeCreated',
    'thread',
)


class CEEFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.ignored_fields = kwargs.get('ignored_fields', IGNORED_FIELDS)

        super().__init__(*args, **kwargs)

    def jsonhandler(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(self.datefmt)
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        try:
            return str(obj)
        except Exception:
            return '<object of type \'{}\' cannot be converted to str>'.format(
                type(obj).__name__
            )

    def format(self, log_record):
        record = OrderedDict()

        record['time'] = self.formatTime(log_record)
        record['msg'] = log_record.getMessage()
        record['pid'] = log_record.process
        record['tid'] = log_record.thread
        record['pri'] = log_record.levelname

        if log_record.exc_info:
            record['exception'] = '\n'.join(
                traceback.format_exception(*log_record.exc_info)
            )

        for k in sorted(log_record.__dict__.keys()):
            if k not in self.ignored_fields and log_record.__dict__[k]:
                record[k] = log_record.__dict__[k]

        if record['threadName'] == 'MainThread':
            del record['threadName']

        if record['processName'] == 'MainProcess':
            del record['processName']

        return "@cee: %s" % (
            json.dumps(record, default=self.jsonhandler)
        )

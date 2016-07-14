import datetime
import json
import logging

from cee_formatter import CEEFormatter

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test_datetime_format():
    stream = StringIO()

    logger = logging.getLogger('test')

    handler = logging.StreamHandler(stream)
    formatter = CEEFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    date = datetime.datetime.now()

    logger.error('test', extra={
        'd': date,
    })

    value = stream.getvalue()

    assert value.startswith('@cee: {')

    json_value = value.replace('@cee: ', '')

    json_dict = json.loads(json_value)

    assert json_dict['d'] == date.isoformat()

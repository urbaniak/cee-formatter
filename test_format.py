import datetime
import json
import logging

import iso8601

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

    # We want to make sure that the time is in full ISO8601 format so
    # we don't lose too much precision (it'll be microseconds).
    # This assertion can generate a false positive when timestamp has
    # a zero microsecond part but I think we can live with it.
    serialized_timestamp = json_dict['time']
    timestamp = iso8601.parse_date(serialized_timestamp).replace(tzinfo=None)
    assert serialized_timestamp == timestamp.isoformat()

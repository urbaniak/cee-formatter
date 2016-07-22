# Python logging cee formatter [![Build Status](https://travis-ci.org/urbaniak/cee-formatter.svg?branch=master)](https://travis-ci.org/urbaniak/cee-formatter)

This is a python formatter which formats logs in CEE format (https://cee.mitre.org).

Logs in CEE format can be parsed by [rsyslog](http://www.rsyslog.com)'s mmjsonparse moodule, logstash or graylog.


## Usage

Here's example logging configuration with `CEEFormatter`.

```python
from cee_formatter import CEEFormatter
from logging.config import dictConfig

LOGGING = {
    'version': 1,
    'formatters': {
        'cee': {
            'class': 'cee_formatter.CEEFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'cee',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            "propagate": False,
        },
    },
}

dictConfig(LOGGING)

```

Example rsyslog configuration for parsing CEE and pushing structured logs to elasticsearch.

```
module(load="mmjsonparse")
action(type="mmjsonparse")

template(name="plain-syslog" type="list") {
    constant(value="{")

    constant(value="\"@timestamp\":\"")
    property(name="timereported" dateFormat="rfc3339")

    constant(value="\",")
    property(name="$!" position.from="3")
}

action(
    type="omelasticsearch"
    server="localhost"
    template="plain-syslog"
    bulkmode="on"
    searchIndex="logstash-index"
    dynSearchIndex="on"
    queue.type="linkedlist"
    queue.size="5000"
    queue.dequeuebatchsize="300"
    action.resumeretrycount="1"
)
```

This is a python formatter which formats logs in CEE format (https://cee.mitre.org).

Logs in CEE format can be parsed by [rsyslog](http://www.rsyslog.com)'s mmjsonparse moodule, logstash or graylog.


# Usage

## Example 1: Logging configuration

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

## Example rsyslog configuration for parsing CEE and pushing structured logs to elasticsearch.

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

## Example 3: Log CEE messages to mongodb using rsyslog


### Logger Config

```
version: 1
formatters:
  cee:
    (): cee_formatter.CEEFormatter
    terminate: true
handlers:
  syslog:
    class: logging.handlers.SysLogHandler
    formatter: cee
    address: [127.0.0.1, 13514]
    socktype: ext://socket.SOCK_STREAM
root:
    handlers: [syslog]
```

### rsyslog config

Entries are inserted into a db called "logs" into a collection named "cee".

```
#################
#### MODULES ####
#################

# provides TCP syslog reception
module(load="imtcp")
module(load="mmjsonparse")
module(load="ommongodb")

input(type="imtcp" port="13514" Ruleset="mongodb")

###############
#### RULES ####
###############

# copied from http://www.rsyslog.com/using-mongodb-with-rsyslog-and-loganalyzer/

template(name="mongodball" type="subtree" subtree="$!")

ruleset(name="mongodb") {
        if $programname == "rsyslogd" then {
                action(type="ommongodb" server="127.0.0.1" db="logs" collection="rsyslog")
        } else {
                action(type="mmjsonparse")
                if $parsesuccess == "OK" then {
                        set $!host = $hostname;

                        set $!syslog!timestamp = $timereported;
                        set $!syslog!time_recvd = $timegenerated;
                        # set $!syslog!procid = $syslogtag;
                        set $!syslog!fac = $syslogfacility;
                        set $!syslog!sev = $syslogpriority;
                        set $!syslog!pri = $syslogpriority-text;
                        set $!syslog!pid = $procid;
                        action(type="ommongodb" server="127.0.0.1" db="logs" collection="cee" template="mongodball")
                }
        }
 }
```

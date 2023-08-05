# c42eventextractor - Utilities to extract and record Code42 security events

![Build status](https://github.com/code42/security-event-extractor/workflows/build/badge.svg)
[![versions](https://img.shields.io/pypi/pyversions/c42eventextractor.svg)](https://pypi.org/project/c42eventextractor/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The `c42eventextractor` package provides modules that assist in the retrieval and logging of Code42 security events.
This is done by exposing handlers that allow developers to supply custom behaviors to occur when events are retrieved.
By default, the extractors will simply print their results to stdout, but these handlers can be extended to allow developers
to record the event info to whatever location or format they desire.

## Requirements

- Python 2.7.x or 3.5.0+
- Code42 Server 6.8.x+

## Installation

Once you've done that, install `c42eventextractor` using:

```bash
$ python setup.py install
```

## Usage - AED

To get all security events within the last default look-back days (60 days):

```python
from c42eventextractor.extractors import FileEventExtractor
from c42eventextractor import FileEventHandlers
from py42.sdk import SDK

code42 = SDK.create_using_local_account(
    "https://example.authority.com",
    "admin@example.com",
    "password",
)

handlers = FileEventHandlers()

# Add implementations for customizing handling response and getting/setting insertion timestamp cursors:
def handle_response(response):
    pass

def record_cursor_position(cursor):
    pass

def get_cursor_position():
    pass

handlers.handle_response = handle_response
handlers.record_cursor_position = record_cursor_position
handlers.get_cursor_position = get_cursor_position

extractor = FileEventExtractor(code42, handlers)
extractor.extract()

# To get all security events in a particular time range, provide an EventTimestamp filter.
# Note that if you use `record_cursor_position`, your event timestamp filter may not apply.

from py42.sdk.file_event_query.event_query import EventTimestamp
time_filter = EventTimestamp.in_range(1564694804, 1564699999)
extractor.extract(1564694804)
extractor.extract(time_filter)

```

`c42eventextractor` provides some common logging and formatting implementations that you may find useful for reporting on this data.
For example, to submit each event to a syslog server in CEF format, try using the below as your `handle_response` implementation:

```python
import json
import logging
from c42eventextractor.logging.handlers import NoPrioritySysLogHandler
from c42eventextractor.logging.formatters import FileEventDictToCEFFormatter

my_logger = logging.getLogger("MY_LOGGER")
handler = NoPrioritySysLogHandler("examplehostname.com")
handler.setFormatter((FileEventDictToCEFFormatter()))
my_logger.addHandler(handler)
my_logger.setLevel(logging.INFO)

def handle_response(response):
    events = json.loads(response.text)["fileEvents"]
    for event in events:
        my_logger.info(event)
```

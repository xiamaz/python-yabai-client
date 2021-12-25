# Python Yabai Client

This is a reimplementation of the client part of yabai in python. This currently
only establishes a unix socket connection, sends a freeform string and parses
the returned json data into a python data structure.

## Example

```
import yabai_client

yc = yabai_client.YabaiClient()
spaces_info = yc.send_message("query --spaces")
# This will get spaces information as a dict
```

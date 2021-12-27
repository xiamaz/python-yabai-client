import time
from yabai_client import YabaiClient
yc = YabaiClient()

display_info = yc._send_message("query", "--displays")

spaces_info = yc._send_message("query", "--spaces")

print(spaces_info)

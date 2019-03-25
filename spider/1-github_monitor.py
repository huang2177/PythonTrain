# url https://api.github.com/repos/huang2177/huang
# web_page https://github.com/huang2177/HIndicatorDialog

import json
import time
import webbrowser
import urllib.request as r


last_update = '2018-08-00T03:34:33Z'
api = 'https://api.github.com/repos/huang2177/huang'
web_page = 'https://github.com/huang2177/HIndicatorDialog'

all_info = json.loads(str(r.urlopen(api).read(), 'utf-8'))

cur_update = all_info['updated_at']

while True:
    if not last_update:
        last_update = cur_update

    if last_update < cur_update:
        webbrowser.open(web_page)

    last_update = cur_update
    time.sleep(60)

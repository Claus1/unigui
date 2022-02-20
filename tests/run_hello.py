import sys
import os
from aiohttp import web

wd = os.getcwd()
#add 2 path if unigui is installed near
print(wd[:wd.find('/unigui')] + '/unigui')
sys.path.insert(0,wd[:wd.find('/unigui')] + '/unigui')

import unigui

async def handle_get(request):
    print(request.query_string)

http_handlers = [web.get('/get', handle_get)]

class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        Hello_user.cache_url()
        print('New Hello user connected and created!')

unigui.start('Test app', user_type = Hello_user, http_handlers = http_handlers)

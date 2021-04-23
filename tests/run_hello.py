import sys
import os

import unigui

class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        print('New Hello user connected and created!')

unigui.start('Test app', port = 8000, user_type = Hello_user, upload_dir = 'images')

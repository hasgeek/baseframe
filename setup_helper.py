#!/usr/bin/env python
# Don't use this script directly. It's called from setup.py

import os
os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib/baseframe'))
os.system("make tinymce")

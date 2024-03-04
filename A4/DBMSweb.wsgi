#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/DBMSweb/")

from ClgFestMang import create_app
application = create_app()

if __name__ == "__main__":
    application.run()

#!/usr/bin/env python3

from bin import config_reader
import sys
import time
import logging
import coloredlogs

acl = config_reader.config_json_read()

logging.getLogger("paramiko").setLevel(logging.CRITICAL)

# Variables
LOG_LEVEL = acl['LOGGING']['LOG_LEVEL']
LOG_FORMAT = acl['LOGGING']['LOG_FORMAT']
LOG_FOLDER = acl['LOGGING']['LOG_FOLDER']
LOG_FILE = "{}/".format(LOG_FOLDER) + "wp_user_list_" + time.strftime("%Y%m%d-%H%M%S") + ".log"


# Initialize Logger
logger = logging.getLogger(__name__)

# Logging to File
logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format=LOG_FORMAT
    )

# Logging to Terminal with colored output
coloredlogs.install(
    fmt=LOG_FORMAT,
    stream=sys.stdout,
    level=LOG_LEVEL
    )


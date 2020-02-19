#!/usr/bin/env python3

# Import include files
from bin import config_reader, colors
from pyfiglet import Figlet

acl = config_reader.config_json_read()

# Variables
VERSION = acl['APPLICATION']['VERSION']
BANNER = acl['APPLICATION']['BANNER']

## Print ASCI Banner to Command Line
def banner():
    b = Figlet(font='small')
    v = Figlet(font='eftipiti')
    ascii_banner = b.renderText(BANNER)
    ascii_version = v.renderText(VERSION)
    print(colors.Colors.HEADER + ascii_banner + colors.Colors.ENDC + colors.Colors.OKGREEN + 'Version' + colors.Colors.ENDC + colors.Colors.BOLD +
          ascii_version + colors.Colors.ENDC )


import os
import sys
from optparse import OptionParser

__all__ = ['get_parser']

def get_parser():
    parser = OptionParser()
    parser.add_option('-f', '--config-file', dest="configfile", help="config file", default=os.path.expanduser("~/.bankscrape"))
    default_configsection = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    parser.add_option('-s', '--config-section', dest="configsection", help="config section", default=default_configsection)
    return parser


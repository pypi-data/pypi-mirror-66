#!/usr/bin/env python

import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("resource", nargs="?", help="A JSON resource file.")
args_parser.add_argument("destination", nargs="?",help="Start page folder name.")
args_parser.add_argument("-l","--list", dest="list",action="store_true", help="List available themes.")
args_parser.add_argument("-e","--extract", metavar="theme",dest="extract", help="Extract theme resource.")
args = args_parser.parse_args()


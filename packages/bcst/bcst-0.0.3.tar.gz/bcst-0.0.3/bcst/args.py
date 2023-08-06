#!/usr/bin/env python

import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("resource", help="A JSON resource file.")
args_parser.add_argument("destination", help="Start page folder name.")
args = args_parser.parse_args()


#!/usr/bin/env python

from os import path
import json, jsonschema


class Resource:
    def __init__(self, resource):
        self.resource=resource
        # Read data
        try:
            with open(resource,'r') as f:
                self.data=f.read()
        except IOError:
            print("Unable to found "+resource)
            exit(1)
        # Decode data
        try:
            self.json=json.loads(self.data)
        except:
            print("Unable to read json from "+resource)
            exit(1)
            

#!/usr/bin/env python

from libs.resource import Resource
from shutil import copytree, ignore_patterns
from jinja2 import Template
import os

class Theme:

    def __init__(self, path, resource_data):
        res=Resource(path+"/resources.json")
        self.theme_path=path.strip('/')
        self.data=res.json
        self.data.update(resource_data)
        # Read theme
        try:
            with open(path+"/index.html",'r') as f:
                self.template=Template(f.read())
        except IOError:
            print("Unable to found "+resource)
            exit(1)


    def deploy(self, path):
        copytree(self.theme_path, path, dirs_exist_ok=True,ignore=ignore_patterns("*.json","index.html"))
        themes_dir=os.path.split(self.theme_path)[0]
        theme_dir=os.path.split(self.theme_path)[1]
        with open(path+"/index.html", "w") as index:
            index.write(self.template.render(self.data))

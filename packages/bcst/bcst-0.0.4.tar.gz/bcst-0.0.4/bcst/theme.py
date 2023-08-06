#!/usr/bin/env python

from bcst.resource import Resource
from shutil import copytree, ignore_patterns
from jinja2 import Template
import os
from os import path

themes_location=path.join(path.dirname(path.abspath(__file__)),"themes")


def list_themes():
    themes=list()
    for f in os.listdir(themes_location):
        if(not(os.path.isfile(os.path.join(themes_location,f)))):
            themes.append(f)
    return(themes)

def get_theme_path(name):
    p=path.join(themes_location,name)
    if(path.isdir(p)):
        return(p)
    else:
        print("Could not find theme: "+name)
        exit(1)    

class Theme:

    def __init__(self, name):
        self.theme_path=get_theme_path(name)
        self.res_path=self.theme_path+"/resources.json"
        self.data=Resource(self.res_path).json
        # Read theme
        try:
            with open(self.theme_path+"/index.html",'r') as f:
                self.template=Template(f.read())
        except IOError:
            print("Unable to found "+resource)
            exit(1)

    def update_resource(self,resource_path):
        r=Resource(resource_path)
        self.data.update(r.json)

        
    def extract(self, dest):
        with open(dest, "w") as resFile:
            resFile.write(self.data.data)
        

    def deploy(self, dest_path):
        copytree(self.theme_path, dest_path, dirs_exist_ok=True,ignore=ignore_patterns("*.json","index.html"))
        themes_dir=os.path.split(self.theme_path)[0]
        theme_dir=os.path.split(self.theme_path)[1]
        with open(dest_path+"/index.html", "w") as index:
            index.write(self.template.render(self.data))

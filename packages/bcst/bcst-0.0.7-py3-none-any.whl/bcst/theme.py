#!/usr/bin/env python


from shutil import copytree, ignore_patterns
from jinja2 import Template
import json
from os import path, listdir

themes_location=path.join(path.dirname(path.abspath(__file__)),"themes")


def list_themes():
    themes=list()
    for f in listdir(themes_location):
        if(not(path.isfile(path.join(themes_location,f)))):
            themes.append(f)
    return(themes)

def get_theme_path(name):
    p=path.join(themes_location,name)
    if(path.isdir(p)):
        return(p)
    else:
        print("Could not find theme: "+name)
        exit(1)    


class Resource:
    """
    Load a resource file.
     - path: Contains the resources location
     - data: Contains the loaded (from json) resource data
     - content: Contains the plain text data of the resource file
    """
    def __init__(self, resource_path):
        self.path=resource_path
        # Read data
        try:
            with open(resource_path,'r') as resFile:
                self.content=resFile.read()
        except:
            self.error("unable to read "+resource_path)
        # Decode data
        try:
            self.data=json.loads(self.content)
        except:
            self.error("unable to load json from "+resource_path)
    
    def error(self, msg):
        """
        Raise error and exit.
        """
        print("In Resource ==> "+msg)
        exit(1)
        
    def update_data(self, new_data):
        """
        Update current resource data.
        """
        self.data.update(new_data)


class Theme:
    """
    Load a theme.
    """
    def __init__(self, name):
        self.path=get_theme_path(name)
        self.resource=Resource(self.path+"/resources.json")
        # Read theme
        try:
            with open(self.path+"/index.html",'r') as f:
                self.template=Template(f.read())
        except IOError:
            print("Unable to found "+resource)
            exit(1)

    def update_resource(self,resource_path):
        r=Resource(resource_path)
        self.resource.update_data(r.data)
        
    def generate(self, dest_path):
        copytree(self.path, dest_path, dirs_exist_ok=True,ignore=ignore_patterns("*.json","index.html"))
        with open(dest_path+"/index.html", "w") as index:
            index.write(self.template.render(self.resource.data))

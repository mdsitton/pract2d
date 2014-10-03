import sys
import os

def get_path():
    ''' Get top level path from where the application was lauched. '''
    # split the path at the file extension
    splitPath = os.path.realpath(sys.path[0]).split('.')

    if len(splitPath) > 1:
        path = os.sep.join(splitPath[0].split(os.sep)[:-1])
    else:
        path = os.sep.join(splitPath[0].split(os.sep))

    return path

def resolve_path(*location):
    path = get_path()
    location = (path,) + location
    location = os.sep.join(location)
    return location

def resolve_file(location, filename):
    pathInfo = (location, filename)
    filePath = os.sep.join(pathInfo)
    return filePath

def read_file(file):
    with open(file, 'r') as file:
        output = file.read()
        return output


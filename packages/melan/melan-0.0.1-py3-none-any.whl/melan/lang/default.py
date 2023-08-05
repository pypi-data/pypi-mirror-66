
import os.path as op
import json

# ------------------------------------------------------------------------

def addpath(cpl,path,before=False):
    assert op.isdir(path), NotADirectoryError('Not a folder: %s' % path)
    if before:
        cpl.pathPrepend(path)
    else:
        cpl.pathAppend(path)

def usepkg(cpl,path,prefix='',package=None):
    cpl.load(path,prefix=prefix,package=package)

def define(cpl,body=None,file=None):
    if body:
        cpl.varAdd(json.loads(body))
    if file:
        cpl.varAdd(file)

def insert(cpl,body):
    return cpl.readfile(body)

def include(cpl,body,r2l=False):
    return cpl.procfile(body,r2l)

# ------------------------------------------------------------------------

export = {
    'pre':{
        'addpath': addpath,
        'usepkg': usepkg,
        'define': define,
        'insert': insert,
        'include': include
    }
}

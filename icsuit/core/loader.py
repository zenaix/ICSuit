# -*- coding:utf-8 -*-

import os

def listmod():
    mod_path = []
    try:
        os.chdir('icsuit/module')
        for root, path, filename in os.walk('.'):
            for f in filename:
                if not f.startswith('_') and f.endswith('.py'):
                    mod_path.append(os.path.join(root, f[:-3])[2:])
        os.chdir('../../')
    except OSError:
        return None

    return mod_path

def findmod(path):
    path = path.split('/')
    mod_dir = os.path.join('icsuit/module', '/'.join(path[:-1]))
    try:
        mod_name = path[-1]+'.py'
        if mod_name in os.listdir(mod_dir):
            return (mod_dir, path[-1])
    except OSError:
        pass

    return (None, None)

def importmod(path):
    mod_dir, mod_name = findmod(path)
    if mod_dir is not None:
        mod_path = '.'.join(mod_dir.split('/'))
        try:
            return __import__(mod_path+'.'+mod_name, fromlist=[mod_name])
        except ImportError:
            pass

    return None

if __name__ == '__main__':
    print findmod("probe/nostate/tcpsyn")

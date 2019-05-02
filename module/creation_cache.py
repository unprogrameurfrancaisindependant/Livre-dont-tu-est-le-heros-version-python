# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil


def create_cache(file_to_cache):

    Chemin_execution = os.getcwd()
    os.mkdir(Chemin_execution + '/_cache')

    for files in os.listdir(Chemin_execution + '/histoires/' + file_to_cache):
        if os.path.isdir((Chemin_execution + '/histoires/'
                          + file_to_cache + '/' + files)):
            shutil.copytree((Chemin_execution + '/histoires/'
                             + file_to_cache + '/' + files),
                            (Chemin_execution + '/_cache/' + files))
        elif os.path.isfile((Chemin_execution + '/histoires/'
                             + file_to_cache + '/' + files)):
            shutil.copy2((Chemin_execution + '/histoires/'
                          + file_to_cache + '/' + files),
                         (Chemin_execution + '/_cache/' + files))

    import _cache
    os.mkdir(Chemin_execution + '/_cache/PAGES')
    for index, story_page in _cache.fichier_histoire.histoire.items():
        with open(Chemin_execution + '/_cache/PAGES/{}.txt'.format(index),
                  'w') as f:
            f.write(str(story_page))

    _cache.fichier_histoire.histoire = dict()


def delete_cache():
    Chemin_execution = os.getcwd()
    shutil.rmtree(Chemin_execution + '/_cache')


def verify_cache():
    Chemin_execution = os.getcwd()
    return os.path.exists(Chemin_execution + '/_cache')

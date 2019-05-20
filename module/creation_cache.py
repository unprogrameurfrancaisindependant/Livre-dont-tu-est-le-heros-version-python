# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil


def create_cache(file_to_cache):

    Chemin_execution = os.getcwd()
    os.mkdir(os.path.join(Chemin_execution, '_cache'))

    for files in os.listdir(os.path.join(Chemin_execution, 'histoires',
                                         file_to_cache)):
        if os.path.isdir(os.path.join(Chemin_execution, 'histoires',
                                      file_to_cache, files)):
            shutil.copytree(os.path.join(Chemin_execution, 'histoires',
                                         file_to_cache, files),
                            os.path.join(Chemin_execution, '_cache', files))
        elif os.path.isfile(os.path.join(Chemin_execution, 'histoires',
                                         file_to_cache, files)):
            shutil.copy2(os.path.join(Chemin_execution, 'histoires',
                                      file_to_cache, files),
                         os.path.join(Chemin_execution, '_cache', files))

    import _cache
    os.mkdir(os.path.join(Chemin_execution, '_cache', 'PAGES'))
    for index, story_page in _cache.fichier_histoire.histoire.items():
        with open(os.path.join(Chemin_execution,
                               '_cache', 'PAGES',
                               '{}.txt').format(index), 'w') as f:
            f.write(str(story_page))

    _cache.fichier_histoire.histoire = dict()


def delete_cache():
    Chemin_execution = os.getcwd()
    os.chmod(os.path.join(Chemin_execution, '_cache'), 0o777)
    shutil.rmtree(os.path.join(Chemin_execution, '_cache'))


def verify_cache():
    Chemin_execution = os.getcwd()
    return os.path.exists(os.path.join(Chemin_execution, '_cache'))

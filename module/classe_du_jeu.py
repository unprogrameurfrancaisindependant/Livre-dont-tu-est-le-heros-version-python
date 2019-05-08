# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import _cache


class Jeu:
    def __init__(self):
        for item in dir(_cache.fichier_histoire):
            if (not item.startswith('_') and not item == 'random' and
                not item == 'unicode_literals' and not item == 'histoire'):
                setattr(self, item, getattr(_cache.fichier_histoire, item))

    def histoire(self, page):
        try:
            with open(os.path.join('_cache', 'PAGES', '{}.txt').format(
                    str(page)), 'r') as f:
                return eval(f.read())
        except:
            print 'Page inexistante'
            raise Exception()

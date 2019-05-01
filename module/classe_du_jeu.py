# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import exemple_fichier


class Jeu:
    def __init__(self):
        for item in dir(exemple_fichier):
            if not item.startswith('_') and not item == 'random':
                setattr(self, item, getattr(exemple_fichier, item))

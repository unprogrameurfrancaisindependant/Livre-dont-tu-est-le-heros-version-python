# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Personnage:
    def __init__(self):
        # Initialise les caratéristiques du personage
        self.point_angoisse_MAX = 12
        self.point_blessure_MAX = 12
        self.point_angoisse = 0
        self.point_blessure = 12
        self.agilite = 0
        self.force = 0
        self.chance = 0
        self.inventaire = list()
        self.stats = {'1': ('Blessures', 'point_blessure', 'inv_progressbar',
                            'point_blessure_MAX', (255,   0,   0)),
                      '2': ('Angoisse', 'point_angoisse', 'progressbar',
                            'point_angoisse_MAX', (0,   0,   255)),
                      '3': ('Force', 'force', 'point'),
                      '4': ('Agilité', 'agilite', 'point'),
                      '5': ('Chance', 'chance', 'point')}

#!/usr/bin/env python3.9
# -*- coding:Utf-8 -*-
from MAJ import MAJ
from module import Game_Master, clear_files, set_permissions

DEBUG = True
# Permet de debuguer le jeu lors de sa creation

set_permissions('free')

MAJ().mise_a_jour_automatique()


Pas_d_idee = Game_Master(DEBUG)
Pas_d_idee.deroulement_jeu()
Pas_d_idee.fin_de_la_partie()
# Fonction qui doit disparaitre

clear_files()

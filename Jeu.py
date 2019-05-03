#!/usr/bin/env python2.7
# -*- coding:Utf-8 -*- 
from MAJ import MAJ
from module import Game_Master, clear_files, set_permissions

MAJ().mise_a_jour_automatique()


set_permissions('execute')

Pas_d_idee = Game_Master()
Pas_d_idee.deroulement_jeu()
Pas_d_idee.fin_de_la_partie()
# Fonction qui doit disparaitre

set_permissions('lock')

clear_files()

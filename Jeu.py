#!/usr/bin/env python
from MAJ import MAJ

MAJ().mise_a_jour_automatique()

from module import Game_Master
from module import set_permissions, clear_files

set_permissions('execute')

Pas_d_idee = Game_Master()
Pas_d_idee.deroulement_jeu()
Pas_d_idee.fin_de_la_partie()
# Fonction qui doit disparaitre

set_permissions('lock')

clear_files()

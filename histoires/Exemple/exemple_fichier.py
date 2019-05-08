# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

###############Porte code 1########################
code_bon_1 = random.randint(10,99)
code_bon_2 = random.randint(10,99)
code_faux = random.randint(10,99)

def creation_code(code_bon_1, code_bon_2, code_faux):
    #Le code bon c'est code_bon_1 + code_bon_2
    list_code = [(str(code_bon_1)+str(code_bon_2)), (str(code_bon_1)+str(code_faux)), (str(code_faux)+str(code_bon_2)),
                 (str(code_bon_2)+str(code_bon_1)), (str(code_bon_2)+str(code_faux)), (str(code_faux)+str(code_bon_1))]
    random.shuffle(list_code)
    return {'bouton_1':{'texte': list_code[0], 'reponse': list_code[0] == (str(code_bon_1)+str(code_bon_2))},
            'bouton_2':{'texte': list_code[1], 'reponse': list_code[1] == (str(code_bon_1)+str(code_bon_2))},
            'bouton_3':{'texte': list_code[2], 'reponse': list_code[2] == (str(code_bon_1)+str(code_bon_2))},
            'bouton_4':{'texte': list_code[3], 'reponse': list_code[3] == (str(code_bon_1)+str(code_bon_2))},
            'bouton_5':{'texte': list_code[4], 'reponse': list_code[4] == (str(code_bon_1)+str(code_bon_2))},
            'bouton_6':{'texte': list_code[5], 'reponse': list_code[5] == (str(code_bon_1)+str(code_bon_2))}}

creation_code = creation_code(code_bon_1, code_bon_2, code_faux)
####################################################

def consigne_1(nb_de, chance_personnage):
    return {'resultat': True if nb_de <= chance_personnage else False, 'personnage':(('chance', '-1'))}
    
histoire = {'1':
            {'actions':
             {},
             'texte':"""Salut, c'est un essaye pour savoir si mes variables se remplacent grace a ma fonction, je donne par exemple la premère partie du bon code {VAR}code_bon_1, pour un peu plus de suspence, je donne le faux {VAR}code_faux, nan je blague, celui là est juste {VAR}code_bon_2""",
             'temps':(15,),
             'choix':
             {'fonction':'creation_code',
              'parametres':{'V':2,'F':3}}},
            '2':
            {'actions':
             {'point_blessure_MAX': +12},
             'texte':"""Bravo, vous avez trouvez le bon code êtes vous content?""",
             'choix':
             {'bouton_1':{'texte':'Oui', 'page':'end'},
              'bouton_2':{'texte':'Non', 'page':'end'}}},
            '3':
            {'actions':
             {'point_angoisse': +5},
             'texte':"""Vous êtes nul, Vous avez perdus, vous devriez vous pendre!!""",
             'choix':
             {'bouton_1':{'texte':'Oui', 'page':'end'},
              'bouton_2':{'texte':'Non', 'page':'end'}}},
 }

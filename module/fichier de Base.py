# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from classe_du_jeu import Jeu
from classe_du_personnage import Personnage
from Interface_graphique import Interface

# Ajouter extention twitch plus tard: twitchio


class Game_Master:
    def __init__(self):
        self.page_actuel = str(1)
        self.Personnage = Personnage()
        self.Jeu = Jeu()
        self.histoire = self.Jeu.histoire
        self.Interface = Interface()

    def replace_var(self, phrase):
        def t(x):
            return x if x > 0 else 20000

        for I in range(phrase.count('{VAR}')):
            nb = phrase.find('{VAR}') + 5
            nb_fin = min(map(t, [phrase.find('.', nb), phrase.find(',', nb),
                                 phrase.find(' ', nb),  phrase.find('!', nb),
                                 phrase.find('?', nb)]))

            if hasattr(self.Jeu, phrase[nb:nb_fin].strip()):
                phrase = phrase.replace(phrase[nb-5:nb_fin].strip(), str(
                    getattr(self.Jeu, phrase[nb:nb_fin].strip())))
            else:
                raise "Cette variable n'existe pas: " + str(phrase[nb:nb_fin])
        return phrase

    def fonction_liste_soustraire(self, liste, objecte):
        var = liste
        var.remove(objecte)
        return var

    def lecture_pages(self):

        #######################################################################
        """
Actions:
        actions:{'nom de variable': + ou - si variable est un nombre,

                 'nom de variable': '+ ou - suivit d'un espace puis le nom
                            de votre oject'  si c'est une liste(sac a dos)
                            pour ajouter ou enlever l'object,

                 'nom de variable':("variable", "</>/<=/>=", valeur,
                             action(si nom de variable nombre alors un nombre,
                                     si une liste alors un str),

                                   ("variable", "object", action)}
        """
        def action_conditions(self, nom_variable, variable, tuplee, type_var):
            if len(tuplee) == 4:
                nom_var, signe, valeur, action = tuplee
                if not hasattr(self.Personnage, nom_var):
                    raise Exception
                var = getattr(self.Personnage, nom_var)
                if eval(str(var)+str(signe)+str(valeur)):
                    if type_var is int:
                        if type(action) is int:
                            setattr(self.Personnage, nom_variable,
                                    var + action)
                        else:
                            raise Exception
                    elif type_var is list:
                        setattr(self.Personnage, nom_variable,
                                variable+[action])

            elif len(tuplee) == 3:
                nom_var, objecte, action = tuplee
                if not hasattr(self.Personnage, nom_var):
                    raise Exception
                var = getattr(self.Personnage, nom_var)
                if type(var) is list:
                    if objecte in var:
                        if type_var is int:
                            if type(action) is int:
                                setattr(self.Personnage, nom_variable,
                                        variable + action)
                            else:
                                raise Exception
                        elif type_var is list:
                            setattr(self.Personnage, nom_variable,
                                    variable+[action])

                else:
                    raise Exception

        self.variables_histoire = self.histoire[self.page_actuel]
        if 'actions' in self.variables_histoire.keys():
            for Emplacement, quoi in (self.variables_histoire['actions']
                                      .items()):

                nom_variable = Emplacement.replace(' ', '_')
                if not hasattr(self.Personnage, nom_variable):
                    raise Exception
                self.change_stats.append(nom_variable)
                variable = getattr(self.Personnage, nom_variable)

                if type(variable) is int:
                    if type(quoi) is int:
                        setattr(self.Personnage,
                                nom_variable, variable + quoi)

                    elif type(quoi) is tuple:
                        action_conditions(self, nom_variable,
                                          variable, quoi, int)

                if type(variable) is list:
                    if type(quoi) is str:
                        if quoi[0] == '-':
                            setattr(self.Personnage, nom_variable,
                                    self.fonction_liste_soustraire(
                                        variable, quoi[2:]))

                        elif quoi[0] == '+':
                            setattr(self.Personnage, nom_variable,
                                    variable + [quoi[2:]])

                        else:
                            setattr(self.Personnage, nom_variable,
                                    variable + [quoi])

                    elif type(quoi) is tuple:
                        action_conditions(self, nom_variable,
                                          variable, quoi, list)


###############################################################################

        """
Textes:
    Ecrivez votre histoire, vous pouvez ajouter des variables en utilisant
    {VAR}nom_de_la_varible que vous initialiserez
    au debut de votre script(pour la lisibilité)

        """
        Texte = self.variables_histoire['texte']
        Texte = self.replace_var(Texte)


###############################################################################

        """
Choix:
    'choix':{'bouton_1':{'texte':'....', 'page': 1/2/etc},
             'bouton_1':{'texte':'....', 'page': 1/2/etc,
                         'condition':('nom_de_la_variable', '</>/<=/>=',
                                      'valeur' si variblle est un nombre) ou
                                                ('nom_de_la_variable',
                                        'object' si la varible est une liste)}}
            ou
            {'fonction':'nom_de_la_fonction',
            'parametres':{'V': page ou il doit aller si il réussit,
                          'F': page ou il doit aller si il échoue}}

        Pour définir une fonction allez dans votre script, définissez votre
        fonction avec les paramètres(variables) que vous voulez,
        definissez les boutons que vous voulez avoir ainsi que la combinaison
        que ous voulez. Au lieu de mettre une page, envoyez a la place
        'reponse': True/False.

        True seras assigné a la page V et False a la page F.

        Exemple (n'oublier pas la denière ligne,
                la variable doit avoir le mème nom que la fonction):

code_bon_1 = random.randint(10,99)
code_bon_2 = random.randint(10,99)
code_faux = random.randint(10,99)

def creation_code(code_bon_1, code_bon_2, code_faux):
    #Le code bon c'est code_bon_1 + code_bon_2

    list_code = [(str(code_bon_1)+str(code_bon_2)),
                (str(code_bon_1)+str(code_faux)),
                (str(code_faux)+str(code_bon_2)),
                (str(code_bon_2)+str(code_bon_1)),
                (str(code_bon_2)+str(code_faux)),
                (str(code_faux)+str(code_bon_1))]

    random.shuffle(list_code)
    return {'bouton_1':{'texte': list_code[0],
                'reponse': list_code[0] == (str(code_bon_1)+str(code_bon_2))},

            'bouton_2':{'texte': list_code[1],
                'reponse': list_code[1] == (str(code_bon_1)+str(code_bon_2))},

            'bouton_3':{'texte': list_code[2],
                'reponse': list_code[2] == (str(code_bon_1)+str(code_bon_2))},

            'bouton_4':{'texte': list_code[3],
                'reponse': list_code[3] == (str(code_bon_1)+str(code_bon_2))},

            'bouton_5':{'texte': list_code[4],
                'reponse': list_code[4] == (str(code_bon_1)+str(code_bon_2))},

            'bouton_6':{'texte': list_code[5],
                'reponse': list_code[5] == (str(code_bon_1)+str(code_bon_2))}}

creation_code = creation_code(code_bon_1, code_bon_2, code_faux)


        """

        Option_Choix = self.variables_histoire['choix']
        if 'fonction' in Option_Choix:
            Temporaire = dict()
            page_V = Option_Choix['parametres']['V']
            page_F = Option_Choix['parametres']['F']
            Choix = getattr(self.Jeu, Option_Choix['fonction'])

            for key, attribut in Choix.items():
                Temporaire[key] = (
                    attribut['texte'],
                    page_V if attribut['reponse'] else page_F, True)

        elif 'bouton_1' in Option_Choix:
            Temporaire = dict()
            for key, attribut in Option_Choix.items():
                jouable = False
                if 'condition' in attribut.keys():
                    if len(attribut['condition']) == 3:
                        nom_var, signe, valeur = attribut['condition']
                        if not hasattr(self.Personnage, nom_var):
                            raise Exception

                        var = getattr(self.Personnage, nom_var)
                        if eval(str(var)+str(signe)+str(valeur)):
                            jouable = True
                    elif len(attribut['condition']) == 2:
                        nom_var, objecte = attribut['condition']
                        if not hasattr(self.Personnage, nom_var):
                            raise Exception

                        var = getattr(self.Personnage, nom_var)
                        if type(var) is list:
                            if objecte in var:
                                jouable = True
                else:
                    jouable = True

                Temporaire[key] = (attribut['texte'], attribut['page'],
                                   jouable)

###############################################################################

        """
Si on veut ajouter un temps sur une déccision:
    'temps': (temps en secondes, choix par défault(bouton_1)
                                                (optionnel sinon random)

        """
        if 'temps' in self.variables_histoire:
            if type(self.variables_histoire['temps']) is int:
                temps = int(self.variables_histoire['temps'])
                default_choice = self.random_temps(Temporaire)
            elif type(self.variables_histoire['temps']) is tuple:
                if len(self.variables_histoire['temps']) == 1:
                    temps = int(self.variables_histoire['temps'][0])
                    default_choice = self.random_temps(Temporaire)
                else:
                    temps = int(self.variables_histoire['temps'][0])
                    default_choice = self.variables_histoire['temps'][1]
        else:
            temps = None
            default_choice = None

###############################################################################

        if 'chance' in self.variables_histoire:
            if len(self.variables_histoire['chance']) == 3:
                type_, consigne, nb_de = self.variables_histoire['chance']
            else:
                type_, consigne, nb_de = self.variables_histoire['chance'], 1
        else:
            type_ = None

        return {'choix': Temporaire, 'texte': Texte,
                'temps': temps, 'default_choice': default_choice,
                'chance': (type_, consigne, nb_de) if type_ else None}

    def lancer_de(self, nb_de, consigne, bouton=None):
        if bouton:
            fct = getattr(self.Jeu, consigne)
            dico = fct(nb_de, self.Personnage.chance)
            # Basé su ma variable chance

            if dico['resultat']:
                bouton['bouton_2'][2] = False
            else:
                bouton['bouton_1'][2] = False
            if 'personnage' in dico:
                for action in fct(nb_de)['personnage']:
                    if type(getattr(self.Jeu, action[0])) is int:
                        setattr(self.Jeu, action[0],
                                getattr(self.Jeu, action[0])
                                + int(action[1]))

                    if type(getattr(self.Jeu, action[0])) is list:
                        if type(action[1]) is str:
                            if action[1][0] == '-':
                                setattr(self.Personnage, action[0],
                                        self.fonction_liste_soustraire(
                                            getattr(self.Jeu, action[0]),
                                            action[1][2:]))

                            elif action[1][0] == '+':
                                setattr(self.Personnage, action[0],
                                        getattr(self.Jeu, action[0])
                                        + [action[1][2:]])

                            else:
                                setattr(self.Personnage, action[0],
                                        getattr(self.Jeu, action[0])
                                        + [action[1]])

        else:
            fct = getattr(self.Jeu, consigne)
            for action in fct(nb_de)['personnage']:
                if type(getattr(self.Jeu, action[0])) is int:
                    setattr(self.Jeu, action[0],
                            getattr(self.Jeu, action[0]) + int(action[1]))

                if type(getattr(self.Jeu, action[0])) is list:
                    if type(action[1]) is str:
                        if action[1][0] == '-':
                            setattr(self.Personnage, action[0],
                                    self.fonction_liste_soustraire(
                                        getattr(self.Jeu, action[0]),
                                        action[1][2:]))
                        elif action[1][0] == '+':
                            setattr(self.Personnage, action[0],
                                    getattr(self.Jeu,
                                            action[0]) + [action[1][2:]])
                        else:
                            setattr(self.Personnage, action[0],
                                    getattr(self.Jeu, action[0]) + [action[1]])

    def creation_stats(self):
        stats = self.Personnage.stats
        T = dict()
        for i, stat in stats.items():
            if stat[2] == 'progressbar' or stat[2] == 'inv_progressbar':
                T[i] = (stat[0], getattr(self.Personnage, stat[1]), stat[2],
                        getattr(self.Personnage, stat[3]), stat[4])

            elif stat[2] == 'point':
                T[i] = (stat[0], getattr(self.Personnage, stat[1]), stat[2])

        self.Interface.create_stats(T)

    def mise_a_jour_stats(self):
        stats = self.Personnage.stats
        liste_changements = list()
        for name in self.change_stats:
            for number, stat in stats.items():
                if name == stat[1]:
                    liste_changements.append((stat[0],
                                              getattr(self.Personnage, name)))

                elif len(stat) == 5 and name == stat[3]:
                    liste_changements.append((stat[0],
                                              getattr(self.Personnage, name),
                                              'echelle'))

        self.Interface.mise_a_jour_stats(liste_changements)
        self.change_stats = list()

    def random_temps(self, choix):
        liste = list()
        for bouton, opt in choix.items():
            if opt[2]:
                liste.append(bouton)
        return random.choice(liste)

    def resize(self):
        self.creation_stats()

    def deroulement_jeu(self):
        self.change_stats = list()
        self.creation_stats()
        self.Interface.Play_musique()
        resize = False
        while 1:
            data = self.lecture_pages()
            self.mise_a_jour_stats()
            retour = self.Interface.page_livre(data, resize)
            if retour[0] == 'resize':
                self.resize()
                resize = True
            elif retour[0] == 'close':
                break
            elif retour[1] == 'end':
                break
            else:
                resize = False
                self.page_actuel = str(retour[1])
                self.Interface.effacer_page_livre(retour[0])
                if retour[0] == 'resize':
                    self.resize()
                elif retour[0] == 'close':
                    break
                elif retour[1] == 'fin_anim':
                    pass

        self.Interface.Pause_musique()
        self.Interface.Close()


if __name__ == '__main__':
    Pas_d_idee = Game_Master()
    Pas_d_idee.deroulement_jeu()

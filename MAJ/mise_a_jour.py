# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import tempfile
import urllib
import urllib2
import zipfile

from mise_a_jour_paquets import paquets_mise_a_jour
from module import set_permissions


class MAJ:
    def __init__(self):
        self.URL = '''https://raw.githubusercontent.com/
unprogrameurfrancaisindependant/
Livre-dont-tu-est-le-heros-version-python/
game/MAJ/.information'''.replace('\n', '')

        self.fichier_MAJ = 'MAJ/.information'

        self.zip_URL = '''https://github.com/unprogrameurfrancaisindependant/
Livre-dont-tu-est-le-heros-version-python/archive/game.zip'''.replace('\n', '')

        self.mise_a_jour_automatique()

    def createur_variables(self, expression, prefix=''):
        variable_valeur = expression.split('=')
        setattr(self, str(prefix + variable_valeur[0].strip()),
                variable_valeur[1].strip())

    def requete_maj(self):
        req = urllib2.Request(self.URL)
        try:
            handle = urllib2.urlopen(req)
        except Exception:
            return 'no connection'
        self.page_MAJ = handle.read()

        liste = self.page_MAJ.replace('\n', '').split(';')
        for item in liste:
            self.createur_variables(item)
        self.Tipeurs = eval(self.Tipeurs)

    def fichier_maj(self):
        with open(self.fichier_MAJ, 'r') as f:
            fichier = f.read()
            liste = fichier.replace('\n', '').split(';')
            for item in liste:
                self.createur_variables(item, 'file_')

    def comparaison(self):
        version = self.version.split('.')
        file_version = self.file_version.split('.')
        for e in range(len(version)):
            if version[e] > file_version[e]:
                self.mise_a_jour_du_jeu_complet()
                return
            elif version[e] < file_version[e]:
                continue

        date_de_modification = self.date_de_modification.split('-')
        file_date_de_modification = self.file_date_de_modification.split('-')
        for e in range(len(date_de_modification)):
            if date_de_modification[e] > file_date_de_modification[e]:
                self.mise_a_jour_tipeurs()
                return
            elif date_de_modification[e] < file_date_de_modification[e]:
                continue

    def mise_a_jour_du_jeu_complet(self):
        Chemin_utilisateur = os.path.expanduser('~')
        Chemin_execution = os.getcwd()
        try:
            path_to_dir_temporaire = tempfile.mkdtemp(dir=Chemin_utilisateur)
            urllib.urlretrieve(self.zip_URL,
                               os.path.join(
                                   path_to_dir_temporaire, 'file.zip'))
            with zipfile.ZipFile(os.path.join(
                path_to_dir_temporaire, 'file.zip')
                                 , 'r') as file_zipped:
                file_zipped.extractall(path_to_dir_temporaire)
            path_to_dir_temporaire_uzipped = os.path.join(
                path_to_dir_temporaire,
                'Livre-dont-tu-est-le-heros-version-python-game')

            set_permissions('free')
            for files in os.listdir(Chemin_execution):
                if files not in ['.git', 'histoires_sauvegardees']:
                    if os.path.isdir((path_to_dir_temporaire + '/' + files)):
                        shutil.rmtree(Chemin_execution + '/' + files)
                    elif os.path.isfile((path_to_dir_temporaire
                                         + '/' + files)):
                        os.remove(Chemin_execution + '/' + files)

            for files in os.listdir(path_to_dir_temporaire_uzipped):
                if files not in ['.git', 'histoires_sauvegardees',
                                 'histoires', 'file.zip']:
                    if os.path.isdir(os.path.join(
                        path_to_dir_temporaire_uzipped, files)):
                        shutil.copytree(os.path.join(
                            path_to_dir_temporaire_uzipped, files),
                                    os.path.join(
                                         Chemin_execution, files))

                    elif os.path.isfile(os.path.join(
                            path_to_dir_temporaire_uzipped, files),):
                        shutil.copy2(os.path.join(
                            path_to_dir_temporaire_uzipped, files),
                                     os.path.join(
                                         Chemin_execution, files))

            for files in os.listdir(os.path.join(
                    path_to_dir_temporaire_uzipped, 'histoires')):
                if os.path.isfile(os.path.join(
                        Chemin_execution, 'histoires', files)):
                    os.remove(os.path.join(
                        Chemin_execution, 'histoires', files))
                    shutil.copy2(os.path.join(
                        path_to_dir_temporaire_uzipped, 'histoires'),
                        os.path.join(
                            Chemin_execution, 'histoires', files))

        except:
            message = """Une érreur s'est produite lors de la mise a
jour, veuillez réessayer ulterieurement""".replace('\n', '')

        finally:
            paquets_mise_a_jour()
            set_permissions('execute')
            try:
                shutil.rmtree(path_to_dir_temporaire)
            except:
                pass

    def mise_a_jour_tipeurs(self):
        with open(self.fichier_MAJ, 'w') as f:
            f.write('version = ' + str(self.file_version) + ';\n')
            f.write('date_de_modification = ' + str
                    (self.date_de_modification) + ';\n')
            f.write('Tipeurs = ' + str(self.Tipeurs))

    def mise_a_jour_automatique(self):
        r = self.requete_maj()
        if r == 'no connection':
            pass
        self.fichier_maj()
        self.comparaison()


if __name__ == '__main__':
    MAJ = MAJ()

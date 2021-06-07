# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import urllib.request, urllib.parse, urllib.error
import zipfile

from .mise_a_jour_paquets import paquets_mise_a_jour
from module import set_permissions

Fichier_MAJ = 'MAJ/.information'



def Tipeurs():
    global Fichier_MAJ
    with open(Fichier_MAJ, 'r') as f:
        fichier = f.read()
        liste = fichier.replace('\n', '').split(';')
        for item in liste:
            variable_valeur = item.split('=')
            if variable_valeur[0].strip() == "Tipeurs":
                return eval(variable_valeur[1])
    return dict()


def VERSION():
    global Fichier_MAJ
    with open(Fichier_MAJ, 'r') as f:
        fichier = f.read()
        liste = fichier.replace('\n', '').split(';')
        for item in liste:
            variable_valeur = item.split('=')
            if variable_valeur[0].strip() == "version":
                return str(variable_valeur[1])
    return '0.0.0'


class MAJ:
    def __init__(self):
        global Fichier_MAJ

        self.URL = '''https://raw.githubusercontent.com/
thebosslol66/Livre-dont-tu-est-le-heros-version-python/
game/MAJ/.information'''.replace('\n', '')

        self.fichier_MAJ = Fichier_MAJ

        self.zip_URL = '''https://github.com/thebosslol66/
Livre-dont-tu-est-le-heros-version-python/archive/game.zip'''.replace('\n', '')

    def createur_variables(self, expression, prefix=''):
        variable_valeur = expression.split('=')
        setattr(self, str(prefix + variable_valeur[0].strip()),
                variable_valeur[1].strip())

    def requete_maj(self):
        req = urllib.request.Request(self.URL)
        try:
            handle = urllib.request.urlopen(req)
        except Exception:
            return 'no connection'

        self.page_MAJ = handle.read()

        self.page_MAJ = self.page_MAJ.decode('UTF-8')
        
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
            urllib.request.urlretrieve(self.zip_URL,
                               os.path.join(
                                   path_to_dir_temporaire, 'file.zip'))
            with zipfile.ZipFile(os.path.join(
                    path_to_dir_temporaire, 'file.zip'),
                                 'r') as file_zipped:
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
            if (paquets_mise_a_jour()):
                self.mise_a_jour_du_jeu_complet()
                print('''Un problème est survenue avec le fichier requirements.txt,
une mise a jour a donc été effectué. Vous pouvez relancer le jeu''')
                raise Exception()
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

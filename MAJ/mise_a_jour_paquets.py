import os
import subprocess
import sys

import mise_a_jour

if os.name == 'nt':
    #sous windos
    Os = 'win'
elif os.name == 'posix':
    #sous linux
    Os = 'lin'

def paquets_mise_a_jour():
    global Os

    if Os == 'lin':
        subprocess.call(['sudo', 'python2.7', '-m', 'pip', '--update',])
    elif Os == 'win':
        subprocess.call([sys.executable, '-m', 'pip', '--update',])

    Chemin_execution = os.getcwd()
    if not 'requirements.txt' in os.listdir(Chemin_execution):
        MAJ().mise_a_jour_du_jeu_complet()
        print '''Un problème est survenue avec le fichier requirements.txt,
une mise a jour a donc été effectué. Vous pouvez relancer le jeu'''
        raise Exception()

    if Os == 'lin':
        subprocess.call(['sudo', 'python2.7', '-m', 'pip', 'install', '-r',
                     'requirements.txt'])
    elif Os == 'win':
        subprocess.call([sys.executable, '-m', 'pip', 'install', '-r',
                     'requirements.txt'])

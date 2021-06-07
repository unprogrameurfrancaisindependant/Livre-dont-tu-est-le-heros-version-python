# -*- coding: utf-8 -*-
import os
import subprocess
import sys

if os.name == 'nt':
    # sous windos
    Os = 'win'
elif os.name == 'posix':
    # sous linux
    Os = 'lin'


def paquets_mise_a_jour():
    global Os

    if Os == 'lin':
        subprocess.call(['sudo', 'python3', '-m', 'pip', '--update', ])
    elif Os == 'win':
        subprocess.call([sys.executable, '-m', 'pip3', '--update', ])

    Chemin_execution = os.getcwd()
    if 'requirements.txt' not in os.listdir(Chemin_execution):
        return 1

    if Os == 'lin':
        subprocess.call(['sudo', 'python', '-m', 'pip', 'install', '-r',
                         'requirements.txt'])
    elif Os == 'win':
        subprocess.call([sys.executable, '-m', 'pip', 'install', '-r',
                         'requirements.txt'])
    return 0

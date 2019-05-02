import os


def set_permissions(permision_type='execute', here=True):
    if not here:
        Chemin_execution = '''/home/pi/pyprojects
/Livre-dont-tu-est-le-heros-version-python'''.replace('\n', '')
    else:
        Chemin_execution = os.getcwd()

    permission = {'execute': (0o555, 0o444, 0o444),
                  'lock': (0o555, 0o444, 0o000),
                  'free': (0o777, 0o777, 0o777)}
    permission = permission[permision_type]

    for files in os.listdir(Chemin_execution):
        if files == 'Jeu.py':
            os.chmod(Chemin_execution + '/' + files, permission[0])
        elif files == 'README.md':
            os.chmod(Chemin_execution + '/' + files, permission[1])
        elif files == '.git':
            pass
        else:
            for dossier, sous_dossier, fichiers in os.walk(
                    Chemin_execution + '/' + files):
                for fichier in fichiers:
                    if fichier == 'mise_a_jour.py':
                        pass
                    elif os.path.isfile(dossier + '/' + fichier):
                        os.chmod(dossier + '/' + fichier, permission[2])


def clear_files(here=True):
    if not here:
        Chemin_execution = '''/home/pi/pyprojects
/Livre-dont-tu-est-le-heros-version-python'''.replace('\n', '')
    else:
        Chemin_execution = os.getcwd()

    for files in os.listdir(Chemin_execution):
        if files == 'Jeu.py':
            os.chmod(Chemin_execution + '/' + files, 0o555)
        elif files == 'README.md':
            os.chmod(Chemin_execution + '/' + files, 0o444)
        elif files == '.git':
            pass
        else:
            for dossier, sous_dossier, fichiers in os.walk(
                    Chemin_execution + '/' + files):
                for fichier in fichiers:
                    if fichier == 'mise_a_jour.py':
                        pass
                    elif os.path.isfile(dossier + '/' + fichier):
                        if os.path.splitext(
                                dossier + '/' + fichier)[1] == ".pyc":
                            os.chmod(dossier + '/' + fichier, 0o777)
                            os.remove(dossier + '/' + fichier)


if __name__ == '__main__':
    clear_files(False)
    set_permissions('free', False)

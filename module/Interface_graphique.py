# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

import pygame
from pygame.locals import *
from pygame.locals import (BLEND_RGBA_SUB, K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN,
                           QUIT, VIDEORESIZE)

# import fichier_de_Base

FPS = 30
# frames per second to update the screen760
WINDOWWIDTH = 1000
# width of the program's window, in pixels640
WINDOWHEIGHT = 560
# height in pixels

POLICE = 'freesans'

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)
BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)
GREY = (191, 191, 191)

IMG_bouton = list()
IMG_horloge = list()

DATA = 'DATA//'

Name = 'Le live dont vous étes le héros'

exemple = {'texte': '''Je suis un texte assez long qui doit apparfaitre
comme le ferais une machine a écrire, nous verrons ca lors des tests.
Alors j"ai décider d"écrie et d"écrire, on verras ce que ca donne\nSurtout
avec des sauts de lignes.''', 'choix': {'bouton_1': ('Bouton_1', 3, True),
                                        'bouton_2': ('Bouton_2', 4, False)}}


class IMG_bouton_color:
    def __init__(self):
        global IMG_bouton

    def new_color(self, color):
        self.IMG_bouton = list()
        for IMG in IMG_bouton:
            Im = IMG.copy()
            Im_array = pygame.PixelArray(Im)
            for i in range(0, 260, 5):
                Im_array.replace(WHITE + (i, ), color + (i, ))
            self.IMG_bouton.append(Im)
        setattr(self, 'IMG_bouton_{}'.format(
            str(color[0]) + str(color[1]) + str(color[2])), self.IMG_bouton)


IMG_bouton_color = IMG_bouton_color()


def blit_text(surface, text, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    # 2D array where each row is a list of words.
    space = font.size(' ')[0]
    # The width of a space.
    max_width, max_height = surface.get_size()
    T = ""
    x, y = (0, 0)
    for line in words:
        for word in line:
            word_surface = font.render(word, 1, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                T += '\n'
                x = 0
                y += word_height
            T += word + ' '
            x += word_width + space
        T += '\n'
        x = 0
        y += word_height
    return T


def taille_text_fct_rect(text, max_width, max_height):
    global POLICE
    size = 1
    font = pygame.font.SysFont(POLICE, size)
    w, h = font.render(text, 1, (0, 0, 0)).get_size()
    while w < max_width and h < max_height:
        size += 1
        font = pygame.font.SysFont(POLICE, size)
        w, h = font.render(text, 1, (0, 0, 0)).get_size()
    return size - 1


class Bouton(pygame.sprite.Sprite):
    def __init__(self, pos, taille, parametres, name, color=None, size=40,
                 animation=True):
        global DISPLAYSURF, IMG_bouton, IMG_bouton_color
        pygame.sprite.Sprite.__init__(self)
        # Appel du constructeur de Sprite

        self.name = name
        self.page = parametres[1]
        self.actif = parametres[2]

        if not color:
            color = GREEN if self.actif else GREY

        if not getattr(IMG_bouton_color,
                       'IMG_bouton_{}'.format(str(color[0]) + str(color[1])
                                              + str(color[2])), False):
            IMG_bouton_color.new_color(color)
            self.T = getattr(IMG_bouton_color,
                             'IMG_bouton_{}'.format(str(color[0])
                                                    + str(color[1])
                                                    + str(color[2])))
        else:
            self.T = getattr(IMG_bouton_color,
                             'IMG_bouton_{}'.format(str(color[0])
                                                    + str(color[1])
                                                    + str(color[2])))

        self.IMG_bouton = list()
        for Im in self.T:
            self.IMG_bouton.append(pygame.transform.scale(Im, taille))

        self.image = self.IMG_bouton[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        DISPLAYSURF.blit(self.image, self.rect)

        self.font = pygame.font.SysFont(POLICE, size)
        self.text = self.font.render(parametres[0].encode('ascii', 'ignore')
                                     .decode('ascii'), 1, (0, 0, 0, 255),
                                     (255, 255, 255)).convert_alpha()
        Text_array = pygame.PixelArray(self.text)
        Text_array.replace((0, 0, 0, 255), (0, 0, 0, 0), 0.7)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (taille[0]/2, taille[1]/2)

        self.img_actuelle = 0

        self.cliquable = False

        if not animation:
            self.img_actuelle = 104

    def update(self, apparition=True, alpha=255):
        if apparition:
            self.update_anim()
            DISPLAYSURF.blit(self.image, self.rect)
        else:
            self.dissoudre(alpha)

    def update_anim(self):
        if self.img_actuelle <= 104:
            self.image = self.IMG_bouton[self.img_actuelle]
            if FPS == 60:
                self.img_actuelle += 1
            elif FPS == 30:
                self.img_actuelle += 2

            if self.img_actuelle > 100 and self.actif:
                self.cliquable = True
            self.image.blit(self.text, self.text_rect,
                            special_flags=pygame.BLEND_RGBA_MULT)

    def clic(self, pos):
        over = self.rect.collidepoint(pos)
        if over and self.cliquable:
            return self.page
        else:
            return None

    def dissoudre(self, alpha):
        self.image.fill((0, 0, 0, alpha), None, special_flags=BLEND_RGBA_SUB)
        DISPLAYSURF.blit(self.image, self.rect)


class Horloge(pygame.sprite.Sprite):
    def __init__(self, pos, taille, temps=30, default_choice='bouton_1',
                 size=40):
        global IMG_horloge

        pygame.sprite.Sprite.__init__(self)

        self.nb_temps = temps*60 + 60

        self.IMG_horloge = list()
        for Im in IMG_horloge:
            self.IMG_horloge.append(pygame.transform.scale(Im, taille))

        self.image = self.IMG_horloge[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.font = pygame.font.SysFont(POLICE, size)
        self.text = self.font.render((str(temps) + "s")
                                     .encode('ascii', 'ignore')
                                     .decode('ascii'), 1, (0, 0, 0),
                                     (255, 255, 255))

        self.text_rect = self.text.get_rect()
        self.text_rect.center = (taille[0] / 2, taille[1] - taille[0] / 4)

        self.show = False
        self.list_img = []
        self.time = 0
        self.nb_img_tot = len(self.IMG_horloge)
        self.nb_img = 0

        self.default_choice = default_choice
        self.end = None

        if FPS == 30:
            self.decal = - ((self.nb_temps) % 48 - 48) + 2
        elif FPS == 60:
            self.decal = - ((self.nb_temps) % 48 - 48) + 1

    def start(self):
        self.show = True

    def stop(self):
        self.show = False

    def new_time(self, time):
        self.time = time

    def update(self, apparition=True, alpha=255):
        if apparition:
            if self.show:
                if FPS == 60:
                    self.nb_img += 1
                elif FPS == 30:
                    self.nb_img += 2

                self.image = self.IMG_horloge[int(self.nb_img + self.decal)
                                              % self.nb_img_tot]

                self.text = self.font.render((str(int(
                    (self.nb_temps - self.nb_img) / 60))+"s")
                                             .encode('ascii', 'ignore')
                                             .decode('ascii'), 1, (0, 0, 0),
                                             (255, 255, 255))

                self.image.fill((255, 255, 255), self.text_rect)
                self.image.blit(self.text, self.text_rect)

                DISPLAYSURF.blit(self.image, self.rect)

                if (self.nb_temps-self.nb_img) <= 0:
                    self.end = True
        else:
            self.dissoudre(alpha)

    def dissoudre(self, alpha):
        self.image.fill((0, 0, 0, alpha), None, special_flags=BLEND_RGBA_SUB)
        DISPLAYSURF.blit(self.image, self.rect)


class Texte(pygame.sprite.Sprite):
    def __init__(self, texte, size, color, pos, width, height, animation=True):
        global DISPLAYSURF, FPS, POLICE
        pygame.sprite.Sprite.__init__(self)

        self.fini = False

        #################################################################

        self.font = pygame.font.SysFont(POLICE, size)
        self.image = pygame.Surface((width, height))

        self.texte = blit_text(self.image, texte.encode('ascii', 'ignore')
                               .decode('ascii'), self.font)

        self.texte_list = self.texte.splitlines()

        self.color = color
        self.pos = pos

        self.textSurf = self.font.render(self.texte, 1, self.color)

        #################################################################

        self.rect = self.image.get_rect()

        self.nb_ligne = 0
        self.nb_chars = 0

        phrase_surface = self.font.render(self.texte_list[0], 1, color)
        self.rect_phrase_en_cour = pygame.rect.Rect(pos,
                                                    phrase_surface.get_size())

        self.list_text = list()

        self.nb_char = dict()
        nb = 0
        for line in self.texte_list:
            self.nb_char[nb] = len(line)
            nb += 1

        if not animation:
            self.nb_chars = len(self.texte_list) + 1
            while not self.fini:
                self.update_anim()

    def update(self, apparition=True, alpha=255):
        if apparition:
            self.update_anim()
            for opt in self.list_text:
                DISPLAYSURF.blit(*opt)
        else:
            self.dissoudre(alpha)

    def update_anim(self):
        if self.nb_ligne < len(self.texte_list):
            if FPS == 60:
                text_actu = self.font.render(
                    self.texte_list[self.nb_ligne][:int(self.nb_chars)], 1,
                    self.color)

                rect_cache = self.rect_phrase_en_cour
                self.nb_chars += 0.25
                if self.nb_chars >= self.nb_char[self.nb_ligne] - 1:
                    self.list_text.append((self.font.render(
                        self.texte_list[self.nb_ligne], 1, self.color),
                                           self.rect_phrase_en_cour))

                    self.nb_chars = 0
                    self.nb_ligne += 1
                    if self.nb_ligne < len(self.texte_list):
                        phrase_surface = self.font.render(
                            self.texte_list[self.nb_ligne], 1, self.color)
                        self.pos = (self.pos[0],
                                    self.pos[1]+phrase_surface.get_size()[1])
                        self.rect_phrase_en_cour = pygame.rect.Rect(
                            self.pos, phrase_surface.get_size())
                    else:
                        self.fini = True

            elif FPS == 30:
                text_actu = self.font.render(
                    self.texte_list[self.nb_ligne][:int(self.nb_chars)], 1,
                    self.color)
                rect_cache = self.rect_phrase_en_cour
                self.nb_chars += 0.5
                if self.nb_chars >= self.nb_char[self.nb_ligne] - 1:
                    self.list_text.append((self.font.render(
                        self.texte_list[self.nb_ligne], 1, self.color),
                                           self.rect_phrase_en_cour))

                    self.nb_chars = 0
                    self.nb_ligne += 1
                    if self.nb_ligne < len(self.texte_list):
                        phrase_surface = self.font.render(
                            self.texte_list[self.nb_ligne], 1, self.color)
                        self.pos = (self.pos[0],
                                    self.pos[1] + phrase_surface.get_size()[1])
                        self.rect_phrase_en_cour = pygame.rect.Rect(
                            self.pos, phrase_surface.get_size())
                    else:
                        self.fini = True

            DISPLAYSURF.blit(text_actu, rect_cache)

    def dissoudre(self, alpha):
        for opt in self.list_text:
            opt[0].fill((0, 0, 0, alpha), None, special_flags=BLEND_RGBA_SUB)
            DISPLAYSURF.blit(opt[0], opt[1])


class Points(pygame.sprite.Sprite):
    def __init__(self, text, point, pos, size, color=(0, 0, 0)):
        global DISPLAYSURF, FPS
        pygame.sprite.Sprite.__init__(self)

        self.point = point
        self.font = pygame.font.SysFont(POLICE, size)
        self.color = color
        self.texte = text
        self.text = self.font.render(str(self.texte.encode('ascii', 'ignore')
                                         .decode('ascii')) + ': ' + str(
                                             self.point), 1, self.color)
        self.rect = self.text.get_rect()
        self.pos = pos
        self.rect = self.rect.move(self.pos)

    def update(self):
        DISPLAYSURF.blit(self.text, self.rect)

    def update_point(self, new_points):
        self.point = new_points
        self.text = self.font.render(str(self.texte.encode('ascii', 'ignore')
                                         .decode('ascii')) + ': ' + str(
                                             self.point), 1, self.color)
        self.rect = self.text.get_rect()
        self.rect.move(self.pos)


class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, text, max_point, pos, size, color_bar,
                 color_text=(0, 0, 0), point=0):
        global DISPLAYSURF, FPS
        pygame.sprite.Sprite.__init__(self)

        self.max_point = max_point
        self.point = point
        self.color_bar = color_bar
        self.color_text = color_text
        self.pos = pos
        self.font = pygame.font.SysFont(POLICE, size)
        self.pourcentage = self.point/float(self.max_point)
        self.texte = text
        self.text = self.font.render(str(self.texte.encode('ascii', 'ignore')
                                         .decode('ascii')) + ':' + ' ' * 16
                                     + str(self.point), 1, self.color_text)
        self.rect = self.text.get_rect()
        self.rect = self.rect.move(self.pos)

        self.spaces = self.font.size(' ')[0] * 14

        self.width_progress_bar = max(1, int((1/float(14))
                                             * self.text.get_size()[1]))

        self.size_text = self.font.render(
            str(self.texte.encode('ascii', 'ignore').decode('ascii'))
            + ':' + ' ', 1, self.color_text).get_size()

        self.contour_rect = pygame.rect.Rect(
            self.size_text[0] + self.width_progress_bar, self.pos[1]
            + self.width_progress_bar, self.spaces - self.width_progress_bar*3,
            self.size_text[1] - self.width_progress_bar * 3)

        self.progress_rect = pygame.rect.Rect(
            self.size_text[0] + self.width_progress_bar * 2, self.pos[1]
            + self.width_progress_bar * 2, (
                self.spaces - self.width_progress_bar * 4) * self.pourcentage,
            self.size_text[1] - self.width_progress_bar * 4)

    def update(self):
        DISPLAYSURF.blit(self.text, self.rect)
        pygame.draw.rect(DISPLAYSURF, self.color_bar, self.progress_rect)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), self.contour_rect,
                         int(self.width_progress_bar))

    def update_point(self, new_points):
        self.point = new_points
        self.text = self.font.render(str(self.texte.encode('ascii', 'ignore')
                                         .decode('ascii')) + ':' + ' '*16
                                     + str(self.point), 1, self.color_text)
        self.rect = self.text.get_rect()
        self.rect = self.rect.move(self.pos)
        self.pourcentage = self.point/float(self.max_point)
        self.progress_rect = pygame.rect.Rect(
            self.size_text[0] + self.width_progress_bar * 2,
            self.pos[1] + self.width_progress_bar * 2,
            (self.spaces - self.width_progress_bar * 4)*self.pourcentage,
            self.size_text[1] - self.width_progress_bar * 4)


class Interface:
    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, LOGOIMAGE, SPOTIMAGE
        global SETTINGSIMAGE, SETTINGSBUTTONIMAGE, RESETBUTTONIMAGE
        global NAME, DATA, NBDECHET, WINDOWWIDTH, WINDOWHEIGHT
        global IMG_bouton, IMG_horloge, DATA
        pygame.init()
        pygame.mixer.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode(
            (WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
        # pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(Name)

        cursor = pygame.cursors.load_xbm(
            (os.path.join(DATA, 'CURSEUR', 'or_curseur_dague.xbm')).encode('utf8'),
            (os.path.join(DATA, 'CURSEUR', 'and_curseur_dague.xbm')).encode('utf8'))

        pygame.mouse.set_cursor(*cursor)
        pygame.mouse.set_visible(1)

        IMG_bouton = list()
        for i in range(105):
            IMG_bouton.append(pygame.image.load(
                (os.path.join(DATA, 'BOUTON', 'IMG_bouton_{}')
                 ).encode('utf8').format(i+1)).convert_alpha())

        IMG_horloge = list()
        for i in range(48):
            IMG_horloge.append(pygame.image.load(
                (os.path.join(DATA, 'HORLOGE', 'IMG_horloge_{}')
                 ).encode('utf8').format(i+1)).convert_alpha())

        pygame.mixer_music.load(
            os.path.join(DATA, 'MUSIQUE', 'Glaciaere-Hammock-02RelaxingInTheHammock.wav'))

        self.creation_de_la_partie()
        # Lignes a modifier

    def creation_de_la_partie(self):
        import _cache
        pygame.display.set_caption(_cache.NOM_DU_LIVRE)
        try:
            cursor = pygame.cursors.load_xbm(
                (os.path.join('_cache', 'DATA', 'CURSEUR', 'or_curseur_dague.xbm')).encode('utf8'),
                (os.path.join('_cache', 'DATA', 'CURSEUR', 'and_curseur_dague.xbm')).encode('utf8'))
        except:
            cursor = pygame.cursors.load_xbm(
                (os.path.join(DATA, 'CURSEUR', 'or_curseur_dague.xbm')).encode('utf8'),
                (os.path.join(DATA, 'CURSEUR', 'and_curseur_dague.xbm')).encode('utf8'))
        pygame.mouse.set_cursor(*cursor)
        pygame.mouse.set_visible(1)

    def Play_musique(self):
        pygame.mixer_music.play(-1)

    def Pause_musique(self):
        pygame.mixer_music.pause()

    def Close(self):
        pygame.mixer.quit()
        pygame.quit()
        time.sleep(1)

    def create_stats(self, stats):
        global DISPLAYSURF
        taille_x, taille_y = DISPLAYSURF.get_size()
        taille_barre_stats = taille_x/6
        taille = int(taille_barre_stats/10)
        font = pygame.font.SysFont(POLICE, taille)
        taille_y_space = font.size(' ')[1]
        pos = (0, 0)
        T = tuple()
        for i in range(len(stats)):
            stat = stats[str(i+1)]
            if stat[2] == 'progressbar' or stat[2] == 'inv_progressbar':
                T += (ProgressBar(
                    stat[0], stat[3], pos, taille, stat[4], point=stat[1]),)
            elif stat[2] == 'point':
                T += (Points(stat[0], stat[1], pos, taille), )
            pos = (0, pos[1]+taille_y_space)

        self.stats_sprites = pygame.sprite.RenderPlain(*T)

    def mise_a_jour_stats(self, stats):
        for stat in stats:
            if len(stat) == 2:
                for sprite in self.stats_sprites:
                    if sprite.texte == stat[0]:
                        sprite.update_point(stat[1])

            elif len(stat) == 3:
                for sprite in self.stats_sprites:
                    if sprite.texte == stat[0]:
                        sprite.max_point = stat[1]
                        sprite.update_point(sprite.point)

    def rapport(self):
        taille_voulut = DISPLAYSURF.get_size()
        taille_img = self.cap_size
        raport = [0, 0]
        raport[0] = taille_voulut[0]/float(taille_img[0])
        raport[1] = taille_voulut[1]/float(taille_img[1])
        if raport[0] > raport[1]:
            self.cap_new_size = raport[0]
        elif raport[1] < raport[0]:
            self.cap_new_size = raport[1]
        else:
            self.cap_new_size = raport[0]

    """
    def fond_stokage(self):
        nb_img = 0
        taille_x, taille_y = DISPLAYSURF.get_size()
        for i in range(int(self.nb_images_fond)):
            try:
                ret, frame = self.cap.read()
            except:
                pass

            cv2.resize(frame, None, fx=self.cap_new_size,
                        fy=self.cap_new_size, interpolation = cv2.INTER_AREA)
            frame = numpy.fliplr(frame)
            frame = numpy.rot90(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame[0:taille_x, 0:taille_y]

            self.list_fond_ecran.append(pygame.surfarray.make_surface(frame))
            nb_img += 1
    """

    def progress_bar(self):
        pass

    def page_livre(self, data, resize=False):
        global DISPLAYSURF
        taille_x, taille_y = DISPLAYSURF.get_size()
        longueur_bouton = (taille_x*3)/10
        longueur_d2 = longueur_bouton/12
        longueur_d1 = longueur_bouton + 2*longueur_d2
        hauteur_bouton = taille_y/12
        hauteur_d1 = 3*hauteur_bouton/2
        hauteur_d2 = 2*hauteur_bouton/3
        hauteur_d3 = hauteur_bouton/4

        t = 50
        nb_bouton = len(data['choix'])
        for i in range(nb_bouton):
            text = data['choix']['bouton_{}'.format(i+1)][0]
            size = taille_text_fct_rect(text, longueur_bouton, hauteur_bouton)
            t = min(t, size)
        size = t

        taille_barre_stats = taille_x/6
        taille_sup = taille_y/10

        liste_bouton = list()

        if nb_bouton == 1:
            liste_bouton.append(
                Bouton((longueur_d1, (2*taille_y/3+hauteur_d1)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
        elif nb_bouton == 2:
            liste_bouton.append(
                Bouton((longueur_d2, (2*taille_y/3+hauteur_d1)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+hauteur_d1)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_2'], 'bouton_2',
                       size=size, animation=not resize))
        elif nb_bouton == 3:
            liste_bouton.append(
                Bouton((longueur_d2, (2*taille_y/3+hauteur_d2)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+hauteur_d2)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_2'], 'bouton_2',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d1,
                        (2*taille_y/3+2*hauteur_d2+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_3'], 'bouton_3',
                       size=size, animation=not resize))
        elif nb_bouton == 4:
            liste_bouton.append(
                Bouton((longueur_d2, (2*taille_y/3+hauteur_d2)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+hauteur_d2)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_2'], 'bouton_2',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d2,
                        (2*taille_y/3+2*hauteur_d2+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_3'], 'bouton_3',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+2*hauteur_d2+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_4'], 'bouton_4',
                       size=size, animation=not resize))
        elif nb_bouton == 5:
            liste_bouton.append(
                Bouton((longueur_d2, (2*taille_y/3+hauteur_d3)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+hauteur_d3)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_2'], 'bouton_2',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d2,
                        (2*taille_y/3+2*hauteur_d3+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_3'], 'bouton_3',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+2*hauteur_d3+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_4'], 'bouton_4',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d1,
                        (2*taille_y/3+3*hauteur_d3+2*hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_5'], 'bouton_5',
                       size=size, animation=not resize))
        elif nb_bouton == 6:
            liste_bouton.append(
                Bouton((longueur_d2, (2*taille_y/3+hauteur_d3)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_1'], 'bouton_1',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+hauteur_d3)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_2'], 'bouton_2',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d2,
                        (2*taille_y/3+2*hauteur_d3+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_3'], 'bouton_3',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+2*hauteur_d3+hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_4'], 'bouton_4',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((longueur_d2,
                        (2*taille_y/3+3*hauteur_d3+2*hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_5'], 'bouton_5',
                       size=size, animation=not resize))
            liste_bouton.append(
                Bouton((taille_x-longueur_bouton-longueur_d2,
                        (2*taille_y/3+3*hauteur_d3+2*hauteur_bouton)),
                       (longueur_bouton, hauteur_bouton),
                       data['choix']['bouton_6'], 'bouton_6',
                       size=size, animation=not resize))

        T = tuple()
        for i in liste_bouton:
            T += (i,)
        self.bouton_sprites = pygame.sprite.RenderPlain(T)
        taille_text = taille_text_fct_rect(data['texte'][:60],
                                           taille_x-taille_barre_stats*2,
                                           (taille_y*2/3 - taille_sup)/16)

        self.text = Texte(data['texte'], taille_text, WHITE,
                          (taille_barre_stats, taille_sup),
                          taille_x-taille_barre_stats*2,
                          taille_y*2/3 - taille_sup, not resize)

        self.text_sprites = pygame.sprite.RenderPlain(self.text)

        if data['temps']:
            self.temps = True
            if not resize:
                self.horloge = Horloge((taille_x-taille_x/6, 0),
                                       (taille_x/6, taille_x/6), data['temps'],
                                       data['default_choice'],
                                       int(taille_x/6/10))
            else:
                self.horloge = Horloge((taille_x-taille_x/6, 0),
                                       (taille_x/6, taille_x/6),
                                       self.stokage_temps,
                                       data['default_choice'],
                                       int(taille_x/6/10))
            self.horloge.start()
            self.horloge_sprites = pygame.sprite.RenderPlain(self.horloge)
        else:
            self.temps = False

        # nb_image_fond = 0
        temps_timer = 0
        while 1:
            FPSCLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ('close', )
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return ('close', )
                elif event.type == VIDEORESIZE:
                    DISPLAYSURF = pygame.display.set_mode(
                        event.dict['size'], pygame.RESIZABLE)
                    if self.temps:
                        self.stokage_temps = (
                            self.horloge.nb_temps-self.horloge.nb_img)/60
                    return ('resize', )
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_xy = pygame.mouse.get_pos()
                        for sprites in self.bouton_sprites.sprites():
                            if sprites.clic(mouse_xy):
                                return sprites.name, sprites.page

            DISPLAYSURF.fill(ORANGE)
            """
            ####Fond animé####
            DISPLAYSURF.blit(self.list_fond_ecran[int(nb_image_fond%
            self.nb_images_fond)], (0, 0))
            nb_image_fond += 1
            ####          ####
            """

            self.stats_sprites.update()
            # Affiche stats
            self.text_sprites.update()
            # Affiche Texte
            if self.text.fini:
                self.bouton_sprites.update()
                # Affiche boutons
                temps_timer += 1
            if self.temps:
                if FPS == 30 and temps_timer >= 60 and not resize:
                    self.horloge_sprites.update()
                elif FPS == 60 and temps_timer >= 120 and not resize:
                    self.horloge_sprites.update()
                elif resize:
                    self.horloge_sprites.update()
                if self.horloge.end:
                    return (self.horloge.default_choice,
                            data['choix'][self.horloge.default_choice][1])

            pygame.display.flip()
            # pygame.display.update()

    def effacer_page_livre(self, bouton):
        global DISPLAYSURF

        alpha = 0
        alpha_diff = 0

        if FPS == 30:
            ajout = 0.135
        elif FPS == 60:
            ajout = 0.0775

        while 1:
            FPSCLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ('close',)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return ('close',)
                elif event.type == VIDEORESIZE:
                    DISPLAYSURF = pygame.display.set_mode(
                        event.dict['size'], pygame.RESIZABLE)
                    return ('resize',)

            DISPLAYSURF.fill(ORANGE)

            self.stats_sprites.update()
            self.text_sprites.update(False, alpha)
            self.horloge_sprites.update(False, alpha)

            for sprites in self.bouton_sprites.sprites():
                if sprites.name != bouton:
                    sprites.update(False, alpha)
                else:
                    sprites.update(False, alpha_diff)

            pygame.display.flip()

            if alpha < 255:
                alpha += ajout
            if alpha_diff < 255 and alpha > 2.5:
                alpha_diff += ajout
            if alpha_diff >= 10:
                return ('fin_anim',)


"""
I = Interface()
for i in range(20):
    I.page_livre(exemple)
    time.sleep(1)
"""

# -*- coding: utf-8 -*-
"""
Module de pilotage d'une carte microcontrôleur (PyBoard, ESP32, Micro:bit, ...) fonctionnant sous micropython à partir d'un ordinateur sous Python.

@author: David Thérincourt - 2020
"""

from .pyboard import Pyboard

def execFileOnBoard(nomFichier, portSerie, debit = 115200):
    """
    Fonction qui exécute un programme MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW. La fonction retourne un tuple transmise par une fonction print() placée dans le script.

    Paramètres :
        nomFichier (str) : nom du fichier MicroPython à exécuté.
        portSerie (str) : nom du port série sur lequel se trouve le microcontrôleur (ex. COM6)

    Paramètre optionnel :
        debit (int) :  débit de transfert des données sur le port série (115200 bauds par défaut)

    Retourne (tuple) :
        Tuple transmis par une unique fonction print(tuple) placée dans le script micropython.
        Exemple : print((x,y))
    """
    pyb = Pyboard(portSerie, debit)
    pyb.enter_raw_repl()
    printResult = pyb.execfile(nomFichier)
    pyb.close()
    return eval(printResult.decode())

def execFileOnBoardToStr(nomFichier, portSerie, debit = 115200):
    """
    Fonction qui exécute un programme MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW. La fonction retourne une chaine de caractères transmise par une fonction print() placée dans le script.

    Paramètres :
        nomFichier (str) : nom du fichier MicroPython à exécuté.
        portSerie (str) : nom du port série sur lequel se trouve le microcontrôleur (ex. COM6)

    Paramètre optionnel :
        debit (int) :  débit de transfert des données sur le port série (115200 bauds par défaut)

    Retourne (str) :
        Chaîne de caractères transmit par la fonction print(str) du script micropython.
    """
    pyb = Pyboard(portSerie, debit)
    pyb.enter_raw_repl()
    printResult = pyb.execfile(nomFichier)
    pyb.close()
    return printResult.decode()

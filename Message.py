__author__ = 'root'

from enum import Enum

class Message(Enum):

    MESSAGE_VIDE = "Il est nécessaire de saisir le nom du fichier et le nombre de tour"
    MESSAGE_NB_LOOP_POSITIF = "Le nombre de tour de boucle doit être positif"
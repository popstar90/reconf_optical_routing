"""
Tout ce qui est en rapport avec l'aléatoire
"""


from scipy.stats import randint
import numpy as np
import copy
import random


def pick_one_numbers_uniformly(low, high):
    """
    Retourne un entier précisé par size entre low et high
    :param int low: plus pétit élément probable
    :param int high: plus grand élément probable
    :param int length:  taille de l'échantillon
    :return int item:
    """
    item = low
    if low != high:
        item = list(randint.rvs(low, high, size=1))[0]
    return item

def pick_random_numbers(liste=[], percent_length=50):

    """
    Retourne un échantillon de liste.
    Chaque élément de l'échantillon  est obtenu grace �  la loi uniforme de bornes: le plus petit
    élément de liste  et le plus grand élément de liste
    :param list liste: liste d'léments �  utiliser pour généer l'échantillon
    :param length: taille de l'échntillon
    :return list sample: echantillon issu de liste
    """

    sample = []
    if percent_length != 0:
        if percent_length < 100:
            length = len(liste) * percent_length / 100
            #print('number_before', length)
            length = int(np.round(length))
            #print('number', length)
            sample = random.sample(liste, length)
        else:
            sample = copy.deepcopy(liste)
    return sample


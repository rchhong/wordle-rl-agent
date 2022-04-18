import torch as torch
import numpy as np

from const import NUM_CHARACTERS_ALPHABET

def convert_to_one_hot(word_list):
    ret = np.zeros((len(word_list), len(word_list[0]) * NUM_CHARACTERS_ALPHABET))

    for i, word in enumerate(word_list):
        for j, char in enumerate(word):
            index = ord(char) - ord('a')
            ret[i, NUM_CHARACTERS_ALPHABET * j + index] = 1

    return torch.tensor(ret)
from phone_hmm import load_phone_hmm_list
from word_hmm import load_dictionary
from utterance_hmm import construct_utterance_hmm_unigram
from viterbi import viterbi
from os import listdir
import re

phone_hmm_list = load_phone_hmm_list()

word_hmm_list = load_dictionary(phone_hmm_list)

unigram_utterance_hmm_start = construct_utterance_hmm_unigram(word_hmm_list)

folder_list = sorted(listdir("../test/f"))
for folder_name in folder_list:
    file_list = sorted(listdir("../test/f/{}".format(folder_name)))
    for file_name in file_list:
        f = open("../test/f/{}/{}".format(folder_name, file_name), "r")
        raw = f.read()
        f.close()

        row_num = int(raw.split("\n")[0].split(" ")[0])
        col_num = int(raw.split("\n")[0].split(" ")[1])
        matrix = [[0.0 for _ in range(0, col_num)] for _ in range(0, row_num)]
        raw_matrix = re.split(r'\s+', raw)[2:]

        for row in range(0, row_num):
            for col in range(0, col_num):
                matrix[row][col] = float(raw_matrix[row * col_num + col])

        viterbi(matrix, unigram_utterance_hmm_start)
        break
    break

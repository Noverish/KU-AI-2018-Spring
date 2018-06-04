from phone_hmm import load_phone_hmm_list
from word_hmm import load_dictionary
from utterance_hmm import construct_utterance_hmm_unigram
from viterbi import viterbi
import re
import output
import os

# find out file paths
file_path_list = []

for root, dirs, files in os.walk("../test/"):
    if len(dirs) == 0:
        for file in files:
            file_path_list.append(os.path.join(root, file))

file_path_list.sort()

# construct hmm
phone_hmm_list = load_phone_hmm_list()
word_hmm_list = load_dictionary(phone_hmm_list)
unigram_utterance_hmm_start = construct_utterance_hmm_unigram(word_hmm_list)

# viterbi for all files
for index, file_path in enumerate(file_path_list):
    file_name = file_path.replace("../test", "tst").replace("\\", "/")
    output_name = file_name.replace("txt", "lab")

    if output.output_exist(output_name):
        print(output_name, 'is already exist', "({}/{})".format(index+1, len(file_path_list)))
        continue

    f = open(file_path)
    raw = f.read()
    f.close()

    row_num = int(raw.split("\n")[0].split(" ")[0])
    col_num = int(raw.split("\n")[0].split(" ")[1])
    matrix = [[0.0 for _ in range(0, col_num)] for _ in range(0, row_num)]
    raw_matrix = re.split(r'\s+', raw)[2:]
    for row in range(0, row_num):
        for col in range(0, col_num):
            matrix[row][col] = float(raw_matrix[row * col_num + col])

    word_list = viterbi(matrix, unigram_utterance_hmm_start)

    output.output_to_file(output_name, word_list[1:])

    print(output_name, 'done!', "({}/{})".format(index+1, len(file_path_list)))

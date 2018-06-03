from hmm import get_state_list_from_hmm
from phone_hmm import load_phone_hmm_list
from word_hmm import load_dictionary
from utterance_hmm import construct_utterance_hmm_unigram
from pprint import pprint

phone_hmm_list = load_phone_hmm_list()

word_hmm_list = load_dictionary(phone_hmm_list)

unigram_utterance_hmm_start, unigram_utterance_hmm_end = construct_utterance_hmm_unigram(word_hmm_list)

pprint(get_state_list_from_hmm(unigram_utterance_hmm_start))
pprint(unigram_utterance_hmm_end.prev)

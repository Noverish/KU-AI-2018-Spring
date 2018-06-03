from hmm import State, find_end_state
from word_hmm import find_word_hmms
import re


def construct_utterance_hmm_unigram(word_hmm_list: [State]) -> (State, State):
    f = open("../data/unigram.txt")
    raw = f.read().strip()
    f.close()

    start_state = State(phone='start')
    end_state = State(phone='end')

    # deal with starts
    for line in raw.split('\n'):
        word_str = re.split(r'\s+', line)[0]
        prob: float = float(re.split(r'\s+', line)[1])

        word_hmms = find_word_hmms(word_hmm_list, word_str)

        assert len(word_hmms) > 0

        for i in range(0, len(word_hmms)):
            start: State = word_hmms[i]
            post_starts = list(start.next.keys())

            assert len(post_starts) > 0
            post_start = None

            for post_start in post_starts:
                start_state.next[post_start] = prob * (1 / len(word_hmms)) * start.next[post_start]
                post_start.prev.append(start_state)

                del start.next[post_start]
                post_start.prev.remove(start)

            index = word_hmm_list.index(start)
            word_hmm_list[index] = post_start
            del start

    # deal with ends
    for i in range(0, len(word_hmm_list)):
        end: State = find_end_state(word_hmm_list[i])
        pre_ends = end.prev

        assert len(pre_ends) > 0

        for pre_end in pre_ends:
            to_end_prob = pre_end.next[end]
            end_state.prev.append(pre_end)

            for word_start in list(start_state.next.keys()):
                if word_start in pre_end.next:
                    pre_end.next[word_start] += to_end_prob * start_state.next[word_start]
                else:
                    pre_end.next[word_start] = to_end_prob * start_state.next[word_start]
                    word_start.prev.append(pre_end)

            del pre_end.next[end]
            end.prev.remove(pre_end)

        del end

    return start_state, end_state

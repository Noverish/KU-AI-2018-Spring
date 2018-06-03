from hmm import State, get_state_list_from_hmm, clone_hmm
from phone_hmm import find_phone_hmm


def load_dictionary(phone_hmm_list) -> [State]:
    f = open("../data/dictionary.txt", "r")
    raw = f.read().strip()
    f.close()

    words = []
    for line in raw.split("\n"):
        word_str = line.split("\t")[0]
        phones = line.split("\t")[1].split(" ")

        word_phone_hmm_list = []
        for phone in phones:
            phone_hmm = clone_hmm(find_phone_hmm(phone_hmm_list, phone))

            tmps = get_state_list_from_hmm(phone_hmm)
            for tmp in tmps:
                tmp.word = word_str

            word_phone_hmm_list.append(phone_hmm)

        # concat two phone hmm
        while len(word_phone_hmm_list) > 1:
            now: State = word_phone_hmm_list[0]
            nxt: State = word_phone_hmm_list[1]

            now_states: [State] = get_state_list_from_hmm(now)
            next_states: [State] = get_state_list_from_hmm(nxt)

            now_end: State = now_states[-1]
            now_pre_ends: [State] = now_end.prev
            next_start: State = next_states[0]
            next_post_starts: [State] = list(next_start.next.keys())

            for now_pre_end in now_pre_ends:
                for next_post_start in next_post_starts:
                    now_pre_end.next[next_post_start] = now_pre_end.next[now_end] * next_start.next[next_post_start]
                    next_post_start.prev.append(now_pre_end)

            for now_pre_end in now_pre_ends:
                del now_pre_end.next[now_end]
                now_end.prev.remove(now_pre_end)

            for next_post_start in next_post_starts:
                del next_start.next[next_post_start]
                next_post_start.prev.remove(next_start)

            del now_end
            del next_start
            del word_phone_hmm_list[1]

        word = word_phone_hmm_list[0]
        words.append(word)

    return words


def find_word_hmms(word_hmm_list, word) -> [State]:
    output_list = []

    for word_hmm in word_hmm_list:
        if word_hmm.word == word:
            output_list.append(word_hmm)

    return output_list


def print_word_hmm(word_hmm: State):
    state_list: [State] = get_state_list_from_hmm(word_hmm)
    prev_ch = None

    print(state_list[0].word, end=' ')
    for state in state_list:
        if state.phone != prev_ch:
            print(state.phone, end=' ')
        prev_ch = state.phone
    print('')

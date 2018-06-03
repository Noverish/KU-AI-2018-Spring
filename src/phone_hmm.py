from hmm import PDF, State
import re


def load_phone_hmm_list() -> [State]:
    f = open("../data/hmm.txt", "r")
    raw = f.read()
    f.close()

    hmm_list = []
    for hmm_raw in __find_hmm_raw(raw):
        phone = __find_phone(hmm_raw)
        state_num = __find_state_num(hmm_raw)

        states = [State(phone)]
        for i in range(1, state_num - 1):
            state = __find_state(hmm_raw, i + 1)
            state.phone = phone
            states.append(state)
        states.append(State(phone))

        tp = __find_transition_probability_matrix(hmm_raw)

        for i in range(0, len(tp)):
            for j in range(0, len(tp)):
                if tp[i][j] != 0:
                    from_state = states[i]
                    to_state = states[j]
                    from_state.next[to_state] = tp[i][j]
                    to_state.prev.append(from_state)

        hmm_list.append(states[0])

    return hmm_list


def find_phone_hmm(phone_hmm_list, phone) -> State:
    for phone_hmm in phone_hmm_list:
        if phone_hmm.phone == phone:
            return phone_hmm
    assert False


def __find_hmm_raw(raw) -> [str]:
    return re.compile("~h[\s\S]*?<ENDHMM>").findall(raw)


def __find_phone(hmm_raw) -> str:
    return re.compile('".+"').search(hmm_raw).group(0)[1:-1]


def __find_state_num(hmm_raw) -> int:
    return int(re.compile("<NUMSTATES>[^\n]*").search(hmm_raw).group().split(" ")[1])


def __find_transition_probability_matrix(hmm_raw) -> [[float]]:
    tp_raw = re.compile("<TRANSP>[^<]*").search(hmm_raw).group().strip()
    tp_size = int(re.split(r'\s+', tp_raw)[1])
    raw_matrix = re.split(r'\s+', tp_raw)[2:]

    matrix = [[0.0 for _ in range(0, tp_size)] for _ in range(0, tp_size)]

    for i in range(0, tp_size):
        for j in range(0, tp_size):
            matrix[i][j] = float(raw_matrix[i * tp_size + j])

    return matrix


def __find_state(hmm_raw, number) -> State:
    index = hmm_raw.index("<STATE> {}".format(number))
    hmm_state_raw = hmm_raw[index:]
    mixes_num = int(re.compile("<NUMMIXES>[^\n]*").search(hmm_state_raw).group().split(" ")[1])

    state = State()

    for i in range(0, mixes_num):
        weight_raw = re.compile("<MIXTURE>[^\n]*").findall(hmm_state_raw)[i]
        mean_raw = re.compile("<MEAN>[^<]*").findall(hmm_state_raw)[i].strip()
        var_raw = re.compile("<VARIANCE>[^<]*").findall(hmm_state_raw)[i].strip()

        weight = float(weight_raw.split(" ")[2])
        mean = list(map(lambda x: float(x), re.split(r'\s+', mean_raw)[2:]))
        var = list(map(lambda x: float(x), re.split(r'\s+', var_raw)[2:]))

        state.pdf_list.append(PDF(weight, mean, var))

    return state

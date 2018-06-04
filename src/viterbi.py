from hmm import State, get_state_list_from_hmm_dfs
from math import log10, sqrt, pi, pow, e


def __normal_distribution_log(x, mean, var):
    a = 1 / (var * sqrt(2 * pi))
    b = -pow(x - mean, 2) / (2 * mean * mean)

    return log10(a) + b * log10(e)


def __start_log(state: State, start_state: State) -> float:
    if state in list(start_state.next.keys()):
        return log10(start_state.next[state])
    else:
        return float('-inf')


def __trans_log(state: State, next_state: State) -> float:
    if next_state in list(state.next.keys()):
        return log10(state.next[next_state])
    else:
        return float('-inf')


def __emit_log(state: State, observation_sequence: [float]) -> float:
    l = []

    for pdf in state.pdf_list:
        weight_log = log10(pdf.weight)
        prob_log = 0.0

        for i in range(0, 39):
            prob_log += __normal_distribution_log(observation_sequence[i], pdf.mean[i], pdf.var[i])

        l.append(weight_log + prob_log)

    return max(l)


def viterbi(obs: [[float]], start_state: State):
    states = get_state_list_from_hmm_dfs(start_state)
    states.remove(start_state)

    V = [{}]
    for st in states:
        V[0][st] = {"prob": __start_log(st, start_state) + __emit_log(st, obs[0]), "prev": None}

    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            # prob_list = {}
            #
            # for prev_st in st.prev:
            #     prob = V[t - 1][prev_st]["prob"] + __trans_log(prev_st, st)
            #     prob_list[prob] = prev_st
            #
            # max_tr_prob = max(list(prob_list.keys()))
            # prev_st = prob_list[max_tr_prob]
            # max_prob = max_tr_prob + __emit_log(st, obs[t])
            # V[t][st] = {"prob": max_prob, "prev": prev_st}

            max_tr_prob = max(V[t - 1][prev_st]["prob"] + __trans_log(prev_st, st) for prev_st in states)
            for prev_st in states:
                if V[t - 1][prev_st]["prob"] + __trans_log(prev_st, st) == max_tr_prob:
                    max_prob = max_tr_prob + __emit_log(st, obs[t])
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

        # print('t : {}'.format(t))

    # print_table(V)

    opt = []

    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None

    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break

    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    opt_str_list = map(lambda x: "<{} {}>".format(x.phone, x.word), opt)

    print('probability : {:.3E}'.format(max_prob))
    print('sequence : {}'.format(' '.join(opt_str_list)))


def print_table(V):
    for state in V[0]:
        state_str = str(state)
        prob_list = [v[state]["prob"] for v in V]
        prob_str_list = map(lambda x: "{:.3E}".format(x), prob_list)
        prob_str_list2 = map(lambda x: "{:10}".format(x), prob_str_list)
        prob_str_list3 = ' '.join(prob_str_list2)

        print("{:60}: {}".format(state_str, prob_str_list3))

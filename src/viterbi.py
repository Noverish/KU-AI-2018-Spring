from hmm import State, get_state_list_from_hmm_dfs
from math import log10, sqrt, pi, pow, e
import re


def __normal_distribution_log(x, mean, var):
    a = 1 / (sqrt(var) * sqrt(2 * pi))
    b = -pow(x - mean, 2) / (2 * var)

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
            max_tr_prob = max(V[t - 1][prev_st]["prob"] + __trans_log(prev_st, st) for prev_st in states)
            for prev_st in states:
                if V[t - 1][prev_st]["prob"] + __trans_log(prev_st, st) == max_tr_prob:
                    max_prob = max_tr_prob + __emit_log(st, obs[t])
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

        print('t : {}'.format(t))

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

    # opt_str_list = map(lambda x: "<{} {}>".format(x.word, x.phone), opt)

    # print('probability : {:.3E}'.format(max_prob))
    # print('sequence : \n{}'.format('\n'.join(opt_str_list)))

    phone_list = []
    for phone in opt:
        if len(phone_list) == 0:
            phone_list.append({'word': phone.word, 'phone': phone.phone})
        elif phone_list[-1]['word'] != phone.word or phone_list[-1]['phone'] != phone.phone:
            phone_list.append({'word': phone.word, 'phone': phone.phone})

    return phone_list_to_word_list(phone_list)


def print_table(V):
    for state in V[0]:
        state_str = str(state)
        prob_list = [v[state]["prob"] for v in V]
        prob_str_list = map(lambda x: "{:.3E}".format(x), prob_list)
        prob_str_list2 = map(lambda x: "{:10}".format(x), prob_str_list)
        prob_str_list3 = ' '.join(prob_str_list2)

        print("{:60}: {}".format(state_str, prob_str_list3))


def phone_list_to_word_list(word_phone_list):
    # print('word_phone_list :', word_phone_list)

    phone_list = list(map(lambda x: x['phone'],  word_phone_list))

    phone_list_str = ' '.join(phone_list)

    # print('phone_list_str :', phone_list_str)

    '''
    <s>	sil
    eight	ey t sp
    five	f ay v sp
    four	f ao r sp
    nine	n ay n sp
    oh	ow sp
    one	w ah n sp
    seven	s eh v ah n sp
    six	s ih k s sp
    three	th r iy sp
    two	t uw sp
    zero	z ih r ow sp
    zero	z iy r ow sp
    '''

    phone_list_str = phone_list_str.replace("ey t sp", "eight")
    phone_list_str = phone_list_str.replace("ey t", "eight")

    phone_list_str = phone_list_str.replace("f ay v sp", "five")
    phone_list_str = phone_list_str.replace("f ay v", "five")

    phone_list_str = phone_list_str.replace("f ao r sp", "four")
    phone_list_str = phone_list_str.replace("f ao r", "four")

    phone_list_str = phone_list_str.replace("n ay n sp", "nine")
    phone_list_str = phone_list_str.replace("n ay n", "nine")

    phone_list_str = phone_list_str.replace("w ah n sp", "one")
    phone_list_str = phone_list_str.replace("w ah n", "one")

    phone_list_str = phone_list_str.replace("s eh v ah n sp", "seven")
    phone_list_str = phone_list_str.replace("s eh v ah n", "seven")

    phone_list_str = phone_list_str.replace("s ih k s ih k s ih k s sp", "six six six")
    phone_list_str = phone_list_str.replace("s ih k s ih k s ih k s", "six six six")
    phone_list_str = phone_list_str.replace("s ih k s ih k s sp", "six six")
    phone_list_str = phone_list_str.replace("s ih k s ih k s", "six six")
    phone_list_str = phone_list_str.replace("s ih k s sp", "six")
    phone_list_str = phone_list_str.replace("s ih k s", "six")

    phone_list_str = phone_list_str.replace("th r iy sp", "three")
    phone_list_str = phone_list_str.replace("th r iy", "three")

    phone_list_str = phone_list_str.replace("t uw sp", "two")
    phone_list_str = phone_list_str.replace("t uw", "two")

    phone_list_str = phone_list_str.replace("z ih r ow sh", "zero")
    phone_list_str = phone_list_str.replace("z ih r ow", "zero")

    phone_list_str = phone_list_str.replace("z iy r ow sh", "zero")
    phone_list_str = phone_list_str.replace("z iy r ow", "zero")

    phone_list_str = phone_list_str.replace("ow sp", "oh")
    phone_list_str = phone_list_str.replace("ow", "oh")

    # print('phone_list_str :', phone_list_str)

    return re.compile('(eight|five|four|nine|oh|one|seven|six|three|two|zero)').findall(phone_list_str)

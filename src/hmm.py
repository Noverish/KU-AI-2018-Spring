class PDF:
    def __init__(self, weight, mean, var) -> None:
        self.weight = weight
        self.mean = mean
        self.var = var


class State:
    def __init__(self, phone="") -> None:
        self.phone = phone
        self.word = ""

        self.pdf_list = []
        self.next = {}
        self.prev = []

    def __repr__(self) -> str:
        return "<0x{:x} phone:'{}' word:'{}' next:'{}', prev:'{}'>".format(id(self), self.phone, self.word,
                                                                           len(self.next), len(self.prev))


def get_state_list_from_hmm(hmm: State) -> [State]:
    state_list = []

    queue = [hmm]
    while len(queue) != 0:
        now = queue[0]
        del queue[0]

        if now not in state_list:
            state_list.append(now)
            queue.extend(list(now.next.keys()))

    return state_list


def clone_hmm(hmm: State) -> State:
    origin_list: [State] = get_state_list_from_hmm(hmm)
    output_list: [State] = [State() for _ in range(0, len(origin_list))]

    for i in range(0, len(origin_list)):
        origin: State = origin_list[i]
        state: State = output_list[i]

        state.phone = origin.phone
        state.word = origin.word
        state.pdf_list = origin.pdf_list

        for key in list(origin.next.keys()):
            value: float = origin.next[key]
            index = origin_list.index(key)

            state.next[output_list[index]] = value

        for p in origin.prev:
            index = origin_list.index(p)

            state.prev.append(output_list[index])

    return output_list[0]


def find_end_state(hmm: State):
    state_list = get_state_list_from_hmm(hmm)
    end_state = state_list[-1]

    assert len(end_state.next) == 0
    assert len(end_state.pdf_list) == 0

    return end_state

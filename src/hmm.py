import re


class PropositionalDensityFunction:
    def __init__(self):
        self.weight = 0
        self.means = []
        self.vars = []

    def print(self):
        print('    weight : {}'.format(self.weight))
        print('    means : {}'.format(self.means))
        print('    vars : {}'.format(self.vars))


class HMMState:
    def __init__(self, number):
        self.number = number
        self.pdfs = []

    def print(self):
        print('  number : {}'.format(self.number))
        for pdf in self.pdfs:
            pdf.print()


class HMM:
    def __init__(self):
        self.name = ""
        self.states = []
        self.tp = []

    def print(self):
        print('name : {}'.format(self.name))
        for state in self.states:
            state.print()
        print('tp : {}'.format(self.tp))


def load_hmms() -> [HMM]:
    f = open("../data/hmm.txt", "r")
    raw = f.read()
    f.close()

    hmms = []
    hmm_strs = re.compile("~h[\s\S]*?<ENDHMM>").findall(raw)

    for hmm_str in hmm_strs:
        hmm_element_strs = re.compile("<[^<]*").findall(hmm_str)
        hmm = HMM()
        hmm.name = re.compile('".+"').search(hmm_str).group(0)[1:-1]

        now_state = None
        now_pdf = None

        for hmm_element_str in hmm_element_strs:
            hmm_element_str = re.sub(r'\s+', ' ', hmm_element_str.strip())
            element_name = re.compile("<[^>]*>").match(hmm_element_str).group()
            element_value = hmm_element_str.replace(element_name, "").strip().split(' ')

            if element_name == "<NUMSTATES>":
                hmm.states = [HMMState(i) for i in range(0, int(element_value[0]))]
            elif element_name == "<STATE>":
                number = int(element_value[0]) - 1
                now_state = hmm.states[number]
            elif element_name == "<NUMMIXES>":
                pass
            elif element_name == "<MIXTURE>":
                now_pdf = PropositionalDensityFunction()
                now_pdf.weight = float(element_value[1])
                now_state.pdfs.append(now_pdf)
            elif element_name == "<MEAN>":
                now_pdf.means = list(map(lambda a: float(a), element_value[1:]))
            elif element_name == "<VARIANCE>":
                now_pdf.vars = list(map(lambda a: float(a), element_value[1:]))
            elif element_name == "<GCONST>":
                pass
            elif element_name == "<TRANSP>":
                state_num = len(hmm.states)
                for i in range(0, state_num):
                    start_i = state_num * i + 1
                    end_i = state_num * (i + 1) + 1
                    float_list = list(map(lambda x: float(x), element_value[start_i:end_i]))
                    hmm.tp.append(float_list)
            elif element_name == "<BEGINHMM>" or element_name == "<ENDHMM>":
                pass
            else:
                print('[WARNING] Unknown element name :', element_name)

        hmms.append(hmm)

    return hmms

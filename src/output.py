

def output_to_file(file_path, word_list):
    f = open("../output.txt", "r")
    raw = f.read()
    f.close()

    if len(raw) == 0:
        raw = "#!MLF!#\n"

    raw += '"{}"\n'.format(file_path)

    raw += "\n".join(word_list) + "\n"

    f = open("../output.txt", "w")
    f.write(raw)
    f.close()


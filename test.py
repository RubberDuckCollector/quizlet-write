chars_to_ignore = ['.', '\'', '\"', ' ', '_',
                   '+', '+', '[', ']', '<', '>']


def parse_msg(msg: str) -> str:
    new_msg = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False

    for i in range(len(msg)):
        for j in range(len(msg[i])):
            if msg[i][j] == '(':
                new_msg += msg[i]
            elif msg[i][j] in chars_to_ignore:
                new_msg += msg[i][j]
            else:
                new_msg += '_'

    return new_msg


def main():
    msg = "die Gemeinschaft (-en)"

    print(parse_msg(msg))


if __name__ == '__main__':
    main()

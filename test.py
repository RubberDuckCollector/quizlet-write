chars_to_ignore = ['.', '\'', '\"', ' ', '_',
                   '+', '+', '[', ']', '<', '>']


def parse_msg(msg: str) -> str:
    new_msg = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False

    try:
        for i in range(len(msg)):
            if i > 0:
                new_msg += " "
                print(
                    "add a space, i has incremented so that must mean we're on the next word")
            for j in range(len(msg[i])):
                print(f"looking at char: {msg[i][j]}")
                if msg[i][j] == '(':
                    print("open bracket detected, add all of it to the new msg")
                    new_msg += msg[i]
                    i += 1  # since the bracket stuff is done all at once, need to go to next i
                elif msg[i][j] in chars_to_ignore:
                    print(
                        f"want to ignore making this char a _, append it as-is instead")
                    new_msg += msg[i][j]
                else:
                    new_msg += '_'

                print(f"new msg: {new_msg}")

    except IndexError:
        pass

    return new_msg


def main():
    msg = "die Gemeinschaft+ (-en)"

    print(f"'{parse_msg(msg)}'")


if __name__ == '__main__':
    main()

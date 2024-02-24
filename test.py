chars_to_ignore = ['.', '\'', '\"', ' ', '_',
                   '+', '+', '[', ']', '<', '>']


def hard(msg: str) -> str:
    hint = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False

    try:
        for i in range(len(msg)):
            if i > 0:
                hint += " "
                print(
                    "add a space, i has incremented so that must mean we're on the next word")
            for j in range(len(msg[i])):
                print(f"looking at char: {msg[i][j]}")
                if msg[i][j] == '(':
                    print("open bracket detected, add all of it to the new msg")
                    hint += msg[i]
                    i += 1  # since the bracket stuff is done all at once, need to go to next i
                elif msg[i][j] in chars_to_ignore:
                    print(
                        f"want to ignore making this char a _, append it as-is instead")
                    hint += msg[i][j]
                else:
                    hint += '_'

                print(f"new msg: {hint}")

    except IndexError:
        pass

    return hint


def normal(msg: str) -> str:
    hint = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False

    try:
        for i in range(len(msg)):
            if i > 0:
                hint += " "
                print(
                    "add a space, i has incremented so that must mean we're on the next word")
            for j in range(len(msg[i])):
                print(f"looking at char: {msg[i][j]}")
                if j == 0 and msg[i][j] != '(':
                    hint += msg[i][j]
                    print("preserve the first character of the word")
                else:
                    if msg[i][j] == '(':
                        print("open bracket detected, add all of it to the new msg")
                        hint += msg[i]
                        i += 1  # since the bracket stuff is done all at once, need to go to next i
                    elif msg[i][j] in chars_to_ignore:
                        print(
                            f"want to ignore making this char a _, append it as-is instead")
                        hint += msg[i][j]
                    else:
                        hint += '_'

                print(f"new msg: {hint}")

    except IndexError:
        pass

    return hint


def easy(msg: str) -> str:
    hint = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False

    try:
        for i in range(len(msg)):
            if i > 0:
                hint += " "
                print(
                    "add a space, i has incremented so that must mean we're on the next word")
            for j in range(len(msg[i])):
                print(f"looking at char: {msg[i][j]}")
                if j < 3 and msg[i][j] != '(':
                    hint += msg[i][j]
                    print("preserve the first character of the word")
                else:
                    if msg[i][j] == '(':
                        print("open bracket detected, add all of it to the new msg")
                        hint += msg[i]
                        i += 1  # since the bracket stuff is done all at once, need to go to next i
                    elif msg[i][j] in chars_to_ignore:
                        print(
                            f"want to ignore making this char a _, append it as-is instead")
                        hint += msg[i][j]
                    else:
                        hint += '_'

                print(f"new msg: {hint}")

    except IndexError:
        pass

    return hint


def very_hard(msg: str) -> str:

    return "No Hints!"


def main():
    msg = "die Gemeinschaft+ (-en)"

    print(f"'{hard(msg)}'")
    print(f"'{normal(msg)}'")
    print(f"'{easy(msg)}'")
    print(f"'{very_hard(msg)}'")


if __name__ == '__main__':
    main()

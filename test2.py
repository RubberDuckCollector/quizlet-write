chars_to_ignore = ['.', '\'', '\"', ' ', '_', '+', '+', '[', ']', '<', '>']


def hard(msg: str) -> str:
    # turn the string into a list of chars
    msg = list(msg)

    hint = ""
    inside_brackets = False

    for i in range(1, len(msg)):
        if msg[i] in chars_to_ignore:
            # if the current char is supposed to be left untouched
            # do that and add it straight to the hint
            hint += msg[i]
        else:
            if msg[i] == '(':
                # add the ( to the hint
                # change the program flow to signal that the code is within a pair of brackets
                inside_brackets = True
                hint += '('
            elif msg[i] == ')':
                # signal that the program is outside the brackets
                # can now add '_' to the rest of the hint
                inside_brackets = False
                hint += ')'
            elif inside_brackets is True:
                # add the actual char to the hint if the char is in betwwen brackets
                hint += msg[i]
            else:
                hint += '_'

    return hint


def make_normal_hint(msg: str) -> str:
    hint = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False
    # TODO: make it so the program goes into a "brackets mode" when it finds brackets
    # preserves content inside brackets and the bracket chars themselves
    # string processing goes back to normal otherwise
    # with the first letter of each word being preserved
    # otherwise it's turned into a _

    try:
        for i in range(len(msg)):
            if i > 0:
                hint += " "
            for j in range(len(msg[i])):
                if j == 0 and msg[i][j] != '(':
                    hint += msg[i][j]
                else:
                    if msg[i][j] == '(':
                        hint += msg[i]
                        i += 1  # since the bracket stuff is done all at once, need to go to next i
                    elif msg[i][j] in chars_to_ignore:
                        hint += msg[i][j]
                    else:
                        hint += '_'

    except IndexError:
        pass

    return hint

def main():
    msg = "die Gemeinschaft+ (-en a;lsdkfj;lasdj faljdksf ;asdfjkl afdsjkl lafs jfs) adfs;ljkfadsljk;afsdadflasdf;ll"

    print(make_normal_hint(msg))


if __name__ == '__main__':
    main()

import my_modules.constants

VALID_DIFFICULTIES = ["easy", "normal", "hard", "very-hard"]


# https://www.geeksforgeeks.org/how-to-find-chinese-and-japanese-character-in-a-string-in-python/
def is_japanese_char(character):
    if '\u3040' <= character <= '\u30FF' or '\u4E00' <= character <= '\u9FFF':
        return True
    else:
        return False

def is_chinese_char(character):
    if '\u4E00' <= character <= '\u9FFF' or '\u3400' <= character <= '\u4DBF':
            return True
    return False

def make_very_hard_hint() -> str:
    return "No hints!"


def make_hard_hint(msg: str) -> str:
    hint = ""
    inside_brackets = False

    for i in range(len(msg)):
        if msg[i] in my_modules.constants.chars_to_ignore:
            # if char should be preserved when hint is being built
            hint += msg[i]
        elif msg[i] in ['(', '（']:
            # if we're currently looking at a (
            # inside_brackets will be assigned True
            # add the ( to the hint
            hint += msg[i]
            inside_brackets = True
        elif msg[i] in [')', '）']:
            # if we're at the end of the bracket
            # add the ) to the hint
            # inside_brackets becomes False
            inside_brackets = False
            hint += msg[i]
        elif inside_brackets is True:
            # add the character stright to the hint
            # we want to preserve the characters inside brackets
            # into the hint
            # therefore they shouldn't be an _ underscore
            hint += msg[i]
        else:
            inside_brackets = False
            # if we're not in brackets
            # the character is neither of ( or )
            # and the character isn't in my_modules.my_modules.constants.chars_to_ignore
            # it must be turned into an _

            # change the underscore to a monospaced one, makes more sense for japanese and chinese that way
            if is_japanese_char(msg[i]) or is_chinese_char(msg[i]):  
                hint += '＿'
            else:
                # otherwise, it's most likely a latin alphabet character
                hint += '_'

    return hint


def make_normal_hint(msg: str) -> str:
    hint = ""

    slashes = [i for i in range(len(msg)) if msg[i] == "/"]
    msg = msg.replace("/", " ")

    msg = list(msg)  # type: ignore # turn the string into a list of chars
    # print(msg)

    i = 0
    # iterating through the list with a while loop
    # incrementing the iterating variable manually

    inside_brackets = False

    while True:
        try:
            if msg[i] in my_modules.constants.chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] in ['(', '（']:
                    # if we're currently looking at a (
                    # inside_brackets will be assigned True
                    # add the ( to the hint
                    inside_brackets = True
                    hint += msg[i]
                elif msg[i] in [')', '）']:
                    # if we're at the end of the bracket
                    # add the ) to the hint
                    # inside_brackets becomes False
                    inside_brackets = False
                    hint += msg[i]
                elif inside_brackets:
                    # add the character stright to the hint
                    # we want to preserve the characters inside brackets
                    # into the hint
                    # therefore they shouldn't be an _ underscore
                    hint += msg[i]
                else:
                    # if all above conditions haven't been met,
                    # if we're not inside_brackets
                    # add the letter to the hint if i == 0,
                    # or the previous letter is a space
                    # otherwise add a '_'
                    # hint += msg[i] if i == 0 or msg[i - 1].isspace() else "_"  # fancy but useless syntax 

                    if i == 0 or msg[i - 1].isspace():
                        hint += msg[i]
                    else:
                        # hint += '_'
                        # change the underscore to a monospaced one, makes more sense for japanese and chinese that way
                        if is_japanese_char(msg[i]) or is_chinese_char(msg[i]):  
                            hint += '＿'
                        else:
                            # otherwise, it's most likely a latin alphabet character
                            hint += '_'

            i += 1  # increment i, ready for the next element of the list

        except IndexError:
            # if we try to access an index that's not in the list
            # it must mean we're at the end of the list
            # and therefore built up the whole hint
            # it's safe to break out of the while True
            break

    hint = list(hint)
    for i in slashes:
        hint[i] = "/"

    hint = "".join(hint)

    return hint


def make_easy_hint(msg: str) -> str:
    hint = ""

    slashes = [i for i in range(len(msg)) if msg[i] == "/"]
    msg = msg.replace("/", " ")

    msg = list(msg)  # type: ignore

    i = 0
    inside_brackets = False

    while True:
        try:
            if msg[i] in my_modules.constants.chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] in ['(', '（']:
                    inside_brackets = True
                    hint += msg[i]  # add the open bracket to the hint
                elif inside_brackets:
                    # we want to preserve the char, and put it in the hint
                    # to give the user leniency
                    # they don't have to memorise what's in the ()
                    # they'll only have to type it out
                    hint += msg[i]
                elif msg[i] in [')', '）']:
                    inside_brackets = False
                    hint += msg[i]  # add the close bracket to the hint
                else:
                    if i == 0 or msg[i - 1].isspace():
                        hint += msg[i]  # Keep the first character of the word
                    elif msg[i - 2].isspace() or i == 1:
                        hint += msg[i]  # Keep the second character of the word
                    elif msg[i - 3].isspace() or i == 2:
                        hint += msg[i]  # Keep the third character of the word
                    else:
                        # change the underscore to a monospaced one, makes more sense for japanese and chinese that way
                        if is_japanese_char(msg[i]) or is_chinese_char(msg[i]):  
                            hint += '＿'
                        else:
                            # otherwise, it's most likely a latin alphabet character
                            # replace other characters with underscore
                            hint += '_'

            i += 1
        except IndexError:
            break

    hint = list(hint)
    for i in slashes:
        hint[i] = "/"

    hint = "".join(hint)

    return hint

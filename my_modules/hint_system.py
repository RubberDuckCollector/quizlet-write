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

    for i in msg:
        if i in ['(', '（']:
            # if we're currently looking at a (
            # inside_brackets will be assigned True
            # add the ( to the hint
            hint += i
            inside_brackets = True
        elif i in [')', '）']:
            # if we're at the end of the bracket
            # add the ) to the hint
            # inside_brackets becomes False
            inside_brackets = False
            hint += i
        elif inside_brackets:
            # add the character stright to the hint
            # we want to preserve the characters inside brackets
            # into the hint
            # therefore they shouldn't be an _ underscore
            hint += i
        elif not i.isalpha():
            # preserve punctuation
            hint += i
        else:
            inside_brackets = False
            # if we're not in brackets
            # the character is neither of ( or )
            # and the character isn't in my_modules.my_modules.constants.chars_to_ignore
            # it must be turned into an _

            # change the underscore to a monospaced one, makes more sense for japanese and chinese that way
            if is_japanese_char(i) or is_chinese_char(i):  
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

    # refers to the number of characters that will be revealed at the start of each word
    given_chars_in_hint = 1

    # iterating through the list with a while loop
    # incrementing the iterating variable manually

    inside_brackets = False

    while True:
        try:
            char = msg[i]
            if char in ['(', '（']:
                # if we're currently looking at a (
                # inside_brackets will be assigned True
                # add the ( to the hint
                inside_brackets = True
                hint += char
            elif char in [')', '）']:
                # if we're at the end of the bracket
                # add the ) to the hint
                # inside_brackets becomes False
                inside_brackets = False
                hint += char
            elif inside_brackets:
                # add the character stright to the hint
                # we want to preserve the characters inside brackets
                # into the hint
                # therefore they shouldn't be an _ underscore
                hint += char
            elif not char.isalpha():
                if char.isspace():
                    given_chars_in_hint = 1  # reset ready for the next word
                # preserve punctuation and numbers
                hint += char
            else:
                if given_chars_in_hint > 0:
                    hint += char
                    given_chars_in_hint -= 1
                else:
                    # hint += '_'
                    # change the underscore to a double space one for monospaced languages, makes more sense for japanese and chinese that way
                    if is_japanese_char(char) or is_chinese_char(char):  
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

    slashes = [i for i in range(len(msg)) if msg[i] == "/"]  # collect the indexes of where the slashes are in the hint
    msg = msg.replace("/", " ")  # replace them with a space, so the character after will be shown in the hint

    msg = list(msg)  # type: ignore

    i = 0
    inside_brackets = False

    # refers to the number of characters that will be revealed at the start of each word
    given_chars_in_hint = 3

    while True:
        try:
            char = msg[i]
            if char in ['(', '（']:
                inside_brackets = True
                hint += msg[i]  # add the open bracket to the hint
            elif char in [')', '）']:
                inside_brackets = False
                hint += char  # add the close bracket to the hint
            elif inside_brackets:
                # we want to preserve the char, and put it in the hint
                # to give the user leniency
                # they don't have to memorise what's in the ()
                # they'll only have to type it out
                hint += char
            elif not char.isalpha():
                if char.isspace():  # reset ready for the next word
                    given_chars_in_hint = 3
                hint += char
            else:
                if given_chars_in_hint > 0:
                    hint += char
                    given_chars_in_hint -= 1
                else:
                    # change the underscore to a monospaced one, makes more sense for japanese and chinese that way
                    if is_japanese_char(char) or is_chinese_char(char):  
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
        hint[i] = "/"  # put the slashes back into the hint at the end to preserve the hint

    hint = "".join(hint)

    return hint

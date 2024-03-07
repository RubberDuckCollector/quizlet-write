chars_to_ignore = [
    '.',
    ',',
    '\'',
    '\"',
    '`',
    ' ',  # space
    '_',
    '-',
    '+',
    '[',
    ']',
    '<',
    '>',
    # '(',
    # ')',
    '{',
    '}',
    ';'
]


# this is really good, but barely doesn't work
# really good concepts though
# e.g joins all elements in between elements with brackets together, they can be treated as one big element
# def make_easy_hint(msg: str) -> list:
#     words = []
#     current_word = ''
#     within_brackets = False

#     for i in msg:
#         if i == '(':
#             within_brackets = True
#             current_word += i
#         elif i == ')':
#             within_brackets = False
#             current_word += i
#             words.append(current_word)
#             current_word = ''
#         elif i == ' ' and not within_brackets:
#             if current_word:
#                 words.append(current_word)
#                 current_word = ''
#         else:
#             current_word += i

#     if current_word:
#         words.append(current_word)

#     hint = ""

#     print(words)
#     try:
#         for i in range(len(words)):
#             for j in range(len(words[i])):
#                 if words[i][j] in chars_to_ignore:
#                     hint += words[i][j]
#                 else:
#                     if j < 3 and words[i][j] != '(':
#                         hint += words[i][j]
#                     else:
#                         if msg[i][j] == '(':
#                             hint += msg[i]
#                             i += 1  # since the bracket stuff is done all at once, need to go to next i
#                         elif msg[i][j] in chars_to_ignore:
#                             hint += msg[i][j]
#                         else:
#                             hint += '_'


#     except IndexError:
#         pass

#     return hint


# def make_easy_hint(msg: str) -> str:
#     hint = ""
#     msg = list(msg)

#     i = 0
#     inside_brackets = False

#     while True:
#         try:
#             if msg[i] in chars_to_ignore:
#                 hint += msg[i]
#             else:
#                 if msg[i] == '(':
#                     inside_brackets = True
#                     hint += msg[i]
#                 elif msg[i] == ')':
#                     inside_brackets = False
#                     hint += msg[i]
#                 elif msg[i].isspace() and not inside_brackets:
#                     hint += msg[i]
#                 elif not inside_brackets:
#                     if i == 0 or msg[i - 1].isspace():
#                         hint += msg[i]  # Keep the first character of the word
#                     elif msg[i - 2].isspace() or i == 1:
#                         hint += msg[i]  # Keep the second character of the word
#                     elif msg[i - 3].isspace() or i == 2:
#                         hint += msg[i]  # Keep the third character of the word
#                     else:
#                         hint += "_"  # Replace other characters with underscore
#                 else:
#                     hint += msg[i]

#             i += 1
#         except IndexError:
#             break
#     return hint


def make_hard_hint(msg: str) -> list:
    words = []
    current_word = ''
    within_brackets = False

    for i in msg:
        if i == '(':
            within_brackets = True
            current_word += i
        elif i == ')':
            within_brackets = False
            current_word += i
            words.append(current_word)
            current_word = ''
        elif i == ' ' and not within_brackets:
            if current_word:
                words.append(current_word)
                current_word = ''
        else:
            current_word += i

    if current_word:
        words.append(current_word)

    hint = ""

    print(words)
    try:
        for i in range(len(words)):
            for j in range(len(words[i])):
                if '(' in words[i]:
                    hint += words[i]
                else:
                    if words[i][j] in chars_to_ignore:
                        hint += words[i][j]
                    else:
                        hint += '_'



    except IndexError:
        pass

    return hint


def make_easy_hint(msg: str) -> str:
    hint = ""
    msg = list(msg)

    i = 0
    inside_brackets = False

    while True:
        try:
            if msg[i] in chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] == '(':
                    inside_brackets = True
                    hint += msg[i]
                elif inside_brackets:
                    hint += msg[i]
                elif msg[i] == ')':
                    inside_brackets = False
                    hint += msg[i]
                elif msg[i].isspace() and not inside_brackets:
                    hint += msg[i]
                elif not inside_brackets:
                    if i == 0 or msg[i - 1].isspace():
                        hint += msg[i]  # Keep the first character of the word
                    elif msg[i - 2].isspace() or i == 1:
                        hint += msg[i]  # Keep the second character of the word
                    elif msg[i - 3].isspace() or i == 2:
                        hint += msg[i]  # Keep the third character of the word
                    else:
                        hint += "_"  # Replace other characters with underscore
                else:
                    hint += msg[i]

            i += 1
        except IndexError:
            break
    return hint


def main():
    # msg = "hello world (hello2 world)"
    msg = "die Gemeinschaft+ (-en ';;;asdf' test test) outside brackets now;;;"
    result = make_easy_hint(msg)
    result = make_hard_hint(msg)
    print("Result:", result)


if __name__ == '__main__':
    main()

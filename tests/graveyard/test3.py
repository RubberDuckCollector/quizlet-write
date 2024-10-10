import inspect, re
from pprint import pprint

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


# def make_normal_hint(msg: str) -> str:
#     hint = ""
#     msg = list(msg)

#     i = 0
#     j = 0

#     while True:
#         try:
#             if msg[i] in chars_to_ignore:
#                 hint += msg[i]
#             else:
#                 if msg[i] == '(':
#                     print("found a (")
#                     j = i
#                     while True:
#                         if msg[j] == ')':
#                             i = j
#                             hint += msg[j]
#                             print("end of bracket found, which is", i)
#                             print("i:", i)
#                             break
#                         else:
#                             hint += msg[j]

#                         j += 1
#                 else:
#                     hint += "_"


#             i += 1
#         except IndexError:
#             print("index error")
#             break
#     return hint

def make_normal_hint(msg: str) -> str:
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
                elif msg[i] == ')':
                    inside_brackets = False
                    hint += msg[i]
                elif msg[i].isspace() and not inside_brackets:
                    hint += msg[i]
                elif not inside_brackets:
                    hint += msg[i] if i == 0 or msg[i - 1].isspace() else "_"
                else:
                    hint += msg[i]

            i += 1
        except IndexError:
            break
    return hint


# def make_normal_hint(msg: str) -> str:
#     hint = ""
#     msg = list(msg)

#     i = 0
#     j = 0
#     inside_brackets = False

#     while True:
#         try:
#             if msg[i] in chars_to_ignore:
#                 hint += msg[i]
#             else:
#                 if msg[i] == '(':
#                     inside_brackets = True
#                     hint += msg[i]
#                     j = i + 1
#                     while True:
#                         if msg[j] == ')':
#                             i = j
#                             hint += msg[j]
#                             inside_brackets = False
#                             break
#                         else:
#                             hint += "_"

#                         j += 1
#                 elif msg[i] == ')':
#                     inside_brackets = False
#                     hint += msg[i]
#                 elif msg[i] == ' ':
#                     hint += msg[i]
#                 elif not inside_brackets:
#                     hint += msg[i]
#                 else:
#                     hint += "_"

#             i += 1
#         except IndexError:
#             break
#     return hint


def make_easy_hint(msg: str) -> str:
    hint = ""
    msg = list(msg)

    i = 0
    j = 0
    inside_brackets = False

    while True:
        try:
            if msg[i] in chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] == '(':
                    inside_brackets = True
                    hint += msg[i]
                    j = i
                    while True:
                        if msg[j] == ')':
                            i = j
                            hint += msg[j]
                            inside_brackets = False
                            break
                        else:
                            hint += msg[j]

                        j += 1
                elif msg[i] == ')':
                    inside_brackets = False
                    hint += msg[i]
                elif msg[i] == ' ':
                    hint += msg[i]
                elif not inside_brackets:
                    hint += msg[i]
                else:
                    hint += "_"

            i += 1
        except IndexError:
            break
    return hint

def main():
    msg = "die Gemeinschaft+ (-en ';;;asdf' test test) outside brackets now;;;"

    # print(make_normal_hint2(msg))
    print(make_normal_hint(msg))
    print(make_easy_hint(msg))


if __name__ == "__main__":
    main()

# DON'T TOUCH
# def make_normal_hint(msg: str) -> str:
#     hint = ""

#     msg = msg.split()  # can equate this to tokenising, each token is a word

#     try:
#         for i in range(len(msg)):
#             if i > 0:
#                 hint += " "
#             for j in range(len(msg[i])):
#                 if j == 0 and msg[i][j] != '(':
#                     hint += msg[i][j]
#                 else:
#                     if msg[i][j] == '(':
#                         hint += msg[i]
#                         i += 1  # since the bracket stuff is done all at once, need to go to next i
#                     elif msg[i][j] in chars_to_ignore:
#                         hint += msg[i][j]
#                     else:
#                         hint += '_'

#     except IndexError:
#         pass

#     return hint


# old version
# def make_easy_hint(msg: str) -> str:
#     hint = ""

#     msg = msg.split()  # can equate this to tokenising, each token is a word
#     print(msg)

#     try:
#         for i in range(len(msg)):
#             if i > 0:
#                 # i increments on each list element, so after each list element, add a space where it should go
#                 hint += " "
#             for j in range(len(msg[i])):
#                 if j < 3 and msg[i][j] != '(':
#                     hint += msg[i][j]
#                 else:
#                     if msg[i][j] == '(':
#                         hint += msg[i]
#                         i += 1  # since the bracket stuff is done all at once, need to go to next i
#                     elif msg[i][j] in chars_to_ignore:
#                         hint += msg[i][j]
#                     else:
#                         hint += '_'

#     except IndexError:
#         pass

#     return hint

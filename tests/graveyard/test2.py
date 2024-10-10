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
    '(',
    ')',
    '{',
    '}',
]

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


# don't touch
# def make_normal_hint(msg: str) -> str:
#     hint = ""

#     msg = list(msg)  # can equate this to tokenising, each token is a word

#     inside_brackets = False
#     # TODO: make it so the program goes into a "brackets mode" when it finds brackets
#     # preserves content inside brackets and the bracket chars themselves
#     # string processing goes back to normal otherwise
#     # with the first letter of each word being preserved
#     # otherwise it's turned into a _

#     try:
#         for i in range(len(msg)):
#             print("i: " + str(i))
#             if msg[i] in chars_to_ignore:
#                 hint += msg[i]
#             else:
#                 if msg[i] == '(':
#                     print("( has been found")
#                     inside_brackets = True
#                     # hint += '('
#                     j = i
#                     while inside_brackets is True:
#                         hint += msg[j]
#                         j += 1
#                         if msg[j] == ')':
#                             hint += ')'
#                             inside_brackets = False
#                 else:
#                     print("last branch: add _ to the hint")
#                     msg += '_'

#     except IndexError:
#         print("index error")

#     return hint

def merge(msg: list) -> str:
    # Find index of element containing '('
    start_index = next((i for i, elem in enumerate(my_list) if '(' in elem), None)

    if start_index is not None:
        # Find index of element containing ')'
        end_index = next((i for i, elem in enumerate(my_list) if ')' in elem and i > start_index), None)
        
        if end_index is not None:
            # Concatenate elements from start_index to end_index
            merged_string = ' '.join(my_list[start_index:end_index + 1])
            return merged_string
        else:
            print("Closing bracket not found.")
    else:
        print("Opening bracket not found.")

def make_normal_hint(msg: str) -> str:
    hint = ""

    msg = msg.split()  # can equate this to tokenising, each token is a word

    inside_brackets = False
    # TODO: the program looks for brackets
    # if it finds brackets, the program merges every list element in between the brackets
    # process list as normal

    try:


    except IndexError:
        print("index error")

    return hint

def main():
    msg = "die Gemeinschaft+ (-en a;lsdkfj;lasdj faljdksf ;asdfjkl afdsjkl lafs jfs) adfs;ljkfadsljk;afsdadflasdf;ll"

    print(make_normal_hint(msg))


if __name__ == '__main__':
    main()
